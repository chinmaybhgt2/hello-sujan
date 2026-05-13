"""One-player Battleship on a 5x5 ocean — find a length-3 ship in limited shots."""
from __future__ import annotations

import random
from typing import List, Set, Tuple

SIZE = 5
SHIP_LEN = 3
MAX_SHOTS = 12


def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def random_ship() -> Set[Tuple[int, int]]:
    horizontal = random.choice([True, False])
    if horizontal:
        r = random.randint(0, SIZE - 1)
        c0 = random.randint(0, SIZE - SHIP_LEN)
        return {(r, c0 + k) for k in range(SHIP_LEN)}
    c = random.randint(0, SIZE - 1)
    r0 = random.randint(0, SIZE - SHIP_LEN)
    return {(r0 + k, c) for k in range(SHIP_LEN)}


def parse_shot(s: str) -> Tuple[int, int] | None:
    s = s.strip().lower()
    if len(s) < 2:
        return None
    if s[0].isalpha() and s[1:].isdigit():
        r = ord(s[0]) - ord("a")
        c = int(s[1:]) - 1
        if 0 <= r < SIZE and 0 <= c < SIZE:
            return r, c
    parts = s.replace(",", " ").split()
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        r, c = int(parts[0]), int(parts[1])
        if 0 <= r < SIZE and 0 <= c < SIZE:
            return r, c
    return None


def render(
    hits: Set[Tuple[int, int]],
    misses: Set[Tuple[int, int]],
    reveal: bool,
    ship: Set[Tuple[int, int]],
) -> None:
    print("    " + " ".join(str(c + 1) for c in range(SIZE)))
    for r in range(SIZE):
        row: List[str] = []
        for c in range(SIZE):
            if (r, c) in hits:
                row.append("X")
            elif (r, c) in misses:
                row.append("o")
            elif reveal and (r, c) in ship:
                row.append("S")
            else:
                row.append(".")
        print(f" {chr(ord('a')+r)}  " + " ".join(row))


def main() -> None:
    print("Battleship: one hidden straight ship of length 3 on 5x5.")
    print(f"You have {MAX_SHOTS} torpedoes. Coordinates like a1 or 0 0.")
    ship = random_ship()
    hits: Set[Tuple[int, int]] = set()
    misses: Set[Tuple[int, int]] = set()
    shots = 0
    while shots < MAX_SHOTS and len(hits) < SHIP_LEN:
        render(hits, misses, False, ship)
        cell = None
        while cell is None:
            cell = parse_shot(input("Target: "))
            if cell is None:
                print("Invalid coordinate.")
            elif cell in hits or cell in misses:
                print("Already fired there.")
                cell = None
        shots += 1
        if cell in ship:
            hits.add(cell)
            print("HIT!")
        else:
            misses.add(cell)
            print("Splash — miss.")
            near = min(manhattan(cell, s) for s in ship)
            if near <= 1:
                print("Sonar ping: something metal is VERY close.")
            elif near == 2:
                print("Sonar ping: heat signature nearby.")
        print(f"Shots used: {shots}/{MAX_SHOTS}")
    render(hits, misses, True, ship)
    if len(hits) == SHIP_LEN:
        print("You sank my battleship!")
    else:
        print("Out of ammo. Ship escaped this time.")


if __name__ == "__main__":
    main()
