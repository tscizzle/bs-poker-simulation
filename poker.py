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

Each hand_type's sortkey_func takes in a tie_break_dict, and returns a float
from 0 through 9, each half-open interval [n, n+1) represnting the range for a
single hand_type. For example, any number 5.xyz represents a flush.
"""

## FINDERS

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
            solo_rank_counts[rank] = 1

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

    straight_top_ranks = []
    for top_rank in range(14, 4, -1):
        missing_ranks = set(range(top_rank-4, top_rank+1)) - ranks
        if len(missing_ranks) <= num_wilds:
            straight_top_ranks.append(top_rank)

    if len(straight_top_ranks) == 0:
        return False, {}
    else:
        top_rank = max(straight_top_ranks)
        return True, { 'top_rank': top_rank }

def flush_finder(natural_cards, num_wilds=0):
    suit_counts = Counter(get_card_suit(card) for card in natural_cards)

    wilds_needed = 5 - max(suit_counts.values() + [0])
    found_flush = num_wilds >= wilds_needed

    if not found_flush:
        return False, {}
    else:
        if num_wilds == 0:
            flush_suits = set(
                suit
                for suit, count in suit_counts.items()
                if count >= 5
            )
            flush_ranks = [
                get_card_rank(card)
                for card in natural_cards
                if get_card_suit(card) in flush_suits
            ]
            top_rank = max(flush_ranks)
        elif num_wilds >= 1:
            top_rank = 14

        return True, { 'top_rank': top_rank }

def full_house_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)
    triplet_rank_counts = defaultdict(int)
    pair_rank_counts = defaultdict(int)
    solo_rank_counts = defaultdict(int)
    for rank, count in rank_counts.items():
        if count >= 3:
            triplet_rank_counts[rank] = count / 3
        if count % 3 == 2:
            pair_rank_counts[rank] = 1
        if count % 3 == 1:
            solo_rank_counts[rank] = 1

    if num_wilds == 0:
        enough_triplets = len(triplet_rank_counts) >= 1
        enough_pairs = len(triplet_rank_counts) + len(pair_rank_counts) >= 2
        if not enough_triplets or not enough_pairs:
            return False, {}
        else:
            triplet_rank = max(triplet_rank_counts.keys())
            mh.decrementCounter(triplet_rank_counts, triplet_rank, 1)
            pair_rank = max(
                triplet_rank_counts.keys() + pair_rank_counts.keys()
            )
            return True, {
                'triplet_rank': triplet_rank,
                'pair_rank': pair_rank,
            }
    # TODO: this recursive technique is the most time consuming part of all the
    #       hand finders. instead of recursing, directly handle each case of
    #       num_wilds / rank_counts
    elif num_wilds == 1 or num_wilds == 2:
        candidates = [
            full_house_finder(natural_cards + [card], num_wilds=num_wilds-1)
            for card in range(13)
        ]
        candidate_tie_break_dicts = [
            tie_break_dict
            for found_full_house, tie_break_dict in candidates
            if found_full_house
        ]
        if len(candidate_tie_break_dicts) == 0:
            return False, {}
        else:
            best_tie_break_dict = { 'triplet_rank': -1, 'pair_rank': -1 }
            for tie_break_dict in candidate_tie_break_dicts:
                better_triplet_rank = (
                    tie_break_dict['triplet_rank'] >
                    best_tie_break_dict['triplet_rank']
                )
                same_triplet_rank = (
                    tie_break_dict['triplet_rank'] ==
                    best_tie_break_dict['triplet_rank']
                )
                better_pair_rank = (
                    tie_break_dict['pair_rank'] >
                    best_tie_break_dict['pair_rank']
                )
                if (
                    better_triplet_rank or
                    (same_triplet_rank and better_pair_rank)
                ):
                    best_tie_break_dict = tie_break_dict
            return True, best_tie_break_dict
    elif num_wilds == 3:
        if len(triplet_rank_counts) + len(pair_rank_counts) == 0:
            return False, {}
        else:
            pair_rank = max(
                triplet_rank_counts.keys() + pair_rank_counts.keys()
            )
            return True, { 'triplet_rank': 14, 'pair_rank': pair_rank }
    elif num_wilds == 4:
        if len(natural_cards) == 0:
            return False, {}
        else:
            pair_rank = max(rank_counts.keys())
            return True, { 'triplet_rank': 14, 'pair_rank': pair_rank }
    elif num_wilds >= 5:
        return True, { 'triplet_rank': 14, 'pair_rank': 14 }

def four_of_a_kind_finder(natural_cards, num_wilds=0):
    rank_counts = Counter(get_card_rank(card) for card in natural_cards)
    solo_ranks = set(rank for rank, count in rank_counts.items() if count >= 1)
    pair_ranks = set(rank for rank, count in rank_counts.items() if count >= 2)
    triplet_ranks = set(
        rank
        for rank, count in rank_counts.items()
        if count >= 3
    )
    quartet_ranks = set(
        rank
        for rank, count in rank_counts.items()
        if count >= 4
    )

    if num_wilds == 0:
        quartet_ranks = quartet_ranks
    elif num_wilds == 1:
        quartet_ranks = quartet_ranks | triplet_ranks
    elif num_wilds == 2:
        quartet_ranks = quartet_ranks | triplet_ranks | pair_ranks
    elif num_wilds == 3:
        quartet_ranks = quartet_ranks | triplet_ranks | pair_ranks | solo_ranks
    elif num_wilds >= 4:
        quartet_ranks = [14]

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

## SORTKEY FUNCS

NUM_RANKS = 14.0

def high_card_sortkey_func(tie_break_dict):
    rank = tie_break_dict['rank']
    tie_break_val = rank / NUM_RANKS
    return 0 + (tie_break_val * 0.95)

def one_pair_sortkey_func(tie_break_dict):
    rank = tie_break_dict['rank']
    tie_break_val = rank / NUM_RANKS
    return 1 + (tie_break_val * 0.95)

def two_pair_sortkey_func(tie_break_dict):
    high_rank = tie_break_dict['high_rank']
    low_rank = tie_break_dict['low_rank']
    tie_break_val = ((high_rank * NUM_RANKS) + low_rank) / ((NUM_RANKS + 1)**2)
    return 2 + (tie_break_val * 0.95)

def three_of_a_kind_sortkey_func(tie_break_dict):
    rank = tie_break_dict['rank']
    tie_break_val = rank / NUM_RANKS
    return 3 + (tie_break_val * 0.95)

def straight_sortkey_func(tie_break_dict):
    top_rank = tie_break_dict['top_rank']
    tie_break_val = top_rank / NUM_RANKS
    return 4 + (tie_break_val * 0.95)

def flush_sortkey_func(tie_break_dict):
    top_rank = tie_break_dict['top_rank']
    tie_break_val = top_rank / NUM_RANKS
    return 5 + (tie_break_val * 0.95)

def full_house_sortkey_func(tie_break_dict):
    triplet_rank = tie_break_dict['triplet_rank']
    pair_rank = tie_break_dict['pair_rank']
    tie_break_val = (
        ((triplet_rank * NUM_RANKS) + pair_rank) /
        ((NUM_RANKS + 1)**2)
    )
    return 6 + (tie_break_val * 0.95)

def four_of_a_kind_sortkey_func(tie_break_dict):
    rank = tie_break_dict['rank']
    tie_break_val = rank / NUM_RANKS
    return 7 + (tie_break_val * 0.95)

def straight_flush_sortkey_func(tie_break_dict):
    top_rank = tie_break_dict['top_rank']
    tie_break_val = top_rank / NUM_RANKS
    return 8 + (tie_break_val * 0.95)


## PUTTING IT ALL TOGETHER

HAND_TYPES = [
    {
        'hand_type': 'high_card',
        'finder': high_card_finder,
        'sortkey_func': high_card_sortkey_func,
    },
    {
        'hand_type': 'one_pair',
        'finder': one_pair_finder,
        'sortkey_func': one_pair_sortkey_func,
    },
    {
        'hand_type': 'two_pair',
        'finder': two_pair_finder,
        'sortkey_func': two_pair_sortkey_func,
    },
    {
        'hand_type': 'three_of_a_kind',
        'finder': three_of_a_kind_finder,
        'sortkey_func': three_of_a_kind_sortkey_func,
    },
    {
        'hand_type': 'straight',
        'finder': straight_finder,
        'sortkey_func': straight_sortkey_func,
    },
    {
        'hand_type': 'flush',
        'finder': flush_finder,
        'sortkey_func': flush_sortkey_func,
    },
    {
        'hand_type': 'full_house',
        'finder': full_house_finder,
        'sortkey_func': full_house_sortkey_func,
    },
    {
        'hand_type': 'four_of_a_kind',
        'finder': four_of_a_kind_finder,
        'sortkey_func': four_of_a_kind_sortkey_func,
    },
    {
        'hand_type': 'straight_flush',
        'finder': straight_flush_finder,
        'sortkey_func': straight_flush_sortkey_func,
    },
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

def get_hand_sortkey(hand_type, tie_break_dict):
    hand_type_obj = [o for o in HAND_TYPES if o['hand_type'] == hand_type][0]
    sortkey_func = hand_type_obj['sortkey_func']
    sortkey = sortkey_func(tie_break_dict)
    return sortkey
