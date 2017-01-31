import random
from abc import ABCMeta, abstractmethod

class Abstract:
    __metaclass__ = ABCMeta
    def __init__(self, playerNum, numPlayers):
        self.playerNum = playerNum
        self.hand = []
        self.score = 0
        self.board = []


#    def scoreBoard(self):
#        for i in self.board:
#            if self.board[i].cardType == 'Nigiri':
#                self.score += self.board[i].pointvalue
#need to implement the new method of scoring for cards using the score() function

    def takeHand(self, hand):
        self.hand = hand

    def giveHand(self):
        return self.hand

    #def generateHand(self):
#        while (len(self.hand) < 8):#formula for cards in hand given numPlayers)
#            self.hand.append(random.choice([Card('nigiri'),Card('Sashimi'),Card('Dumpling'),Card('Wasabi'),Card('Maki'),Card('Tempura'),Card('Pudding')]))#may want to change if we want to incorporate the number of times a card appears in the deck
#        for i in range(len(self.hand)):
#            print self.hand[i].cardType

    def move(self):
        raise NotImplementedError('Each player must have a move() function')
        # each player/algorithm should overide this method to return the card of choice

# me = Player(1,1)
# me.generateHand()
