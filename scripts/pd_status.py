#!/usr/bin/env python3
"""Report where an interrupted PD run actually stands.

The Knowledge Base is prose, which is right for handing context to a person but
leaves resuming to whoever reads it: the log is free-form, entries can be
missing, and nothing connects a line saying an artifact was produced to the file
being on disk. This parses the KB into a definite answer — mode, which of the 18
tasks are done, what comes next — and then checks that answer against reality
rather than trusting it.

The inconsistencies matter more than the progress. A log claiming block VI is
finished while `/mnt/user-data/outputs/` is empty means the run died during
artifact generation, and resuming from task 19 would ship nothing.

Usage:
    python3 pd_status.py                          # default KB location
    python3 pd_status.py --kb /path/to/kb.md
    python3 pd_status.py --json                   # machine-readable
    python3 pd_status.py --outputs /some/dir      # where artifacts should be
"""
import argparse
import json
import os
import re
import sys

SKILL_VERSION = "4.2"
DEFAULT_KB = "/home/claude/pd-knowledge-base.md"
DEFAULT_OUTPUTS = "/mnt/user-data/outputs"

# Task 18 is split into 18a (financial parameters) and 18b/c/d (the artifacts),
# so it is tracked as one task with several deliverables.
BLOCKS = [
    ("I. Market analysis", range(1, 7)),
    ("II. Customers", range(7, 10)),
    ("III. Strategy", range(10, 15)),
    ("IV. Validation", range(15, 18)),
    ("V. Main scenario", [18]),
    ("VI. Artifacts", [18]),
]
# Light runs a subset; Full and Geographic Expansion run everything.
LIGHT_TASKS = [1, 3, 5, 7, 10, 11, 12, 14, 18]
ALL_TASKS = list(range(1, 19))

ARTIFACTS = [
    ("one-pager", ".pptx"),
    ("financial-plan", ".xlsx"),
    ("presentation", ".pptx"),
    ("interview-guide", ".docx"),  # Full mode only
]

FM = re.compile(r"^([a-z-]+):\s*(.+?)\s*$", re.M)
# ### [Date, time] — Task N: [name] — done|partial|blocked
ENTRY = re.compile(
    r"^#{2,4}\s*\[?([^\]\n]*?)\]?\s*[—–-]+\s*Task\s*(\d+)\s*[a-d]?\s*:\s*(.*?)\s*[—–-]+\s*"
    r"(done|partial|blocked)\b",
    re.M | re.I,
)
PLACEHOLDER = re.compile(r"\[.*(?:Light|Full|GeoExpansion).*\]|^\s*$")


def parse_kb(text):
    head = text.split("## ", 1)[0]
    fm = {k: v for k, v in FM.findall(head)}
    # init_kb.py puts the project in the H1 title rather than in frontmatter
    title = re.match(r"#\s*PD Knowledge Base\s*[—–-]+\s*(.+)", head.strip())
    if title and "project-name" not in fm:
        fm["project-name"] = title.group(1).strip()
    entries = []
    for when, num, name, status in ENTRY.findall(text):
        entries.append({
            "task": int(num),
            "name": name.strip().strip("[]"),
            "status": status.lower(),
            "when": when.strip(),
        })
    return fm, entries


def expected_tasks(mode):
    m = (mode or "").strip().lower()
    # The template's placeholder lists every mode, so a substring test would
    # match it and report a mode nobody chose. Reject it before resolving.
    if m.startswith("[") or "/" in m:
        return ALL_TASKS, None
    if m.startswith("light"):
        return LIGHT_TASKS, "Light"
    if m.startswith("full"):
        return ALL_TASKS, "Full"
    if "geo" in m:
        return ALL_TASKS, "Geographic Expansion"
    return ALL_TASKS, None


def block_of(task):
    for name, rng in BLOCKS[:-1]:
        if task in rng:
            return name
    return BLOCKS[-1][0]


