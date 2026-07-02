#!/usr/bin/env python3
"""
fmcsa_pull.py — pull a carrier's live safety snapshot from the FMCSA QCMobile API.

Usage:
    export FMCSA_WEBKEY=your-key      # free key: https://mobile.fmcsa.dot.gov/QCDevsite/
    python fmcsa_pull.py <DOT_NUMBER>

Prints a JSON snapshot plus a paste-ready markdown block for the carrier profile:
authority status, allowed-to-operate, safety rating, driver/vehicle OOS rates,
crash counts, inspections, fleet size, BASICs (where available).

Key can also live in a local file `.fmcsa-webkey` next to this script (gitignored
via *-key.txt patterns — name it .env style or keep it out of the repo).
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

BASE = "https://mobile.fmcsa.dot.gov/qc/services/carriers"


def get_key() -> str:
    key = os.environ.get("FMCSA_WEBKEY", "").strip()
    if not key:
        keyfile = os.path.join(os.path.dirname(__file__), ".fmcsa-webkey")
        if os.path.exists(keyfile):
            key = open(keyfile, encoding="utf-8").read().strip()
    if not key:
        sys.exit("FMCSA_WEBKEY not set. Get a free key at https://mobile.fmcsa.dot.gov/QCDevsite/")
    return key


def fetch(path: str, key: str):
    url = f"{BASE}/{path}?webKey={key}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        sys.exit("Usage: python fmcsa_pull.py <DOT_NUMBER>")
    dot, key = sys.argv[1], get_key()

    carrier = fetch(dot, key).get("content", {}).get("carrier", {})
    if not carrier:
        sys.exit(f"No carrier found for DOT {dot}")
    try:
        basics = fetch(f"{dot}/basics", key).get("content", [])
    except Exception:
        basics = []
    try:
        authority = fetch(f"{dot}/authority", key).get("content", [])
    except Exception:
        authority = []

    snap = {
        "pulled_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dot": dot,
        "legal_name": carrier.get("legalName"),
        "dba": carrier.get("dbaName"),
        "allowed_to_operate": carrier.get("allowedToOperate"),
        "status_code": carrier.get("statusCode"),
        "safety_rating": carrier.get("safetyRating"),
        "safety_rating_date": carrier.get("safetyRatingDate"),
        "oos_date": carrier.get("oosDate"),
        "driver_oos_rate": carrier.get("driverOosRate"),
        "driver_oos_natl_avg": carrier.get("driverOosRateNationalAverage"),
        "vehicle_oos_rate": carrier.get("vehicleOosRate"),
        "vehicle_oos_natl_avg": carrier.get("vehicleOosRateNationalAverage"),
        "crash_total": carrier.get("crashTotal"),
        "fatal_crash": carrier.get("fatalCrash"),
        "injury_crash": carrier.get("injCrash"),
        "driver_inspections": carrier.get("driverInsp"),
        "vehicle_inspections": carrier.get("vehicleInsp"),
        "total_power_units": carrier.get("totalPowerUnits"),
        "total_drivers": carrier.get("totalDrivers"),
        "authority": authority,
        "basics": basics,
    }
    print(json.dumps(snap, indent=2))

    # Paste-ready profile block
    rating = snap["safety_rating"] or "None (Unrated)"
    hard_stop = rating.upper().startswith(("C", "U")) and rating != "None (Unrated)"
    print("\n--- paste into the carrier profile ---\n")
    print(f"## Safety snapshot (FMCSA QCMobile, {snap['pulled_at_utc']})")
    print(f"- Legal name: {snap['legal_name']}  (DOT {dot})")
    print(f"- Allowed to operate: {snap['allowed_to_operate']}  · OOS order date: {snap['oos_date'] or 'none'}")
    print(f"- Safety rating: {rating}{'  🚩 HARD STOP' if hard_stop else ''}")
    print(f"- Driver OOS: {snap['driver_oos_rate']}% (natl avg {snap['driver_oos_natl_avg']}%)")
    print(f"- Vehicle OOS: {snap['vehicle_oos_rate']}% (natl avg {snap['vehicle_oos_natl_avg']}%)")
    print(f"- Crashes: {snap['crash_total']} total / {snap['fatal_crash']} fatal / {snap['injury_crash']} injury")
    print(f"- Inspections: {snap['vehicle_inspections']} vehicle / {snap['driver_inspections']} driver")
    print(f"- Fleet: {snap['total_power_units']} power units · {snap['total_drivers']} drivers")
    if snap["vehicle_inspections"] in (0, None):
        print("- ⚠️ No/limited inspection history — never treat as ordinary capacity (see policy §5)")


if __name__ == "__main__":
    main()
