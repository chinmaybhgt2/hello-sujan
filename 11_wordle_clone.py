"""Six guesses to find a secret five-letter word — Wordle-style feedback."""
from __future__ import annotations

import random
from typing import List

WORD_BANK = [
    "apple",
    "brave",
    "crane",
    "delta",
    "eagle",
    "flame",
    "grape",
    "house",
    "ivory",
    "jolly",
    "knead",
    "lemon",
    "mango",
    "noble",
    "ocean",
    "piano",
    "query",
    "roast",
    "sunny",
    "tiger",
    "ultra",
    "vivid",
    "whale",
    "xenon",
    "yacht",
    "zebra",
]


def pick_word() -> str:
    return random.choice(WORD_BANK)


def score_guess(secret: str, guess: str) -> List[str]:
    result = ["_"] * 5
    sec = list(secret)
    gue = list(guess)
    for i in range(5):
        if gue[i] == sec[i]:
            result[i] = "G"
            sec[i] = gue[i] = " "
    for i in range(5):
        if gue[i] == " ":
            continue
        if gue[i] in sec:
            result[i] = "Y"
            idx = sec.index(gue[i])
            sec[idx] = " "
        else:
            result[i] = "X"
    return result


def explain() -> None:
    print("G = green (right letter, right spot)")
    print("Y = yellow (letter exists, wrong spot)")
    print("X = gray (letter not in word today)")
    print("Think of it like Mastermind, but with English words instead of colored pegs.")


def valid_guess(raw: str) -> bool:
    w = raw.strip().lower()
    return len(w) == 5 and w.isalpha()


def show_lexicon_hint() -> None:
    sample = ", ".join(WORD_BANK[:8])
    print(f"Example words in rotation: {sample}, …")


def main() -> None:
    secret = pick_word()
    print("=== Mini Wordle (5 letters, 6 guesses) ===")
    explain()
    show_lexicon_hint()
    for attempt in range(1, 7):
        guess = ""
        while not valid_guess(guess):
            guess = input(f"Guess {attempt}/6: ").strip().lower()
            if not valid_guess(guess):
                print("Need exactly five letters A-Z.")
        pattern = score_guess(secret, guess)
        print(" ".join(pattern))
        print(" ".join(list(guess)))
        if guess == secret:
            print(f"Solved in {attempt} tries!")
            return
    print(f"Nice try — the word was: {secret}")


if __name__ == "__main__":
    main()
    # Self-contained mini clone — no network calls, runs offline anywhere.
