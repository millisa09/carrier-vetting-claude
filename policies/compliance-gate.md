# The Compliance Gate (Pre-Book → Booked)

> A carrier passes **every check** below before a rate confirmation goes out. No cleared
> gate, no booked load. Every outcome — pass, exception, decline — is logged with evidence.

## Check 1 — Safety (FMCSA + your vetting platform)

- **Safety rating:** None/Satisfactory = OK · **Conditional / Unsatisfactory = HARD STOP.**
- **BASIC scores** against your adopted thresholds (`policies/carrier-vetting-policy.md` §4).
  Over threshold in your disqualifying number of categories = hard stop.
- Pull live: `python scripts/fmcsa_pull.py <DOT>` (authority, OOS rates, crashes, inspections).
- **Third-party benchmark (recommended):** if you have a Carrier Assure feed
  (https://www.carrierassure.com/ — API access on request), check the score: A/B/C = ordinary
  review · D = review weaknesses · **F = not ordinary capacity** (documented diligence + senior
  approval before use; an F tied to failing safety thresholds = do not use).
- **Fraud signals** (decline or heavy scrutiny regardless of scores): fraud/double-brokering
  reports on your vetting platform · more trucks inspected than owned (VIN anomaly / cloning) ·
  FMCSA undeliverable mail · brand-new authority + tiny fleet chasing big freight (chameleon) ·
  insurance history full of lapses and short policies.

## Check 2 — Documents on file

| Doc | Requirement |
|---|---|
| Broker-Carrier Agreement | signed, on file |
| Certificate of Insurance | **{{COMPANY_NAME}} as certificate holder** · not expired · ≥ ${{1M}} auto / ${{100K}} cargo · verify it **applies** to this equipment/commodity/lane |
| W-9 | on file |

High-value freight: if cargo value exceeds the carrier's cargo coverage, the carrier carries
more, or you buy shipper's-interest coverage the customer agrees to. Never move high-value
freight under-insured.

## Check 3 — Identity (anti-fraud)

Compare the booking contact (caller ID, email) to the carrier's **FMCSA-listed** phone/email.
Mismatch → call the FMCSA number and confirm the dispatcher actually works there **before**
booking. Watch for independent dispatchers representing multiple carriers — you pay the
carrier, never a dispatcher. No booking until identity is confirmed.

## Check 4 — Truck-on-insurance (flagged carriers)

For any red-flag carrier (VIN anomaly, few/no inspections, poor safety, fraud report): get the
truck's VIN-last-6 / year / make, then **call the insurer** and confirm that specific truck
and driver are on the active policy. A valid COI on paper can still mean an uninsured truck
on your freight. Not on policy / can't confirm = do not book.

## Check 5 — CAVRA baselines

| Baseline | Rule | On a miss |
|---|---|---|
| Authority age | ≥ 90 days continuous | 30–89 days → documented review; < 30 days → senior approval, one-load limit, enhanced verification |
| Roadside inspections | ≥ 1 in prior 24 months | Escalate + exception note + controls |
| New-carrier volume | one trial load | expand after clean POD/tracking/payment review |
| Shipment suitability | carrier fits THIS load | enhanced-risk freight → heightened review |
| Re-vet trigger | inactive > 120 days, lapse, authority change, fraud alert | full gate re-run |

## The decision

- **All clear (or exception properly approved):** send the rate confirmation → Booked.
- **Docs missing:** obtain first.
- **Baseline miss:** escalate → 4-question exception note (`templates/exception-note.md`)
  → approved scope only.
- **Hard stop:** decline. Log it. Find another carrier — every time.

**After booking, the gate stays live:** the daily sweep (`sops/booked-load-sweep.md`)
re-verifies every live load until delivery.
