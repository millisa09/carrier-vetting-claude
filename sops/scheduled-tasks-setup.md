# Putting the system on a schedule (Claude Code)

Two recurring runs make this system self-enforcing. In Claude Code, just ask:

## 1 · The daily sweep

> "Create a scheduled task called `daily-compliance-sweep` that runs every day at 6:45 AM.
> Each run: read and execute `sops/booked-load-sweep.md` verbatim — pull every live load,
> re-verify the 8 checks per load, grade 🟢/⚠️/🔴, write the report to `sweeps/`, and if any
> load is 🔴, alert me immediately with the finding and recommended action."

Pick a time **before your dispatch hours** so problems are caught before trucks roll.
Run daily, all 7 days — freight moves on weekends.

## 2 · The monthly defensibility audit

> "Create a scheduled task called `monthly-defensibility-audit` that runs on the 1st of every
> month at 7 AM. Each run: act as the legal-counsel agent and audit the prior month —
> exception-note quality (the 4 questions), hard-stop integrity, sweep-finding resolution,
> and threshold consistency. Write a dated memo to `audits/` ranked by severity with a fix list."

## Notes

- **First run:** click "Run now" once on each task to pre-approve the tools it needs, so
  future runs don't pause on permission prompts. It also doubles as a live shakedown.
- Claude Code scheduled tasks run while the app is open; if the machine is off at fire time,
  the task runs on next launch. For fully unattended operation, run the same prompts headless
  via `claude -p` on your OS scheduler (Task Scheduler / cron), or port the sweep to a
  workflow tool.
- The sweep needs access to your loads (TMS API/MCP/export) and your carrier profiles —
  wire those in `CLAUDE.md` first.
- **Cadence summary:** gate = every load at booking · sweep = every morning ·
  audit = monthly · re-vet = on triggers (lapse, authority change, fraud alert, 120-day
  inactivity).
