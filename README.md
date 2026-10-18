# Vote Math

Quorum, threshold and margin counting. The room is split, the bylaws say a percent, and someone has to count to the next whole person.

## What it computes

- **The quorum truth** - members and a quorum percent to the people who must be present, rounded up: 40 members at 25% need 10.
- **The threshold truth** - a tally against a required percent, on two bases side by side (for and against only, and all votes cast): enough by, exactly enough, or short by.
- **The margin truth** - how many votes changing sides would tie or reverse the result: 14 for, 9 against, 3 changing sides would reverse it.

## Boundary

Counting only. Vote Math works from the percents and tallies you type. It does not say what your bylaws require, whether a vote is valid, or how a meeting should be run. Your own rules decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the counting.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (23 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/votemath/
Repo: https://github.com/iLanis-agent/votemath
