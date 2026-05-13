"""Console memory: flip two positions to find matching pairs of letters."""
from __future__ import annotations

import random
from typing import List, Optional, Tuple

SIZE = 4
PAIR_COUNT = (SIZE * SIZE) // 2


def build_deck() -> List[str]:
    letters = [chr(65 + i) for i in range(PAIR_COUNT)]
    deck = letters + letters
    random.shuffle(deck)
    return deck


def idx_to_rc(i: int) -> Tuple[int, int]:
    return i // SIZE, i % SIZE


def format_coord(idx: int) -> str:
    r, c = idx_to_rc(idx)
    return f"{chr(ord('a') + r)}{c + 1}"


def parse_cell(s: str) -> Optional[int]:
    s = s.strip().lower()
    if not s:
        return None
    if s[0] in "abcdefgh" and len(s) >= 2 and s[1].isdigit():
        r = ord(s[0]) - ord("a")
        c = int(s[1]) - 1
        if 0 <= r < SIZE and 0 <= c < SIZE:
            return r * SIZE + c
    parts = s.replace(",", " ").split()
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        r, c = int(parts[0]), int(parts[1])
        if 0 <= r < SIZE and 0 <= c < SIZE:
            return r * SIZE + c
    return None


def render(deck: List[str], shown: List[bool]) -> None:
    print("    " + " ".join(str(c + 1) for c in range(SIZE)))
    for r in range(SIZE):
        row = [deck[r * SIZE + c] if shown[r * SIZE + c] else "#" for c in range(SIZE)]
        print(f" {chr(ord('a')+r)}  " + " ".join(row))


def main() -> None:
    print("Memory pairs on a 4x4 grid. Use 'a1' style or 'row col' (0-3).")
    print("Goal: clear the board in as few turns as possible — like flipping diner placemats.")
    deck = build_deck()
    shown = [False] * (SIZE * SIZE)
    matches = 0
    turns = 0
    while matches < PAIR_COUNT:
        render(deck, shown)
        first = None
        while first is None:
            first = parse_cell(input("First cell: "))
            if first is None:
                print("Invalid cell.")
            elif shown[first]:
                print("Already revealed.")
                first = None
        shown[first] = True
        render(deck, shown)
        second = None
        while second is None or second == first:
            second = parse_cell(input("Second cell: "))
            if second is None:
                print("Invalid cell.")
            elif second is not None and shown[second]:
                print("Already revealed.")
                second = None
            elif second == first:
                print("Pick a different cell.")
                second = None
        shown[second] = True
        turns += 1
        render(deck, shown)
        if deck[first] == deck[second]:
            matches += 1
            print(f"Match on {format_coord(first)} and {format_coord(second)}!")
        else:
            print(
                f"No match ({format_coord(first)}={deck[first]}, "
                f"{format_coord(second)}={deck[second]}) — hiding again."
            )
            shown[first] = False
            shown[second] = False
    par = PAIR_COUNT + 2
    quality = "sharp memory!" if turns <= par else "good focus — try for fewer turns next time."
    print(f"You cleared the board in {turns} turns ({quality})")


if __name__ == "__main__":
    main()
