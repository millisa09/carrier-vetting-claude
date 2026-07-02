# The Daily Booked-Load Sweep ("are we secure right now?")

> The gate checks a carrier **once, at booking**. This sweep is the other half: insurance
> gets cancelled mid-load, authority gets revoked overnight, a payment-change email lands at
> 9 PM. Every morning before dispatch hours, every live load gets re-verified.
> **A clean gate yesterday is not a clean load today.**

## The three enforcement layers

| Layer | When | What |
|---|---|---|
| **1 · The gate** | every load, at booking | full `policies/compliance-gate.md` before the rate con |
| **2 · This sweep** | **daily, before dispatch hours** (7 days — freight moves on weekends) | every live load re-checked for drift; 🔴 = same-day action |
| **3 · Deep audit** | monthly, 1st | legal-counsel defensibility audit of exceptions + hard-stop integrity |
| *(+ triggers)* | event-driven | insurance lapse alert, authority change, fraud report, payment-change request → immediate re-vet |

## Steps

1. **Pull every live load** from your TMS/board — everything carrier-attached from
   pre-booking through delivery. Capture: load #, carrier, MC/DOT, status, delivery date.

2. **Per load, verify:**

   | # | Check | 🔴 unsecured when… |
   |---|---|---|
   | a | Gate evidence exists (safety verdict, signed agreement, W-9) | booked with **no gate record** (booked around the gate) |
   | b | **COI alive through the delivery date**, correct limits + cert holder | expired, or expires before delivery |
   | c | Authority still active (`scripts/fmcsa_pull.py <DOT>` — prioritize flagged, occasional, and new-authority carriers) | inactive/revoked, or new OOS order |
   | d | No new Conditional/Unsatisfactory rating since the gate ran | rating flipped mid-load |
   | e | Last compliance check within your cadence | ⚠️ stale — queue a re-check, not 🔴 |
   | f | Exception loads: the 4-question note exists AND this load is inside the approved scope | note missing, or load outside scope |
   | g | Carrier not marked Do-Not-Use after booking | DNU carrier on a live load |
   | h | No new fraud/identity/payment-change signals since booking | unresolved new signal |

3. **Grade:** 🟢 secure · ⚠️ attention (stale check, COI expiring within 7 days) ·
   🔴 **unsecured** (any right-column hit).

4. **Write the report** → `sweeps/SWEEP_<YYYY-MM-DD>.md` (one row per load: load · carrier ·
   MC · status · grade · finding · evidence). Append a timestamped row to each checked
   carrier's profile check log.

5. **Escalate by grade:**
   - 🔴 → notify the owner **immediately** with the finding + recommended action (pause
     dispatch, replace carrier, verify insurer directly). A 🔴 on a not-yet-picked-up load =
     **hold the pickup info** until resolved.
   - ⚠️ only → list in the report, queue re-checks. No alert.
   - all 🟢 → silent. Clean day = no noise.

## Guardrails

- Never auto-contact a carrier about anything financial or a suspicion.
- A 🔴 pauses and escalates — it does not auto-cancel. Restrict/suspend stays human.
- Unverifiable check = `TBD` + ⚠️, never silently passed.
- Don't hammer the FMCSA API for every regular carrier daily — the monthly cadence covers
  regulars; the sweep pulls live data for flagged/occasional/new-authority carriers.
