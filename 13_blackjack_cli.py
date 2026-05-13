"""Simplified casino Blackjack vs dealer — closest to 21 without busting wins."""
from __future__ import annotations

import random
from typing import List, Tuple

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["♠", "♥", "♦", "♣"]


def fresh_deck() -> List[str]:
    deck: List[str] = []
    for s in SUITS:
        for r in RANKS:
            deck.append(f"{r}{s}")
    random.shuffle(deck)
    return deck


def hand_value(cards: List[str]) -> Tuple[int, bool]:
    total = 0
    aces = 0
    for c in cards:
        rank = c[:-1]
        if rank in ("J", "Q", "K", "10"):
            total += 10
        elif rank == "A":
            aces += 1
            total += 11
        else:
            total += int(rank)
    soft = aces > 0 and total <= 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
        soft = aces > 0 and total <= 21
    return total, soft


def draw(deck: List[str], hand: List[str], n: int = 1) -> None:
    for _ in range(n):
        if deck:
            hand.append(deck.pop())


def show(hand: List[str], hide_second: bool = False) -> str:
    if hide_second and len(hand) > 1:
        return " ".join(hand[:1]) + " [hidden]"
    return " ".join(hand)


def dealer_play(deck: List[str], hand: List[str]) -> None:
    while True:
        val, _ = hand_value(hand)
        if val >= 17:
            break
        draw(deck, hand, 1)


def main() -> None:
    print("=== CLI Blackjack (dealer stands on 17) ===")
    bank = 100
    while bank > 0:
        print(f"\nBankroll: ${bank}")
        bet_raw = input("Bet amount (0 to walk away): ").strip()
        try:
            bet = int(bet_raw)
        except ValueError:
            print("Numbers only.")
            continue
        if bet == 0:
            print("Cash out. Thanks!")
            break
        if bet < 0 or bet > bank:
            print("Invalid bet.")
            continue
        deck = fresh_deck()
        player: List[str] = []
        dealer: List[str] = []
        draw(deck, player, 2)
        draw(deck, dealer, 2)
        print("Your hand:", show(player))
        print("Dealer shows:", show(dealer, hide_second=True))
        if hand_value(player)[0] == 21:
            print("Blackjack!")
            bank += bet
            continue
        while True:
            val, _ = hand_value(player)
            if val > 21:
                print("Bust! You lose.")
                bank -= bet
                break
            act = input("Hit (h) or stand (s)? ").strip().lower()
            if act == "s":
                print("You stand at", val)
                print("Dealer reveals:", " ".join(dealer))
                dealer_play(deck, dealer)
                dv, _ = hand_value(dealer)
                print("Dealer total:", dv)
                pv, _ = hand_value(player)
                if dv > 21:
                    print("Dealer busts — you win!")
                    bank += bet
                elif pv > dv:
                    print("You win!")
                    bank += bet
                elif pv < dv:
                    print("Dealer wins.")
                    bank -= bet
                else:
                    print("Push — bet returned.")
                break
            elif act == "h":
                draw(deck, player, 1)
                print("Your hand:", show(player))
            else:
                print("Type h or s.")


if __name__ == "__main__":
    main()