def find_artifacts(outputs_dir):
    found = {}
    if not os.path.isdir(outputs_dir):
        return found, False
    names = os.listdir(outputs_dir)
    for stem, ext in ARTIFACTS:
        hits = [n for n in names if n.startswith(stem) and n.endswith(ext)]
        if hits:
            found[stem] = sorted(hits)
    return found, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", default=DEFAULT_KB)
    ap.add_argument("--outputs", default=DEFAULT_OUTPUTS)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.kb):
        msg = (f"No Knowledge Base at {a.kb}. Either this is a fresh run — start with "
               f"init_kb.py — or the KB was written somewhere else; pass --kb.")
        print(json.dumps({"error": "kb_missing", "kb": a.kb, "message": msg}, indent=2)
              if a.json else msg)
        return 2

    text = open(a.kb).read()
    fm, entries = parse_kb(text)
    tasks, mode_name = expected_tasks(fm.get("mode"))

    status = {}
    for e in entries:  # later entries win, so a retried task reflects its latest run
        status[e["task"]] = e
    done = sorted(t for t in tasks if status.get(t, {}).get("status") == "done")
    partial = sorted(t for t in tasks if status.get(t, {}).get("status") == "partial")
    blocked = sorted(t for t in tasks if status.get(t, {}).get("status") == "blocked")
    remaining = [t for t in tasks if t not in done]
    next_task = remaining[0] if remaining else None

    artifacts, outputs_exist = find_artifacts(a.outputs)

    problems = []
    raw_mode = (fm.get("mode") or "").strip()
    if not raw_mode or PLACEHOLDER.match(raw_mode) or mode_name is None:
        problems.append(
            f"mode is {raw_mode!r}, which is not one of Light / Full / GeoExpansion. "
            "The KB template's placeholder was never replaced, so the task list below "
            "assumes Full. Ask which mode this run is in before continuing.")
    if fm.get("skill-version") and fm["skill-version"] != SKILL_VERSION:
        problems.append(
            f"KB was written by skill version {fm['skill-version']}, this is "
            f"{SKILL_VERSION}. Section layout and task numbering may differ.")
    if not entries:
        problems.append(
            "the execution log has no parseable entries. Either nothing was logged or "
            "the format drifted from '### [date] — Task N: name — done|partial|blocked'. "
            "Progress below cannot be trusted; confirm with the person.")
    # a claim of finished artifacts that the filesystem does not support
    if 18 in done and not artifacts:
        problems.append(
            f"task 18 is logged done but no artifact was found in {a.outputs}. The run "
            "most likely died during artifact generation — redo block VI rather than "
            "treating PD as finished.")
    if artifacts and 18 not in done:
        problems.append(
            f"artifacts exist in {a.outputs} but task 18 is not logged done. Check "
            "whether they are complete or left over from an earlier attempt.")
    if not outputs_exist:
        problems.append(f"{a.outputs} does not exist, so no artifact could be verified.")
    # gaps: a later task done while an earlier one never was
    gaps = [t for t in tasks if t not in done and any(d > t for d in done)]
    if gaps:
        shown = ", ".join(str(g) for g in gaps[:6]) + ("…" if len(gaps) > 6 else "")
        problems.append(
            f"{len(gaps)} task(s) never reached done while a later task did ({shown}). "
            "Either they were deliberately skipped, or entries were lost from the log — "
            "confirm which before treating the later work as resting on them.")

    if a.json:
        json.dump({
            "kb": a.kb, "project": fm.get("project-name") or fm.get("project"),
            "mode": mode_name, "mode_raw": raw_mode,
            "skill_version_kb": fm.get("skill-version"),
            "skill_version_current": SKILL_VERSION,
            "updated": fm.get("updated"),
            "tasks_expected": tasks, "done": done, "partial": partial,
            "blocked": blocked, "remaining": remaining, "next_task": next_task,
            "artifacts": artifacts, "problems": problems,
        }, sys.stdout, indent=2)
        print()
        return 1 if problems else 0

    print(f"# PD status — {fm.get('project-name') or fm.get('project') or 'unnamed project'}")
    print(f"\nKB        : {a.kb}")
    print(f"mode      : {mode_name or raw_mode or '(not set)'}")
    print(f"updated   : {fm.get('updated', '(unknown)')}")
    print(f"progress  : {len(done)}/{len(tasks)} tasks done"
          + (f", {len(partial)} partial" if partial else "")
          + (f", {len(blocked)} blocked" if blocked else ""))

    print("\nper block:")
    for name, rng in BLOCKS[:5]:
        in_block = [t for t in tasks if t in rng]
        if not in_block:
            continue
        d = [t for t in in_block if t in done]
        mark = "done" if len(d) == len(in_block) else f"{len(d)}/{len(in_block)}"
        print(f"  {name:22s} {mark}")

    if partial or blocked:
        print()
        for t in partial:
            print(f"  partial: task {t} — {status[t]['name']}")
        for t in blocked:
            print(f"  blocked: task {t} — {status[t]['name']}")

    print(f"\nartifacts in {a.outputs}:")
    if artifacts:
        for stem, hits in artifacts.items():
            print(f"  {stem:16s} {', '.join(hits)}")
    else:
        print("  none found")

    if next_task:
        print(f"\nnext      : task {next_task} ({block_of(next_task)})")
    else:
        print("\nnext      : every task in this mode is logged done")

    if problems:
        print(f"\ninconsistencies ({len(problems)}) — resolve before continuing:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("\nno inconsistencies between the log and the filesystem.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
