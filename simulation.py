import random

from poker import (
    get_card_rank,
    print_card,
    twos_are_wild,
    get_best_hand,
    get_hand_sortkey
)


def simulate_hands(hand_size, num_trials):
    deck = range(52)

    best_hands = []
    for _ in range(num_trials):
        cards = random.sample(deck, hand_size)
        best_hand = get_best_hand(cards, is_wild_func=twos_are_wild)
        best_hands.append(best_hand)

    return best_hands

def generate_hand_size_median_hands_csv(num_trials):
    for hand_size in range(2, 29):
        best_hands = simulate_hands(hand_size, num_trials)
        sorted_best_hands = sorted(
            best_hands,
            key=lambda hand: get_hand_sortkey(*hand)
        )
        print(hand_size, sorted_best_hands[len(sorted_best_hands)/2])


if __name__ == '__main__':
    generate_hand_size_median_hands_csv(10000)
