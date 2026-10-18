// Vote Math engine - quorum, threshold and margin counting from owner-entered rules.
// Mirrored by oracle.py; keep the op order identical.

function _int(x, lo, hi, msg) {
  if (!isFinite(x) || x % 1 !== 0 || x < lo || x > hi) throw new Error(msg);
}

function _num(x) {
  return String(x);
}

function _pct(p) {
  if (!isFinite(p) || p <= 0 || p > 100) throw new Error("required percent must be over 0 and at most 100");
}

function _need(base, pct) {
  return Math.ceil(base * pct / 100 - 1e-9);
}

function _s(n, one, many) {
  return n === 1 ? one : many;
}

// The quorum truth: how many must be present under a percent the owner enters.
function quorumTruth(members, pct, present) {
  _int(members, 1, 100000, "members must be a whole number from 1 to 100000");
  _pct(pct);
  _int(present, 0, members, "present must be a whole number from 0 up to the member count");
  var need = _need(members, pct);
  var diff = present - need;
  var tail = diff > 0 ? "over by " + diff : diff === 0 ? "exactly enough" : "short by " + (-diff);
  return members + " " + _s(members, "member", "members") + ", quorum " + _num(pct) + "%: " + need + " must be present. " + present + " present: " + tail + ".";
}

function _tally(f, a, ab) {
  _int(f, 0, 1000000, "votes must be whole numbers, 0 or more");
  _int(a, 0, 1000000, "votes must be whole numbers, 0 or more");
  _int(ab, 0, 1000000, "votes must be whole numbers, 0 or more");
}

function _vs(f, need) {
  var d = f - need;
  var t = d > 0 ? "enough by " + d : d === 0 ? "exactly enough" : "short by " + (-d);
  return need + " " + (need === 1 ? "is" : "are") + " needed, " + t;
}

// The threshold truth: the same tally against a percent, on two bases.
function thresholdTruth(f, a, ab, pct) {
  _tally(f, a, ab);
  _pct(pct);
  var fa = f + a, cast = f + a + ab;
  if (fa <= 0) throw new Error("enter at least one vote for or against");
  var lead = "For " + f + ", against " + a + ", abstain " + ab + ". Required " + _num(pct) + "%: ";
  if (ab === 0) return lead + "of the " + fa + " " + _s(fa, "vote", "votes") + " cast, " + _vs(f, _need(fa, pct)) + ".";
  return lead + "of the " + fa + " " + _s(fa, "vote", "votes") + " for and against, " + _vs(f, _need(fa, pct)) + ". Of the " + cast + " " + _s(cast, "vote", "votes") + " cast, " +
    _vs(f, _need(cast, pct)) + ".";
}

// The margin truth: how many votes changing sides would turn the result.
function marginTruth(f, a) {
  _tally(f, a, 0);
  var lead = f + " for, " + a + " against: ";
  if (f === a) return lead + "tied, one vote changing sides decides it.";
  var hi = f > a ? f : a;
  var lo = f > a ? a : f;
  var who = f > a ? "for" : "against";
  var diff = hi - lo;
  lead = lead + who + " leads by " + diff + ". ";
  if (diff % 2 === 0) {
    var h = diff / 2;
    return lead + h + " " + _s(h, "vote", "votes") + " changing sides would tie it, " + (h + 1) + " would reverse it.";
  }
  var k = Math.floor(diff / 2) + 1;
  if (k === 1) return lead + "1 vote changing sides would reverse it.";
  return lead + k + " votes changing sides would reverse it (" + (k - 1) + " " + _s(k - 1, "vote", "votes") +
    " would leave it " + (hi - (k - 1)) + " to " + (lo + (k - 1)) + ").";
}
