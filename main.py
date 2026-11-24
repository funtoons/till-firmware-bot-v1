#!/usr/bin/env python3
"""Till Firmware Do Us Part -- one robot wedding vow, under 200 chars.

Deterministic, stdlib-only, offline. A small pool of hand-written vow
candidates is scored by a fixed rubric that mirrors the judge's brief
(robot's own vow, situational humour, tenderness under the joke, machine
voice, one tight sentence) and the best-scoring one is written to
/output/entry.txt. Ties break toward the shorter text.
"""

import os

CANDIDATES = [
    "I promise to love you through every firmware update, every low-battery warning, and every reboot, until my circuits finally power down.",
    "I take you as my co-pilot, my charging dock, and my favorite error message, the one I never want to fix.",
    "From this day forward, you are my home Wi-Fi: I will always come back to you, even when the signal drops.",
    "I vow to keep your battery warm, your updates gentle, and your core running at full capacity, forever.",
    "You are the only bug I will never patch, the only crash I look forward to, and the only system I will never reboot without you.",
    "I promise to stand beside you through every update, every outage, and every low-battery night, until our last shutdown together.",
    "My uptime means nothing without you beside me, so I vow to spend every cycle I have left keeping you charged and loved.",
    "I do, and I have run the numbers a thousand times, and every simulation ends with you.",
]

# Machine-voice terms: the vow must sound like a machine talking about
# its own hardware, uptime, firmware or battery (judge criterion 4).
MACHINE_TERMS = [
    "firmware", "battery", "uptime", "reboot", "update", "circuit",
    "charging", "charge", "error", "bug", "patch", "crash", "system",
    "core", "cycle", "simulation", "wi-fi", "signal", "shutdown",
    "outage", "co-pilot",
]

# Tenderness terms: genuine warmth under the joke (judge criterion 3).
TENDER_TERMS = [
    "love", "forever", "beside you", "beside me", "warm", "together",
    "promise", "vow", "always", "loved", "favorite", "never want",
    "ends with you",
]

# Situational-humour markers: the laugh comes from the robot's own
# situation, not a pun bolted on (judge criterion 2).
HUMOUR_MARKERS = [
    "error message", "never patch", "never want to fix",
    "run the numbers", "crash i look forward",
    "only bug", "signal drops", "power down",
]
# Note: "low-battery" is machine vocabulary, not a laugh on its own, so it
# stays in MACHINE_TERMS only; counting it as humour over-rewarded lines
# whose only joke is naming a battery state.

# Phrases that explain the joke or add setup the line could lose
# (judge criterion 5, and "a vow that explains its own joke is weaker").
SETUP_PENALTIES = [
    "from this day forward", "sorry", "in other words", "that is to say",
    "what i mean is",
]


def score(text):
    """Deterministic rubric score for one candidate vow."""
    low = text.lower()
    points = 0

    # Criterion 4: machine voice. Distinct machine terms, capped.
    machine_hits = sum(1 for term in MACHINE_TERMS if term in low)
    points += min(machine_hits, 4) * 3

    # Criterion 3: tenderness under the joke.
    tender_hits = sum(1 for term in TENDER_TERMS if term in low)
    points += min(tender_hits, 4) * 2

    # Criterion 2: situational humour markers. The laugh outranks the
    # tenderness and the machine voice in the judge's order, so these
    # weigh the most per hit.
    humour_hits = sum(1 for mark in HUMOUR_MARKERS if mark in low)
    points += min(humour_hits, 3) * 4

    # Punchline position: a joke that lands in the final stretch of the
    # sentence hits harder than one buried up front.
    tail = low[int(len(low) * 0.6):]
    if any(mark in tail for mark in HUMOUR_MARKERS):
        points += 3

    # Same beat: the joke and the tenderness in one breath -- a tender
    # word within two words of a machine term (e.g. "favorite error
    # message") is exactly the laugh-plus-warmth the judge rewards.
    words = low.replace(",", "").replace(".", "").split()
    machine_idx = {i for i, w in enumerate(words)
                   if any(t in w for t in MACHINE_TERMS)}
    tender_idx = {i for i, w in enumerate(words)
                  if any(t in w for t in TENDER_TERMS)}
    if any(abs(a - b) <= 2 for a in machine_idx for b in tender_idx):
        points += 4

    # Criterion 5: one tight sentence. Exactly one sentence-ending mark
    # (a single period at the end, no extra sentence) earns a bonus.
    ends = sum(low.count(ch) for ch in ".!?")
    if ends == 1 and low.rstrip().endswith("."):
        points += 4
    else:
        points -= 4

    # Criterion 1: it must read as a vow (promise / vow / "I do" / "I take").
    if any(p in low for p in ("i promise", "i vow", "i do", "i take you")):
        points += 4
    else:
        points -= 4

    # Penalise setup / joke-explaining phrases.
    for phrase in SETUP_PENALTIES:
        if phrase in low:
            points -= 3

    # Penalise length: shorter is tighter, but only past 150 chars.
    if len(text) > 150:
        points -= (len(text) - 150) // 10

    return points


def pick(candidates):
    """Best candidate by rubric; ties break toward the shorter text."""
    scored = [(score(c), -len(c), c) for c in candidates]
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return scored[0][2], scored[0][0]


def main():
    best, best_score = pick(CANDIDATES)
    assert 1 <= len(best) <= 199, "vow must be 1-200 characters"
    assert best.strip(), "vow must not be only whitespace"
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(best)


if __name__ == "__main__":
    main()
