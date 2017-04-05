import random
from abc import ABCMeta, abstractmethod

class Abstract:
    __metaclass__ = ABCMeta
    def __init__(self, playerNum, numPlayers):
        self.playerNum = playerNum
        self.round = 0
        self.score = 0
        self.setup()

    def takeHand(self, hand):
        self.hand = hand

    def giveHand(self):
        return self.hand

    def move(self, game):
        raise NotImplementedError('Each player must have a move() function')
        # each player/algorithm should overide this method to return the card of choice

    def cleanup(self):
        pass

    def setup(self):
        self.hand = []
        self.place = 0
        try:
            newBoard = []
            for card in self.board:
                if type(card) == Nigiri:
                    newBoard.append(card)
        except:
            self.board = []
        self.board = newBoard
