from collections import Counter, defaultdict

import misc_helpers as mh


"""
Suit

Represent each suit as a number 0 through 3

0: clubs
1: diamonds
2: hearts
3: spades
"""

SUIT_NAMES = {0: 'clubs', 1: 'diamonds', 2: 'hearts', 3: 'spades'}

def suit_repr(suit):
    return SUIT_NAMES[suit]

def print_suit(suit):
    print(suit_repr)


"""
Card

Represent a card as a number 0 through 51

0: 2 of clubs
1: 3 of clubs
...
12: ace of clubs
13: 2 of diamonds
...

A card has a suit (clubs, ..., spades) and a rank (2, ..., 11 [jack], ..., 14 [ace])
"""

FACE_CARD_NAMES = {11: 'jack', 12: 'queen', 13: 'king', 14: 'ace'}

def get_card_suit(card):
    return card / 13

def get_card_rank(card):
    return (card % 13) + 2

def rank_repr(rank):
    return FACE_CARD_NAMES.get(rank, rank)

def card_repr(card):
    suit = get_card_suit(card)
    suit_display = suit_repr(suit)
    rank = get_card_rank(card)
    rank_display = rank_repr(rank)
    return '{} of {}'.format(rank_display, suit_display)

def print_card(card):
    print(card_repr(card))


"""
Wilds
"""

def twos_are_wild(card):
    return get_card_rank(card) == 2


"""
Poker Hand

Represent a poker hand with a tuple of (hand_type, tie_break_dict)

To compare two poker hands, take the highest hand_type, and break ties between
poker hands of the same hand_type using tie_break_dict

Order of hand_type's, along with their tie_break_dict parameters:
- high_card { rank: number }
- one_pair { rank: number }
- two_pair { high_rank: number, low_rank: number }
- three_of_a_kind { rank: number }
- straight { top_rank: number }
- flush { top_rank: number }
- full_house { triplet_rank: number, pair_rank: number }
- four_of_a_kind { rank: number }
- straight_flush { top_rank: number }

Each hand_type's finder takes in a non-empty list of cards and a number of
wilds, and returns a tuple of (found_hand: boolean, tie_break_dict)
"""

def high_card_finder(natural_cards, num_wilds=0):
    if num_wilds == 0:
        rank = max(get_card_rank(card) for card in natural_cards)
    elif num_wilds >= 1:
        rank = 14

    return True, { 'rank': rank }

def one_pair_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)

    if num_wilds == 0:
        pair_ranks = [rank for rank, count in rank_counts.items() if count >= 2]
    elif num_wilds == 1:
        pair_ranks = rank_counts.keys()
    elif num_wilds >= 2:
        pair_ranks = [14]

    if len(pair_ranks) == 0:
        return False, {}
    else:
        rank = max(pair_ranks)
        return True, { 'rank': rank }

def two_pair_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)
    pair_rank_counts = defaultdict(int)
    solo_rank_counts = defaultdict(int)
    for rank, count in rank_counts.items():
        if count >= 2:
            pair_rank_counts[rank] = count / 2
        if count % 2 == 1:
            solo_rank_counts[rank] = count % 2

    num_wilds_left = num_wilds
    while num_wilds_left >= 1:
        # if we already have a pair, and we have 2 wilds, use them to make a
        # pair of aces
        if sum(pair_rank_counts.values()) >= 1 and num_wilds_left >= 2:
            pair_rank_counts[14] += 1
            num_wilds_left -= 2
        # if we have 4 wilds, use them to make 2 pairs of aces
        elif num_wilds_left >= 4:
            pair_rank_counts[14] += 2
            num_wilds_left -= 4
        # otherwise, pair a wild with the highest remaining solo rank
        elif sum(solo_rank_counts.values()) >= 1:
            pair_with_wild_rank = max(solo_rank_counts.keys())
            num_wilds_left -= 1
            pair_rank_counts[pair_with_wild_rank] += 1
            mh.decrementCounter(solo_rank_counts, pair_with_wild_rank, 1)
        else:
            break

    if sum(pair_rank_counts.values()) < 2:
        return False, {}
    else:
        high_rank = max(
            rank for rank, count in pair_rank_counts.items() if count >= 1
        )
        mh.decrementCounter(pair_rank_counts, high_rank, 1)
        low_rank = max(
            rank for rank, count in pair_rank_counts.items() if count >= 1
        )
        return True, { 'high_rank': high_rank, 'low_rank': low_rank }

