import random

from poker import get_card_rank, print_card, twos_are_wild, get_best_hand


def simulate_hands(hand_size, num_hands):
    deck = range(52)

    for _ in range(num_hands):
        cards = random.sample(deck, hand_size)
        best_hand = get_best_hand(cards, is_wild_func=twos_are_wild)


if __name__ == '__main__':
    simulate_hands(10, 1)
