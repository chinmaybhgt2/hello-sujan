"""Timed trivia sprint — answer multiple-choice questions as fast as you can."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Tuple

QUESTIONS: List[Tuple[str, List[str], int]] = [
    ("Capital of France?", ["London", "Paris", "Berlin", "Madrid"], 1),
    ("2 ** 10 equals?", ["512", "1024", "2048", "256"], 1),
    ("Planet known as the Red Planet?", ["Venus", "Mars", "Jupiter", "Saturn"], 1),
    ("Speed of light symbol?", ["v", "c", "s", "l"], 1),
    ("HTML means?", [
        "Hyper Text Markup Language",
        "High Transfer Main Link",
        "Home Tool Markup Line",
        "Hyperlink Text Mode Layer",
    ], 0),
    ("Which gas do plants absorb?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Helium"], 2),
    ("Largest ocean?", ["Atlantic", "Indian", "Arctic", "Pacific"], 3),
    ("How many sides on a hexagon?", ["5", "6", "7", "8"], 1),
    ("Water boils at sea level (°C)?", ["90", "100", "120", "80"], 1),
    ("Python is a type of …?", ["Snake only", "Programming language", "CPU", "Browser"], 1),
    ("Smallest prime number?", ["0", "1", "2", "3"], 2),
    ("HTTP status for 'Not Found'?", ["200", "301", "404", "500"], 2),
    ("CPU stands for?", [
        "Central Processing Unit",
        "Computer Personal Utility",
        "Cached Program Upload",
        "Control Panel Utility",
    ], 0),
    ("Which company makes Windows?", ["Apple", "Google", "Microsoft", "IBM"], 2),
]


@dataclass
class Stats:
    correct: int = 0
    wrong: int = 0
    elapsed: float = 0.0


def ask_all() -> Stats:
    stats = Stats()
    start = time.perf_counter()
    for i, (q, opts, ans) in enumerate(QUESTIONS, start=1):
        print(f"\nQ{i}/{len(QUESTIONS)}: {q}")
        for j, text in enumerate(opts):
            label = chr(ord("A") + j)
            print(f"  {label}) {text}")
        pick = None
        while pick is None:
            raw = input("Answer (letter): ").strip().upper()
            if len(raw) == 1 and "A" <= raw <= chr(ord("A") + len(opts) - 1):
                pick = ord(raw) - ord("A")
            else:
                print("Choose a valid letter.")
        if pick == ans:
            print("Correct!")
            stats.correct += 1
        else:
            right = chr(ord("A") + ans)
            print(f"Wrong — answer was {right}.")
            stats.wrong += 1
    stats.elapsed = time.perf_counter() - start
    return stats


def grade(stats: Stats) -> str:
    total = stats.correct + stats.wrong
    acc = stats.correct / max(1, total)
    if acc == 1.0 and stats.elapsed < 55:
        return "Lightning brain — perfect rush!"
    if acc == 1.0:
        return "Perfect score — steady wins the race."
    if acc >= 0.85:
        return "Strong trivia instincts."
    if acc >= 0.55:
        return "Room to grow — read a fun facts book."
    return "Every expert was once a beginner — play again."


def recap(stats: Stats) -> None:
    avg = stats.elapsed / max(1, stats.correct + stats.wrong)
    print(f"Average time per question: {avg:.1f}s")


def main() -> None:
    print("=== Trivia Rush ===")
    print("Answer A/B/C/D quickly. Your clock stops after the last question.")
    input("Press Enter to start…")
    stats = ask_all()
    print(f"\nScore: {stats.correct} correct, {stats.wrong} wrong.")
    print(f"Time: {stats.elapsed:.1f} seconds.")
    recap(stats)
    print(grade(stats))


if __name__ == "__main__":
    main()
