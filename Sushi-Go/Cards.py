import numpy as np

class AbstractCard:
    def __init__ (self, cardType):
        self.cardType = cardType

#    def score(self,  amount):
#        raise NotImplementedError('subclasses must override score()') # should return the points from this tyoe of card given the number of cards

class Nigiri(AbstractCard):
    def __init__(self, pointValue):
        super(self, ('Nigiri '+ str(pointValue))).__init__()
        self.pointValue = pointValue

#    def score(self, amount): #if each card has a score function we will only have to call this on one card it might be better to create a score fnction that calculates score in the SushiGo class
#        return amount * self.pointValue
        

class Sashimi(AbstractCard):
    def __init__(self):
        super(self, 'Sashimi').__init__()

#    def score(self, amount):
#        return np.floor(amount/3) * 3

class Dumpling(AbstractCard):
    def __init__(self):
        super(self, 'Dumpling').__init__()

#    def score(self, amount):
#        score = 0
#        if (amount < 5):
#            for i in range(amount): # there might be something more efficient
#                score += i
#            return score
#        else:
#            return 15

class Wasabi(AbstractCard):
    def __init__(self):
        super(self, 'Wasabi').__init__()
        self.nigiri = False
        self.nigiriCard

    def addNigiri(self, nigiri):
        self.nigiri = True
        self.nigiriCard = nigiri

#    def score(self, amount): #this means we will have to evaluate each wasabi seperately
#        if self.nigiri:
#            return (self.nigiri.score() * 2) #*2 because we are already counting one by scoring the nigiri
#        else:
#            return 0

class Tempura(AbstractCard):
    def __init__(self):
        super(self, 'Tempura').__inti__()

#    def score(self, amount):
#        return np.floor(amount/2) * 2

class Maki(AbstractCard): # I do not like that the formating of ths and the nigiri card is different from the rest. this one is also harder to score, any Ideas?
    def __init__(self, size):
        super(self, ('Maki' + str(size))).__init__()
        self.size = size

#    def getSize(self):
#        return self.size

#    def getTotal(self, Maki):
#        total = 0
#        for card in Maki:
#            total += card.getSize()
#        return total

#    def score(self, Maki, totals):
#        total = self.getTotal(self, Maki)
#        sorttotals = sorted(totals)
#        ties = sorttotals.count(total)
#        if total == sorttotals[-1]:
#            return np.floor(6/(ties+1))
#        elif total == sorttotals[ - (1 + sorttotals.count(sorttotals[-1]))]:
#            return np.floor(3/(ties+1))
#        else:
#            return 0
            

class Pudding(AbstractCard):
    def __init__(self):
        super(self, 'Pudding').__init__()

#    def score(self, amount, amounts):
#        sortamounts = sorted(amounts)
#        ties = sortamounts.count(amount)
#        if amount == sortamounts[-1]:
#            return np.floor(6/(ties+1))
#        elif amount == sortamounts[1]:
#            return np.floor(-6/(ties+1))
#        else:
#            return 0

        
