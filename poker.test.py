import poker
import card_names as cn

import unittest


class TestPoker(unittest.TestCase):
    def test_high_card_finder(self):
        six_high_hand = [
            cn.THREE_OF_CLUBS,
            cn.FIVE_OF_DIAMONDS,
            cn.SIX_OF_DIAMONDS,
        ]
        self.assertEqual(
            poker.high_card_finder(six_high_hand, num_wilds=0),
            (True, { 'rank': 6 })
        )
        self.assertEqual(
            poker.high_card_finder(six_high_hand, num_wilds=1),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.high_card_finder(six_high_hand, num_wilds=2),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.high_card_finder(six_high_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.high_card_finder(six_high_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

    def test_one_pair_finder(self):
        five_high_hand = [
            cn.FOUR_OF_HEARTS,
            cn.FIVE_OF_HEARTS,
            cn.TWO_OF_SPADES,
            cn.THREE_OF_SPADES,
        ]
        self.assertEqual(
            poker.one_pair_finder(five_high_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.one_pair_finder(five_high_hand, num_wilds=1),
            (True, { 'rank': 5 })
        )
        self.assertEqual(
            poker.one_pair_finder(five_high_hand, num_wilds=2),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.one_pair_finder(five_high_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.one_pair_finder(five_high_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )

        pair_of_fours_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.THREE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.one_pair_finder(pair_of_fours_hand, num_wilds=0),
            (True, { 'rank': 4 })
        )
        self.assertEqual(
            poker.one_pair_finder(pair_of_fours_hand, num_wilds=1),
            (True, { 'rank': 7 })
        )
        self.assertEqual(
            poker.one_pair_finder(pair_of_fours_hand, num_wilds=2),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.one_pair_finder(pair_of_fours_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.one_pair_finder(pair_of_fours_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

    def test_two_pair_finder(self):
        five_high_hand = [
            cn.FOUR_OF_HEARTS,
            cn.FIVE_OF_HEARTS,
            cn.TWO_OF_SPADES,
            cn.THREE_OF_SPADES,
        ]
        self.assertEqual(
            poker.two_pair_finder(five_high_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.two_pair_finder(five_high_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.two_pair_finder(five_high_hand, num_wilds=2),
            (True, { 'high_rank': 5, 'low_rank': 4 })
        )
        self.assertEqual(
            poker.two_pair_finder(five_high_hand, num_wilds=3),
            (True, { 'high_rank': 14, 'low_rank': 5 })
        )
        self.assertEqual(
            poker.two_pair_finder(five_high_hand, num_wilds=4),
            (True, { 'high_rank': 14, 'low_rank': 14 })
        )

        pair_of_fours_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_hand, num_wilds=1),
            (True, { 'high_rank': 7, 'low_rank': 4 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_hand, num_wilds=2),
            (True, { 'high_rank': 14, 'low_rank': 4 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_hand, num_wilds=3),
            (True, { 'high_rank': 14, 'low_rank': 7 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_hand, num_wilds=4),
            (True, { 'high_rank': 14, 'low_rank': 14 })
        )

        pair_of_fours_and_sevens_hand = [
            cn.THREE_OF_HEARTS,
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FOUR_OF_SPADES,
            cn.SEVEN_OF_SPADES,
            cn.NINE_OF_SPADES,
        ]
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_and_sevens_hand, num_wilds=0),
            (True, { 'high_rank': 7, 'low_rank': 4 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_and_sevens_hand, num_wilds=1),
            (True, { 'high_rank': 9, 'low_rank': 7 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_and_sevens_hand, num_wilds=2),
            (True, { 'high_rank': 14, 'low_rank': 7 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_and_sevens_hand, num_wilds=3),
            (True, { 'high_rank': 14, 'low_rank': 9 })
        )
        self.assertEqual(
            poker.two_pair_finder(pair_of_fours_and_sevens_hand, num_wilds=4),
            (True, { 'high_rank': 14, 'low_rank': 14 })
        )

    def test_three_of_a_kind_finder(self):
        five_high_hand = [
            cn.FOUR_OF_HEARTS,
            cn.FIVE_OF_HEARTS,
            cn.TWO_OF_SPADES,
            cn.THREE_OF_SPADES,
        ]
        self.assertEqual(
            poker.three_of_a_kind_finder(five_high_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(five_high_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(five_high_hand, num_wilds=2),
            (True, { 'rank': 5 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(five_high_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(five_high_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

        pair_of_fours_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.three_of_a_kind_finder(pair_of_fours_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(pair_of_fours_hand, num_wilds=1),
            (True, { 'rank': 4 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(pair_of_fours_hand, num_wilds=2),
            (True, { 'rank': 7 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(pair_of_fours_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(pair_of_fours_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

        three_fours_hand = [
            cn.THREE_OF_CLUBS,
            cn.FOUR_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.three_of_a_kind_finder(three_fours_hand, num_wilds=0),
            (True, { 'rank': 4 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(three_fours_hand, num_wilds=1),
            (True, { 'rank': 4 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(three_fours_hand, num_wilds=2),
            (True, { 'rank': 7 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(three_fours_hand, num_wilds=3),
            (True, { 'rank': 14 })
        )
        self.assertEqual(
            poker.three_of_a_kind_finder(three_fours_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

    def test_straight_finder(self):
        solo_run_hand = [
            cn.FOUR_OF_HEARTS,
        ]
        self.assertEqual(
            poker.straight_finder(solo_run_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(solo_run_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(solo_run_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(solo_run_hand, num_wilds=3),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(solo_run_hand, num_wilds=4),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_finder(solo_run_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        two_in_run_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
            cn.SIX_OF_SPADES,
        ]
        self.assertEqual(
            poker.straight_finder(two_in_run_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(two_in_run_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(two_in_run_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(two_in_run_hand, num_wilds=3),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_finder(two_in_run_hand, num_wilds=4),
            (True, { 'top_rank': 10 })
        )
        self.assertEqual(
            poker.straight_finder(two_in_run_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        three_in_run_hand = [
            cn.EIGHT_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
        ]
        self.assertEqual(
            poker.straight_finder(three_in_run_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(three_in_run_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.straight_finder(three_in_run_hand, num_wilds=2),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_finder(three_in_run_hand, num_wilds=3),
            (True, { 'top_rank': 10 })
        )
        self.assertEqual(
            poker.straight_finder(three_in_run_hand, num_wilds=4),
            (True, { 'top_rank': 12 })
        )
        self.assertEqual(
            poker.straight_finder(three_in_run_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        five_in_run_and_more_hand = [
            cn.SEVEN_OF_CLUBS,
            cn.EIGHT_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.FIVE_OF_HEARTS,
            cn.SIX_OF_HEARTS,
            cn.JACK_OF_HEARTS,
        ]
        self.assertEqual(
            poker.straight_finder(five_in_run_and_more_hand, num_wilds=0),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_finder(five_in_run_and_more_hand, num_wilds=1),
            (True, { 'top_rank': 9 })
        )
        self.assertEqual(
            poker.straight_finder(five_in_run_and_more_hand, num_wilds=2),
            (True, { 'top_rank': 11 })
        )
        self.assertEqual(
            poker.straight_finder(five_in_run_and_more_hand, num_wilds=3),
            (True, { 'top_rank': 12 })
        )
        self.assertEqual(
            poker.straight_finder(five_in_run_and_more_hand, num_wilds=4),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.straight_finder(five_in_run_and_more_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

    def test_flush_finder(self):
        solo_suit_hand = [
            cn.FOUR_OF_HEARTS,
            cn.THREE_OF_SPADES,
        ]
        self.assertEqual(
            poker.flush_finder(solo_suit_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(solo_suit_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(solo_suit_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(solo_suit_hand, num_wilds=3),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(solo_suit_hand, num_wilds=4),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(solo_suit_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        two_in_suit_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
            cn.SIX_OF_SPADES,
        ]
        self.assertEqual(
            poker.flush_finder(two_in_suit_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(two_in_suit_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(two_in_suit_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.flush_finder(two_in_suit_hand, num_wilds=3),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(two_in_suit_hand, num_wilds=4),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(two_in_suit_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        five_in_suit_hand = [
            cn.KING_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
            cn.EIGHT_OF_HEARTS,
            cn.NINE_OF_HEARTS,
            cn.JACK_OF_HEARTS,
        ]
        self.assertEqual(
            poker.flush_finder(five_in_suit_hand, num_wilds=0),
            (True, { 'top_rank': 11 })
        )
        self.assertEqual(
            poker.flush_finder(five_in_suit_hand, num_wilds=1),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(five_in_suit_hand, num_wilds=2),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(five_in_suit_hand, num_wilds=3),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(five_in_suit_hand, num_wilds=4),
            (True, { 'top_rank': 14 })
        )
        self.assertEqual(
            poker.flush_finder(five_in_suit_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

    def test_full_house_finder(self):
        five_high_hand = [
            cn.FOUR_OF_HEARTS,
            cn.FIVE_OF_HEARTS,
            cn.TWO_OF_SPADES,
            cn.THREE_OF_SPADES,
        ]
        self.assertEqual(
            poker.full_house_finder(five_high_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(five_high_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(five_high_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(five_high_hand, num_wilds=3),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(five_high_hand, num_wilds=4),
            (True, { 'triplet_rank': 14, 'pair_rank': 5 })
        )
        self.assertEqual(
            poker.full_house_finder(five_high_hand, num_wilds=5),
            (True, { 'triplet_rank': 14, 'pair_rank': 14 })
        )

        pair_of_fours_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_hand, num_wilds=2),
            (True, { 'triplet_rank': 7, 'pair_rank': 4 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_hand, num_wilds=3),
            (True, { 'triplet_rank': 14, 'pair_rank': 4 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_hand, num_wilds=4),
            (True, { 'triplet_rank': 14, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_hand, num_wilds=5),
            (True, { 'triplet_rank': 14, 'pair_rank': 14 })
        )

        three_fours_hand = [
            cn.THREE_OF_CLUBS,
            cn.FOUR_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.full_house_finder(three_fours_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_hand, num_wilds=1),
            (True, { 'triplet_rank': 4, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_hand, num_wilds=2),
            (True, { 'triplet_rank': 7, 'pair_rank': 4 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_hand, num_wilds=3),
            (True, { 'triplet_rank': 14, 'pair_rank': 4 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_hand, num_wilds=4),
            (True, { 'triplet_rank': 14, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_hand, num_wilds=5),
            (True, { 'triplet_rank': 14, 'pair_rank': 14 })
        )

        pair_of_fours_and_sevens_hand = [
            cn.THREE_OF_HEARTS,
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FOUR_OF_SPADES,
            cn.SEVEN_OF_SPADES,
            cn.NINE_OF_SPADES,
        ]
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_and_sevens_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_and_sevens_hand, num_wilds=1),
            (True, { 'triplet_rank': 7, 'pair_rank': 4 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_and_sevens_hand, num_wilds=2),
            (True, { 'triplet_rank': 9, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_and_sevens_hand, num_wilds=3),
            (True, { 'triplet_rank': 14, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_and_sevens_hand, num_wilds=4),
            (True, { 'triplet_rank': 14, 'pair_rank': 9 })
        )
        self.assertEqual(
            poker.full_house_finder(pair_of_fours_and_sevens_hand, num_wilds=5),
            (True, { 'triplet_rank': 14, 'pair_rank': 14 })
        )

        three_fours_two_sevens_hand = [
            cn.FOUR_OF_CLUBS,
            cn.THREE_OF_HEARTS,
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FOUR_OF_SPADES,
            cn.SEVEN_OF_SPADES,
            cn.NINE_OF_SPADES,
        ]
        self.assertEqual(
            poker.full_house_finder(three_fours_two_sevens_hand, num_wilds=0),
            (True, { 'triplet_rank': 4, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_two_sevens_hand, num_wilds=1),
            (True, { 'triplet_rank': 7, 'pair_rank': 4 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_two_sevens_hand, num_wilds=2),
            (True, { 'triplet_rank': 9, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_two_sevens_hand, num_wilds=3),
            (True, { 'triplet_rank': 14, 'pair_rank': 7 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_two_sevens_hand, num_wilds=4),
            (True, { 'triplet_rank': 14, 'pair_rank': 9 })
        )
        self.assertEqual(
            poker.full_house_finder(three_fours_two_sevens_hand, num_wilds=5),
            (True, { 'triplet_rank': 14, 'pair_rank': 14 })
        )

    def test_four_of_a_kind_finder(self):
        five_high_hand = [
            cn.FOUR_OF_HEARTS,
            cn.FIVE_OF_HEARTS,
            cn.TWO_OF_SPADES,
            cn.THREE_OF_SPADES,
        ]
        self.assertEqual(
            poker.four_of_a_kind_finder(five_high_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(five_high_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(five_high_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(five_high_hand, num_wilds=3),
            (True, { 'rank': 5 })
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(five_high_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

        pair_of_fours_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.four_of_a_kind_finder(pair_of_fours_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(pair_of_fours_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(pair_of_fours_hand, num_wilds=2),
            (True, { 'rank': 4 })
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(pair_of_fours_hand, num_wilds=3),
            (True, { 'rank': 7 })
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(pair_of_fours_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

        three_fours_hand = [
            cn.THREE_OF_CLUBS,
            cn.FOUR_OF_CLUBS,
            cn.FIVE_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
            cn.FIVE_OF_SPADES,
            cn.FOUR_OF_SPADES,
        ]
        self.assertEqual(
            poker.four_of_a_kind_finder(three_fours_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(three_fours_hand, num_wilds=1),
            (True, { 'rank': 4 })
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(three_fours_hand, num_wilds=2),
            (True, { 'rank': 5 })
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(three_fours_hand, num_wilds=3),
            (True, { 'rank': 7 })
        )
        self.assertEqual(
            poker.four_of_a_kind_finder(three_fours_hand, num_wilds=4),
            (True, { 'rank': 14 })
        )

    def test_straight_flush_finder(self):
        solo_run_hand = [
            cn.FOUR_OF_HEARTS,
        ]
        self.assertEqual(
            poker.straight_flush_finder(solo_run_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(solo_run_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(solo_run_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(solo_run_hand, num_wilds=3),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(solo_run_hand, num_wilds=4),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_flush_finder(solo_run_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        two_in_diff_suits_hand = [
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
            cn.SIX_OF_SPADES,
        ]
        self.assertEqual(
            poker.straight_flush_finder(two_in_diff_suits_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_diff_suits_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_diff_suits_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_diff_suits_hand, num_wilds=3),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_diff_suits_hand, num_wilds=4),
            (True, { 'top_rank': 10 })
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_diff_suits_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        two_in_same_suit_hand = [
            cn.EIGHT_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
        ]
        self.assertEqual(
            poker.straight_flush_finder(two_in_same_suit_hand, num_wilds=0),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_same_suit_hand, num_wilds=1),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_same_suit_hand, num_wilds=2),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_same_suit_hand, num_wilds=3),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_same_suit_hand, num_wilds=4),
            (True, { 'top_rank': 12 })
        )
        self.assertEqual(
            poker.straight_flush_finder(two_in_same_suit_hand, num_wilds=5),
            (True, { 'top_rank': 14 })
        )

        three_in_run_same_suit_hand = [
            cn.SEVEN_OF_CLUBS,
            cn.EIGHT_OF_CLUBS,
            cn.FOUR_OF_HEARTS,
            cn.SIX_OF_HEARTS,
            cn.SEVEN_OF_HEARTS,
        ]
        self.assertEqual(
            poker.straight_flush_finder(
                three_in_run_same_suit_hand,
                num_wilds=0
            ),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(
                three_in_run_same_suit_hand,
                num_wilds=1
            ),
            (False, {})
        )
        self.assertEqual(
            poker.straight_flush_finder(
                three_in_run_same_suit_hand,
                num_wilds=2
            ),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                three_in_run_same_suit_hand,
                num_wilds=3
            ),
            (True, { 'top_rank': 11 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                three_in_run_same_suit_hand,
                num_wilds=4
            ),
            (True, { 'top_rank': 12 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                three_in_run_same_suit_hand,
                num_wilds=5
            ),
            (True, { 'top_rank': 14 })
        )

        five_in_run_same_suit_hand = [
            cn.NINE_OF_HEARTS,
            cn.THREE_OF_SPADES,
            cn.FOUR_OF_SPADES,
            cn.FIVE_OF_SPADES,
            cn.SIX_OF_SPADES,
            cn.SEVEN_OF_SPADES,
        ]
        self.assertEqual(
            poker.straight_flush_finder(
                five_in_run_same_suit_hand,
                num_wilds=0
            ),
            (True, { 'top_rank': 7 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                five_in_run_same_suit_hand,
                num_wilds=1
            ),
            (True, { 'top_rank': 8 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                five_in_run_same_suit_hand,
                num_wilds=2
            ),
            (True, { 'top_rank': 9 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                five_in_run_same_suit_hand,
                num_wilds=3
            ),
            (True, { 'top_rank': 10 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                five_in_run_same_suit_hand,
                num_wilds=4
            ),
            (True, { 'top_rank': 13 })
        )
        self.assertEqual(
            poker.straight_flush_finder(
                five_in_run_same_suit_hand,
                num_wilds=5
            ),
            (True, { 'top_rank': 14 })
        )


if __name__ == '__main__':
    unittest.main()
