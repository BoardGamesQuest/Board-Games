import random

class Deck:
    def __init__(self):
        self.cards = []

    def generate(self):
        distribution = {} # someone needs to find the actuall distribution fo cards

    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        return self.cards[random.randint(0, len(self.cards))]#returns a random card

    def removeCard(self, card):
        self.card.remove(card) # removes the first instance of the given card from the deck

    def addCard(self, card):
        self.cards.insert(random.randint(0, len(self.cards)), card) # adds a card to a random spot in the deck

    def getDeck(self):
        return self.cards

