import copy
import random

class SushiGo:
    def __init__(self, params, debugMode=False):
        if type(params) == list:
            self.numPlayers = params[0]
        self.debugMode = debugMode
        self.players = []
        for i in range(numPlayers):
            players.append(Player(i, numPlayers))

    # def reset():
    #     for player in players:
    #         player.hand = player.generateHand
    #         # someone write generateHand plz
    #         player.board = []

    def display():
        for player in self.players:
            print "This is player {}'s hand:".format(player.playerNum), player.hand
            print "This is player {}'s board:".format(player.playerNum), player.board

    def selectCards():
        # temporary
        move = Card("Squid Nigiri")

    def processMoves(player, move):
        player.hand.remove(move)
        player.board.append(move)

    def passHands():
        # this might be pretty inefficient, optimize plz
        tempPlayers = copy.deepcopy(self.players)
        for player in self.players:
            player.hand = tempPlayers[(player.playerNum+1)%numPlayers]




    def runGame():
        numRound = 0
        for player in self.players:
            player.generateHand()
        self.display()
        while player.



# not sure if a card class helps
# I think we should just have files for Card and then subclasses for each card?
class Card:
    def __init__(self, cardType):
        self.cardType = cardType

#class Nigiri(Card):
#    def __init__(self, cardType,name, pointvalue):
#        self.name = str(name)
#        self.pointvalue = pointvalue
#
#class Sashimi(Card):
#
#class Dumpling(Card):
#
#class Wasabi(Card):
#
#class Maki(Card):
#
#class Tempura(Card):
#
#class Pudding(Card):


class Player:
    def __init__(self, playerNum, numPlayers):
        self.playerNum = playerNum
        self.hand = self.generateHand(numPlayers)
        self.board = []
        self.score = 0
    def scoreBoard():
        for i in self.board:
            if self.board[i].cardType == Nigiri
                self.score += self.board[i].pointvalue

    def generateHand():
        if len(self.hand < #formula for cards in hand gien numPlayers)
            self.hand.append(random.choice([Card('nigiri'),Card('Sashimi')]))#may want to change if we want to incorporate the number of times a card appears in the deck
