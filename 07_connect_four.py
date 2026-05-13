"""Connect Four — drop discs into columns until four in a row."""
from __future__ import annotations

from typing import List, Optional

ROWS = 6
COLS = 7
EMPTY = "."


def new_board() -> List[List[str]]:
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board: List[List[str]]) -> None:
    print("  " + " ".join(str(c) for c in range(COLS)))
    for r in range(ROWS):
        print(str(r) + " " + " ".join(board[r][c] for c in range(COLS)))
    print()


def lowest_empty(board: List[List[str]], col: int) -> Optional[int]:
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def four_in_row(board: List[List[str]], sym: str) -> bool:
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                ok = True
                for k in range(1, 4):
                    nr, nc = r + dr * k, c + dc * k
                    if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                        ok = False
                        break
                    if board[nr][nc] != sym:
                        ok = False
                        break
                if ok:
                    return True
    return False


def full(board: List[List[str]]) -> bool:
    return all(board[0][c] != EMPTY for c in range(COLS))


def parse_col(s: str) -> Optional[int]:
    s = s.strip()
    if not s.isdigit():
        return None
    v = int(s)
    if 0 <= v < COLS:
        return v
    return None


def ai_move(board: List[List[str]], sym: str) -> int:
    opp = "O" if sym == "X" else "X"
    for c in range(COLS):
        r = lowest_empty(board, c)
        if r is None:
            continue
        board[r][c] = sym
        win = four_in_row(board, sym)
        board[r][c] = EMPTY
        if win:
            return c
    for c in range(COLS):
        r = lowest_empty(board, c)
        if r is None:
            continue
        board[r][c] = opp
        danger = four_in_row(board, opp)
        board[r][c] = EMPTY
        if danger:
            return c
    order = [3, 2, 4, 1, 5, 0, 6]
    for c in order:
        if lowest_empty(board, c) is not None:
            return c
    return 0


def main() -> None:
    print("Connect Four — you are X, CPU is O. Enter column 0-6.")
    board = new_board()
    human = True
    while True:
        print_board(board)
        if four_in_row(board, "O"):
            print("CPU wins.")
            break
        if four_in_row(board, "X"):
            print("You win!")
            break
        if full(board):
            print("Draw.")
            break
        if human:
            col = None
            while col is None:
                col = parse_col(input("Your column: "))
                if col is None:
                    print("Invalid column.")
                elif lowest_empty(board, col) is None:
                    print("Column full.")
                    col = None
            r = lowest_empty(board, col)
            assert r is not None
            board[r][col] = "X"
        else:
            c = ai_move(board, "O")
            r = lowest_empty(board, c)
            assert r is not None
            board[r][c] = "O"
            print(f"CPU plays column {c}.")
        human = not human


if __name__ == "__main__":
    main()
