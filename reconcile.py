#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json
from decimal import Decimal

latest = {}

with open("payments.jsonl") as f:
    for line in f:
        try:
            e = json.loads(line)
            if not isinstance(e, dict) or not e.get("txn_id") or "ts" not in e:
                continue
            tid = e["txn_id"]
            if tid not in latest or e["ts"] > latest[tid]["ts"]:
                latest[tid] = {"ts": e["ts"], "event": e}
        except (ValueError, TypeError):
            continue

payments = []
for item in latest.values():
    e = item["event"]
    if e.get("status") == "success":
        try:
            payments.append(Decimal(str(e["amount"]).replace(",", "")))
        except (KeyError, ValueError):
            continue

count, total = len(payments), sum(payments, 0)

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count == expected:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
else:
    print(
        f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")

"""
The script was fixed to:

- Keep only the latest attempt for each txn_id.
- Count only transactions whose latest status is `success`.
- Ignore malformed JSON lines and events without a txn_id.
- Use Decimal to calculate money accurately and avoid floating-point errors.
- Compare the successful payment count with expected.txt and print the verification result and code if it matches.
"""