def three_of_a_kind_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)
    solo_ranks = set(rank for rank, count in rank_counts.items() if count >= 1)
    pair_ranks = set(rank for rank, count in rank_counts.items() if count >= 2)
    triplet_ranks = set(
        rank
        for rank, count in rank_counts.items()
        if count >= 3
    )

    if num_wilds == 0:
        triplet_ranks = triplet_ranks
    elif num_wilds == 1:
        triplet_ranks = triplet_ranks | pair_ranks
    elif num_wilds == 2:
        triplet_ranks = triplet_ranks | pair_ranks | solo_ranks
    elif num_wilds >= 3:
        triplet_ranks = [14]

    if len(triplet_ranks) == 0:
        return False, {}
    else:
        rank = max(triplet_ranks)
        return True, { 'rank': rank }

def straight_finder(natural_cards, num_wilds=0):
    ranks = set(get_card_rank(card) for card in natural_cards)
    missing_ranks = sorted(rank for rank in range(2, 15) if rank not in ranks)
    missing_ranks = [1] + missing_ranks + [15]
    straight_top_ranks = [
        missing_ranks[i]-1
        for i in range(len(missing_ranks)-1, 0, -1)
        if (missing_ranks[i] - missing_ranks[i-1]) > 5
    ]
    if len(straight_top_ranks) == 0:
        return False, {}
    else:
        top_rank = max(straight_top_ranks)
        return True, { 'top_rank': top_rank }

def flush_finder(natural_cards, num_wilds=0):
    suit_counts = Counter(get_card_suit(card) for card in natural_cards)
    flush_suits = set(suit for suit, count in suit_counts.items() if count >= 5)
    if len(flush_suits) == 0:
        return False, {}
    else:
        flush_ranks = [
            get_card_rank(card)
            for card in natural_cards
            if get_card_suit(card) in flush_suits
        ]
        top_rank = max(flush_ranks)
        return True, { 'top_rank': top_rank }

def full_house_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)
    triplet_ranks = set(
        rank
        for rank, count in rank_counts.items()
        if count >= 3
    )
    pair_ranks = set(rank for rank, count in rank_counts.items() if count >= 2)
    if len(triplet_ranks) == 0 or len(pair_ranks) < 2:
        return False, {}
    else:
        triplet_rank = max(triplet_ranks)
        pair_ranks.remove(triplet_rank)
        pair_rank = max(pair_ranks)
        return True, { 'triplet_rank': triplet_rank, 'pair_rank': pair_rank }

def four_of_a_kind_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)
    quartet_ranks = set(
        rank
        for rank, count in rank_counts.items()
        if count >= 4
    )
    if len(quartet_ranks) == 0:
        return False, {}
    else:
        rank = max(quartet_ranks)
        return True, { 'rank': rank }

def straight_flush_finder(natural_cards, num_wilds=0):
    cards_by_suit = [
        [card for card in natural_cards if get_card_suit(card) == suit]
        for suit in range(4)
    ]
    tie_break_dicts = [
        straight_finder(suit_cards, num_wilds=num_wilds)[1]
        for suit_cards in cards_by_suit
    ]
    straight_flush_top_ranks = [
        tie_break_dict['top_rank']
        for tie_break_dict in tie_break_dicts
        if 'top_rank' in tie_break_dict
    ]
    if len(straight_flush_top_ranks) == 0:
        return False, {}
    else:
        top_rank = max(straight_flush_top_ranks)
        return True, { 'top_rank': top_rank }

HAND_TYPES = [
    { 'hand_type': 'high_card',       'finder': high_card_finder },
    { 'hand_type': 'one_pair',        'finder': one_pair_finder },
    { 'hand_type': 'two_pair',        'finder': two_pair_finder },
    { 'hand_type': 'three_of_a_kind', 'finder': three_of_a_kind_finder },
    { 'hand_type': 'straight',        'finder': straight_finder },
    { 'hand_type': 'flush',           'finder': flush_finder },
    { 'hand_type': 'full_house',      'finder': full_house_finder },
    { 'hand_type': 'four_of_a_kind',  'finder': four_of_a_kind_finder },
    { 'hand_type': 'straight_flush',  'finder': straight_flush_finder },
]

def get_best_hand(cards, is_wild_func):
    num_wilds = sum(1 for card in cards if is_wild_func(card))
    natural_cards = [card for card in cards if not is_wild_func(card)]
    for hand_type_obj in HAND_TYPES[::-1]:
        hand_type = hand_type_obj['hand_type']
        hand_type_finder = hand_type_obj['finder']
        found_hand, tie_break_dict = hand_type_finder(
            natural_cards,
            num_wilds=num_wilds
        )
        if found_hand:
            return hand_type, tie_break_dict
