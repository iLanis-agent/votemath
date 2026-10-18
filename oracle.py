#!/usr/bin/env python3
# Vote Math oracle - mirrors engine.js.
import json, math

def _int(x, lo, hi, msg):
    if not math.isfinite(x) or x % 1 != 0 or x < lo or x > hi:
        raise ValueError(msg)

def _num(x):
    return str(int(x)) if x == int(x) else repr(x)

def _pct(p):
    if not math.isfinite(p) or p <= 0 or p > 100:
        raise ValueError("required percent must be over 0 and at most 100")

def _need(base, pct):
    return math.ceil(base * pct / 100 - 1e-9)

def _s(n, one, many):
    return one if n == 1 else many

def quorum_truth(members, pct, present):
    _int(members, 1, 100000, "members must be a whole number from 1 to 100000")
    _pct(pct)
    _int(present, 0, members, "present must be a whole number from 0 up to the member count")
    need = _need(members, pct)
    diff = present - need
    tail = f"over by {diff}" if diff > 0 else "exactly enough" if diff == 0 else f"short by {-diff}"
    return f"{int(members)} {_s(members, 'member', 'members')}, quorum {_num(pct)}%: {need} must be present. {int(present)} present: {tail}."

def _tally(f, a, ab):
    for x in (f, a, ab):
        _int(x, 0, 1000000, "votes must be whole numbers, 0 or more")

def _vs(f, need):
    d = f - need
    t = f"enough by {d}" if d > 0 else "exactly enough" if d == 0 else f"short by {-d}"
    return f"{need} {'is' if need == 1 else 'are'} needed, {t}"

def threshold_truth(f, a, ab, pct):
    _tally(f, a, ab)
    _pct(pct)
    fa = f + a
    cast = f + a + ab
    if fa <= 0:
        raise ValueError("enter at least one vote for or against")
    lead = f"For {f}, against {a}, abstain {ab}. Required {_num(pct)}%: "
    if ab == 0:
        return lead + f"of the {fa} {_s(fa, 'vote', 'votes')} cast, {_vs(f, _need(fa, pct))}."
    return lead + f"of the {fa} {_s(fa, 'vote', 'votes')} for and against, {_vs(f, _need(fa, pct))}. Of the {cast} {_s(cast, 'vote', 'votes')} cast, {_vs(f, _need(cast, pct))}."

def margin_truth(f, a):
    _tally(f, a, 0)
    lead = f"{f} for, {a} against: "
    if f == a:
        return lead + "tied, one vote changing sides decides it."
    hi, lo = (f, a) if f > a else (a, f)
    who = "for" if f > a else "against"
    diff = hi - lo
    lead = lead + f"{who} leads by {diff}. "
    if diff % 2 == 0:
        h = diff // 2
        return lead + f"{h} {_s(h, 'vote', 'votes')} changing sides would tie it, {h + 1} would reverse it."
    k = diff // 2 + 1
    if k == 1:
        return lead + "1 vote changing sides would reverse it."
    return (lead + f"{k} votes changing sides would reverse it ({k - 1} {_s(k - 1, 'vote', 'votes')} "
            f"would leave it {hi - (k - 1)} to {lo + (k - 1)}).")

FNS = {"quorumTruth": quorum_truth, "thresholdTruth": threshold_truth, "marginTruth": margin_truth}

CASES = [
    ("quorumTruth", [40, 25, 12]), ("quorumTruth", [40, 25, 10]), ("quorumTruth", [40, 25, 7]),
    ("quorumTruth", [1, 100, 1]), ("quorumTruth", [7, 50, 3]), ("quorumTruth", [40, 0, 12]),
    ("quorumTruth", [40, 25, 41]), ("quorumTruth", [0, 25, 0]),
    ("thresholdTruth", [14, 9, 3, 60]), ("thresholdTruth", [14, 9, 0, 60]),
    ("thresholdTruth", [20, 3, 2, 50]), ("thresholdTruth", [1, 0, 0, 100]),
    ("thresholdTruth", [14, 9, 3, 66.67]), ("thresholdTruth", [0, 0, 5, 50]),
    ("thresholdTruth", [14, -1, 3, 60]), ("thresholdTruth", [14, 9, 3, 101]),
    ("marginTruth", [14, 9]), ("marginTruth", [10, 10]), ("marginTruth", [12, 8]),
    ("marginTruth", [11, 10]), ("marginTruth", [9, 10]), ("marginTruth", [4, 6]),
    ("marginTruth", [3, 3.5]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
