from deck import Card, Deck
import nose.tools as n


def test_card_init():
    card = Card("J", "s")
    n.assert_equal(card.number, "J")
    n.assert_equal(card.suit, "s")

def test_card_str():
    card = Card("A", "c")
    n.assert_equal(str(card), "Ac")

def test_card_lt():
    card1 = Card("3", "d")
    card2 = Card("8", "d")
    n.assert_less(card1, card2)

def test_card_gt():
    card1 = Card("K", "s")
    card2 = Card("10", "c")
    n.assert_greater(card1, card2)

def test_card_equal():
    card1 = Card("5", "c")
    card2 = Card("5", "h")
    n.assert_equal(card1, card2)

def test_deck_init():
    deck = Deck()
    n.assert_equal(len(deck), 52)
    cards = set()
    for card in deck.cards:
        card_tuple = (card.number, card.suit)
        n.assert_not_in(card_tuple, cards)
        cards.add(card_tuple)

def test_draw_card():
    deck = Deck()
    card = deck.draw_card()
    n.assert_equal(len(deck), 51)
