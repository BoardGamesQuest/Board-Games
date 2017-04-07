import random
import Cards

distribution = {'Nigiri': 5, 'Wasabi': 0, 'Maki': 2, 'Dumpling': 14, 'Tempura': 14, 'Sashimi': 14, 'Pudding': 10}# someone needs to find the actuall distribution for cards
makiDistribution = [3, 5, 2]
nigiriDistribution = [1,2,1]
# from SushiGo import distribution, makiDistribution, nigiriDistribution

class Deck:
    def __init__(self):
        self.cards = []

    def generateCards(self):
        for cardType in distribution:
            if cardType == 'Nigiri': # we need a more efficient method
                for i in range(distribution[cardType]):
                    for j in range(len(nigiriDistribution)):
                        for k in range(nigiriDistribution[j]):
                            cards.append(Cards.Nigiri(j))
            if cardType == 'Wasabi':
                for i in range(distribution[cardType]):
                    cards.append(Cards.Wasabi())
            if cardType == 'Sashimi':
                for i in range(distribution[cardType]):
                    cards.append(Cards.Sashimi())
            if cardType == 'Dumpling':
                for i in range(distribution[cardType]):
                    cards.append(Cards.Dumpling())
            if cardType == 'Tempura':
                for i in range(distribution[cardType]):
                    cards.append(Cards.Tempura())
            if cardType == 'Maki':
                for i in range(distribution[cardType]):
                    for j in range(len(makiDistribution)):
                        for k in range(makiDistribution[j]):
                            cards.append(Cards.Maki(j))
            if cardType == 'Pudding':
                for i in range(distribution[cardType]):
                    cards.append(Cards.Pudding())

        return cards

    def generate(self):
        self.cards = self.generateCards()

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
