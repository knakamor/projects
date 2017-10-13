import random


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.discard = []

    def receive_card(self, card):
        self.discard.append(card)

    def receive_cards(self, cards):
        self.discard.extend(cards)

    def play_card(self):
        if not self.hand:
            random.shuffle(self.discard)
            self.hand = self.discard
            self.discard = []
        if not self.hand:
            return None
        card = self.hand.pop()
        return card

    def __repr__(self):
        return self.name

    def __len__(self):
        return len(self.hand) + len(self.discard)
