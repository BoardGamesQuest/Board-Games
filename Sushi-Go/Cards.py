
class Card:
    def __init__ (self, cardType):
        self.cardType = cardType

    def score(self,  amount):
        raise NotImplementedError('subclasses must override score()') # should return the points from this tyoe of card given the number of cards

class Nigiri(Card):
    def __init__(self, pointValue):
        super(self, ('Nigiri '+ str(pointValue))).__init__()

    def score(self, amount): #if each card has a score function we will only have to call this on one card it might be better to create a score fnction that calculates score in the SushiGo class
        pass
