# carrier-vetting-claude 🚛⚖️

**A CAVRA-aligned carrier vetting & compliance system for freight brokerages, built to run on [Claude Code](https://claude.com/claude-code).**

Point Claude at your carrier database, drop in these policies and agents, and you get a
working compliance desk: a written vetting policy, a pre-book gate, a daily "are we still
secure?" sweep over every booked load, and an AI legal-counsel desk that audits your
decisions for defensibility — the way a plaintiff attorney would.

Built by a working freight brokerage, sanitized and open-sourced so other brokerages
don't have to start from zero.

> ⚠️ **This is not legal advice.** It's an operating template. Have your own attorney and
> insurance professionals review anything you adopt. See [Credits & attribution](#credits--attribution).

---

## Why

After a catastrophic crash or a stolen load, the question a court asks a broker is not
*"was your decision perfect?"* It's:

> **Based on the information available at the time, did you make a reasonable and
> defensible carrier selection — or did you ignore warning signs a reasonable
> transportation provider would have caught?**

Most small brokerages have no written policy, inconsistent vetting, and undocumented
exceptions — the exact three things that lose negligent-selection cases. This kit gives
you the written policy, the enforcement rails, and the paper trail, with Claude doing the
repetitive work.

## What's in the box

```
carrier-vetting-claude/
├── CLAUDE.md                          ← project instructions (fill in your company)
├── policies/
│   ├── carrier-vetting-policy.md      ← your written vetting law (CAVRA-aligned template)
│   └── compliance-gate.md             ← the pre-book gate: no rate con until cleared
├── .claude/agents/
│   ├── compliance-officer.md          ← the gate-keeper desk (vets every carrier)
│   └── legal-counsel.md               ← the law desk (audits, contracts, incidents)
├── sops/
│   ├── booked-load-sweep.md           ← daily sweep: re-verify every live load
│   └── scheduled-tasks-setup.md       ← how to put the sweep + audit on a schedule
├── scripts/
│   └── fmcsa_pull.py                  ← pull authority/safety/OOS from FMCSA QCMobile (free API)
└── templates/
    ├── exception-note.md              ← the 4-question exception record
    ├── risk-acceptance-log.md         ← the log a defense attorney wishes you kept
    └── carrier-profile.md             ← one folder per carrier, evidence attached
```

## Quickstart

1. **Install [Claude Code](https://claude.com/claude-code)** and clone this repo (or copy it
   into your compliance workspace).
2. **Fill in the placeholders** — search for `{{` across the repo: company name, insurance
   minimums, your safety thresholds, who can approve exceptions.
3. **Get a free FMCSA webKey** at https://mobile.fmcsa.dot.gov/QCDevsite/ and set it:
   `export FMCSA_WEBKEY=your-key` (or put it in a local `.env` — never commit it).
   Test: `python scripts/fmcsa_pull.py <DOT_NUMBER>`.
4. **Connect your carrier database.** Claude Code can read whatever you have:
   - a folder of carrier files/PDFs (works out of the box — this kit assumes one folder per carrier),
   - a TMS with an API (ask Claude to write a small pull script for it),
   - an MCP server for your TMS if one exists,
   - even a spreadsheet export. Files are a perfectly good database.
5. **Vet your first carrier:** open Claude Code in this folder and say
   *"Run the compliance gate on carrier MC 123456 for a dry van load, pickup Friday."*
   The compliance-officer agent walks the gate and writes the evidence to the carrier profile.
6. **Schedule the sweep** — see `sops/scheduled-tasks-setup.md` for the daily 6:45 AM
   booked-load sweep and the monthly defensibility audit.

## Go further: add Carrier Assure to your Claude 🔌

The CAVRA Standard recommends benchmarking every carrier against a third-party risk platform,
not just government data — and the platform built by CAVRA's own author is
**[Carrier Assure](https://www.carrierassure.com/)** (Cassandra Gaines' company). It scores
carriers **A–F** by combining safety, fraud, and operational data.

**Reach out to Carrier Assure for API access** (https://www.carrierassure.com/) and wire it
into this kit — ask Claude to write the integration once you have credentials. With a score
feed connected, the gate and the daily sweep get a benchmarking layer on top of FMCSA data:

| Score | How the gate treats it (per the CAVRA Standard) |
|-------|--------------------------------------------------|
| **A / B / C** | Supports ordinary review — continue the normal gate |
| **D** | Review the displayed weaknesses; determine whether they affect this shipment |
| **F** | **Not ordinary capacity.** Documented diligence, senior approval, and a written record (Carrier Assure's Due Diligence Certificate or equivalent) before any use — and if the F is tied to safety data that fails your adopted thresholds, the carrier may not be used |

If your onboarding platform passes a carrier but Carrier Assure flags an F, don't ignore the
conflict — review it, decide under your written policy, and document the mitigating facts.
(This kit is not affiliated with or endorsed by Carrier Assure; it's simply the tool the
source framework was designed around.)

## The three enforcement layers

| Layer | When | What |
|-------|------|------|
| **The gate** | Every load, at booking | Full vetting before a rate confirmation goes out. Hard stops are non-negotiable. |
| **The daily sweep** | Every morning, before dispatch | Every live load re-verified: insurance still active through delivery, authority not revoked, no new red flags. Insurance dies overnight; a clean gate yesterday is not a clean load today. |
| **The monthly audit** | 1st of the month | The legal-counsel agent audits last month's exceptions and hard-stop integrity the way opposing counsel would — while there's still time to fix the record. |

## Credits & attribution

This kit stands on two people who **built in public**:

- **[Cassandra Gaines](https://www.logisticsriskexpert.com/cavra-standard/)** — transportation
  attorney, expert witness, and CEO of **[Carrier Assure](https://www.carrierassure.com/)** —
  author of **The CAVRA Standard:
  Carrier Assessment, Verification, Risk, and Accountability in Reasonable Carrier Selection**
  (v1.0, June 2026), published free for the industry. The policy templates in this kit are
  *adaptations inspired by* her framework. Per her use notice: the CAVRA Standard is hers;
  modifications here are our own and are **not** attributed to her; nothing in this kit is
  "CAVRA certified" or endorsed by her or Carrier Assure. Read the original — it's excellent:
  https://www.logisticsriskexpert.com/cavra-standard/

- **[Zubair Trabzada](https://github.com/zubair-trabzada/ai-legal-claude)** — author of
  **ai-legal-claude**, an open-source AI legal-assistant architecture for Claude Code
  (multi-agent contract review, risk scoring, plain-language translation). The
  legal-counsel agent in this kit borrows its architecture ideas and, just as importantly,
  its honest disclaimer discipline.

Thank you both. This repo exists to pay that forward.

## Disclaimers (read these)

- **Not legal advice.** No attorney-client relationship is created by using this kit. Consult
  a licensed transportation attorney before adopting any policy.
- **Not a certification.** Using this kit does not make you "CAVRA compliant" and does not
  guarantee safety outcomes, claim avoidance, or favorable litigation results.
- **Your numbers are your decision.** The thresholds shipped here are common industry
  reference points; your freight profile, insurers, and counsel determine yours.
- **The templates must be edited.** A policy you don't actually follow is worse than no
  policy. Adopt only what you will enforce consistently.

## License

MIT — see [LICENSE](LICENSE). The CAVRA Standard itself belongs to Cassandra Gaines and is
not part of this license; reference it with attribution per her published use notice.
