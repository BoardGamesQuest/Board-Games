import random
from abc import ABCMeta, abstractmethod

class Abstract:
    __metaclass__ = ABCMeta
    def __init__(self, playerNum, numPlayers):
        self.playerNum = playerNum
        self.round = 0
        self.score = 0
        self.board = []
        self.numPlayers = numPlayers

    def takeHand(self, hand):
        self.hand = hand

    def move(self, game):
        raise NotImplementedError('Each player must have a move() function')
        # each player/algorithm should overide this method to return the card of choice

    def cleanup(self):
        self.hand = []
        newBoard = []
        for card in self.board:
            if card.cardType == 'Pudding':
                newBoard.append(card)
        self.board = newBoard

    def setup(self):
        pass
