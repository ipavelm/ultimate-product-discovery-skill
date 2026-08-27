#!/usr/bin/env python3
"""Initialise the Knowledge Base for a new PD run.

Creates /home/claude/pd-knowledge-base.md with the correct frontmatter:
skill-version, project-name, mode, created. This is what stops the
"Mode: [Light / Full / GeoExpansion]" placeholder from being left unfilled.

It also creates /home/claude/.pd_env exporting PD_MODE, which the scripts
covered by Rule 1 in SKILL.md need (delete_light_slides.py and others):

    source /home/claude/.pd_env

Usage:
    python3 init_kb.py --project "TimeTag" --mode Light
    python3 init_kb.py --project "My Startup" --mode Full --output /home/claude/pd-kb.md
    python3 init_kb.py --project "Bittrace Thailand" --mode GeoExpansion
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

SKILL_VERSION = "4.1"

TEMPLATE = """# PD Knowledge Base — {project}
skill-version: {version}
created: {date}
updated: {date}
mode: {mode}

## Execution log (incremental)

_Append an entry here after every task. Format:_
_### [Date, time] — Task N: [name] — done|partial|blocked_
_- 3–5 key findings_

---

## Block I: Market (full summary)
_Filled in once block I is complete._

## Block II: Customers
_Filled in once block II is complete._

## Block III: Strategy
_Filled in once block III is complete._

## Block IV: Hypotheses
_Filled in once block IV is complete._

## Block V: Main scenario
_Filled in after task 18a._

## Status
- Last completed task: —
- Last completed block: —
- Next step: start with Task 1 (market analysis)
"""

# For GeoExpansion — an extra home-geo baseline section
GEO_EXPANSION_EXTRA = """

## Home-geo baseline (Geographic Expansion only)
_Fill this in during Step 0, before block I starts:_
- Home geography: [the country/region where the product already runs]
- Paying customers in the home geography: [count]
- ARR in the home geography: [amount]
- Launched in the home geography: [month/year]
- Key home-geo metrics: LTV=[X], CAC=[Y], retention=[Z]%
- Why we are moving into a new geography: [the core hypothesis]
- Target geography: [country/region]
- Multi-geo roadmap: [the next geographies with SAM estimates, if any]
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--project", required=True, help="Project name")
    ap.add_argument("--mode", required=True,
                    choices=["Light", "Full", "GeoExpansion"],
                    help="Mode: Light / Full / GeoExpansion")
    ap.add_argument("--output", default="/home/claude/pd-knowledge-base.md",
                    help="Path to the KB file (default: /home/claude/pd-knowledge-base.md)")
    ap.add_argument("--env-output", default="/home/claude/.pd_env",
                    help="Path to the env file (default: /home/claude/.pd_env)")
    args = ap.parse_args()

    output_path = Path(args.output)
    if output_path.exists():
        print(f"Warning: file {output_path} already exists. Overwrite? [y/N] ", end="")
        if input().strip().lower() != "y":
            print("Cancelled.")
            sys.exit(0)

    content = TEMPLATE.format(
        project=args.project,
        version=SKILL_VERSION,
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        mode=args.mode,
    )
    if args.mode == "GeoExpansion":
        content += GEO_EXPANSION_EXTRA

    output_path.write_text(content, encoding="utf-8")
    print(f"Knowledge Base created: {output_path}")
    print(f"  Project: {args.project}")
    print(f"  Mode: {args.mode}")

    env_path = Path(args.env_output)
    env_content = f"""# PD environment -- created {datetime.now().strftime('%Y-%m-%d %H:%M')}
# Source this file before running scripts from SKILL.md Rule 1:
#   source {args.env_output}
#
# This protects delete_light_slides.py from running in Full/GeoExpansion mode
# (which would delete 13 needed slides).

export PD_MODE={args.mode}
export PD_PROJECT="{args.project}"
"""
    env_path.write_text(env_content, encoding="utf-8")
    print(f"Environment created: {env_path}")
    print(f"  Before running scripts, execute: source {env_path}")


if __name__ == "__main__":
    main()
