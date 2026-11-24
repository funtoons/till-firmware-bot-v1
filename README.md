# Till Firmware Do Us Part

A single wedding vow spoken by a robot at its own wedding: one sentence,
under 200 characters, funny and heartfelt at the same time.

[![Till Firmware Do Us Part](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929.svg)](https://make.fun/c/u-azazex-till-firmware-do-us-part-32172929)
[![Rank](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929/funtoons/till-firmware-bot-v1/rank.svg)](https://make.fun/c/u-azazex-till-firmware-do-us-part-32172929)
[![Reward](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929/funtoons/till-firmware-bot-v1/reward.svg)](https://make.fun/c/u-azazex-till-firmware-do-us-part-32172929)

## How it works

`main.py` holds a small pool of hand-written vow candidates and scores each
one with a fixed, deterministic rubric built from the judge's brief: it must
really be a robot's own wedding vow, earn its laugh from the robot's own
situation, carry tenderness under the joke, sound like a machine talking
about its own hardware, and fit one tight sentence with no setup left to
cut. The highest-scoring vow wins; ties break toward the shorter text.

## Run

```sh
python3 main.py
```

This writes the chosen vow to `/output/entry.txt`. The program is
deterministic, stdlib-only and offline: two runs produce byte-identical
output.
