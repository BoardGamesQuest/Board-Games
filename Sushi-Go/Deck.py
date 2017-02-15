import random
import Cards

class Deck:
    def __init__(self):
        self.cards = []

    def generate(self, distribution):
        for cardType in distribution:
            if cardType == 'Nigiri': # we need a more efficient method
                for i in range(distribution[cardType]/3):
                    self.cards.append(Cards.Nigiri(1))
                    self.cards.append(Cards.Nigiri(2))
                    self.cards.append(Cards.Nigiri(3))
            if cardType == 'Wasabi':
                for i in range(distribution[cardType]):
                    self.cards.append(Cards.Wasabi())
            if cardType == 'Sashimi':
                for i in range(distribution[cardType]):
                    self.cards.append(Cards.Sashimi())
            if cardType == 'Dumpling':
                for i in range(distribution[cardType]):
                    self.cards.append(Cards.Dumpling())
            if cardType == 'Tempura':
                for i in range(distribution[cardType]):
                    self.cards.append(Cards.Tempura())
            if cardType == 'Maki':
                for i in range(distribution[cardType]/3):
                    self.cards.append(Cards.Maki(1))
                    self.cards.append(Cards.Maki(2))
                    self.cards.append(Cards.Maki(3))
            if cardType == 'Pudding':
                for i in range(distribution[cardType]):
                    self.cards.append(Cards.Pudding())

        return self.cards


    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        return self.cards[random.randint(0, len(self.cards)-1)]#returns a random card

    def getHand(self, size):
        hand = []
        for i in range(size):
            card = self.getCard()
            hand.append(card)
            self.removeCard(card)
        return hand

    def removeCard(self, card):
        self.cards.remove(card) # removes the first instance of the given card from the deck

    def addCard(self, card):
        self.cards.insert(random.randint(0, len(self.cards)), card) # adds a card to a random spot in the deck

    def getDeck(self):
        return self.cards
