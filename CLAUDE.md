# Notes for agents working on this skill

## Install commands are for Windows PowerShell

The maintainer runs Windows PowerShell 5.1, and so do many users of a published
skill. Two things break there, both silently and both repeatedly:

- **Use `npx.cmd`, never bare `npx`.** In PowerShell `npx` resolves to
  `npx.ps1`, which the default execution policy refuses to load —
  `PSSecurityException / UnauthorizedAccess`. The `.cmd` shim is not a
  PowerShell script, so it runs without touching the policy. Never suggest
  changing the execution policy to work around this; it weakens a security
  setting to save one character.
- **No `&&`.** PowerShell 5.1 has no `&&` operator. Give each command on its own
  line, or join with `;` if they genuinely must be one line.

So the shape to hand someone is:

```
npx.cmd -y skills@latest add <owner>/<repo>@<skill> -g -y
```
