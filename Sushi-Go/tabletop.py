import copy
import random
import numpy as np


class SushiGo:
    def __init__(self, params, debugMode=False):
        if type(params) == list:
            self.numPlayers = params[0]
        if type(params) == list and len(params) > 1:
            self.maxRounds = params[1] #default should be 3
        self.debugMode = debugMode
        self.players = []
        # for i in range(self.numPlayers):
        #     self.players.append(Player(i, self.numPlayers))
        self.numRound = 0


    # def reset():
    #     for player in players:
    #         player.hand = player.generateHand
    #         # someone write generateHand plz
    #         player.board = []

    def display(self):
        for player in self.players:
            print "This is player {}'s hand:".format(player.playerNum), player.hand
            print "This is player {}'s board:".format(player.playerNum), player.board

    def generateDeck(self):
        distribution = {Nigiri: [10,10,10],
                        Wasabi: 10}
        self.deck = np.array([])
        for cardType in distribution:
            # print cardType
            # TODO: check the fact that your dictionary datatypes are not all the same
            # isinstance(distribution[cardType], list)
            if type(distribution[cardType]) == list:
                for variation in range(len(distribution[cardType])):
                    # print np.repeat(cardType(variation), distribution[cardType][variation])
                    self.deck = np.append(self.deck, np.repeat(cardType(variation+1), distribution[cardType][variation]))
            else:
                self.deck = np.append(self.deck, np.repeat(cardType(), distribution[cardType]))
        print self.deck

    def shuffleDeck(self):
        np.random.shuffle(self.deck)

    def dealHands(self, numplayers, numCards):
        for i in range(numplayers):
            hand = self.deck[:numCards]
            self.deck = self.deck[numCards:]
            print "HAND", hand
            # player.hand = hand

    def selectCards(self):
        # temporary
        move = Card("Squid Nigiri")

    def getCard(self):
        return self.deck[0] # if already shuffled otherwise we should take a random card

    def removeCard(self, card):
        self.deck.remove(card) # removes the first instance of the given card from the deck

    def addCard(self, card):
        self.deck.insert(random.randint(0, len(self.deck)), card) # adds a card to a random spot in the deck

    def processMoves(self, player, move):
        player.hand.remove(move)
        player.board.append(move)

    def passHands(self):
        # this might be pretty inefficient, optimize plz
        tempPlayers = copy.deepcopy(self.players)
        for player in self.players:
            player.hand = tempPlayers[(player.playerNum+1)%numPlayers]

    def runGame(self):
        for player in self.players:
            player.generateHand()
        self.display()
#        while True: #hopefully theres a better way to repeatedly check
        for player in self.players:
            self.processMoves(player, player.selectCards())
        if len(self.players[len(self.players)-1].hand) == 0:
            for player in self.players:
                player.scoreBoard()
                self.numRound += 1
                player.generateHand()
        else:
            self.passHands()



    # def runGame():
    #     numRound = 0
    #     for player in self.players:
    #         player.generateHand()
    #     self.display()
    #     while player.



# not sure if a card class helps
# I think we should just have files for Card and then subclasses for each card?
class Card:
    def __init__(self, cardType):
        self.cardType = cardType

# class Nigiri(Card):
   # def __init__(self, cardType,name, pointvalue):
   #     self.name = str(name)
   #     self.pointvalue = pointvalue
#
class Nigiri(Card):
    def __init__(self, variation):
        self.score = variation
#
#class Dumpling(Card):
#
class Wasabi(Card):
    def __init__(self):
        pass
#
#class Maki(Card):
#
#class Tempura(Card):
#
#class Pudding(Card):

board = SushiGo([2])
board.generateDeck()
board.shuffleDeck()
board.dealHands(4,10)

class Player:
    def __init__(self, playerNum, numPlayers, game):
        self.playerNum = playerNum
        # self.hand = self.generateHand(numPlayers)
        self.board = []
        self.score = 0
    # def scoreBoard():
    #     for i in self.board:
    #         if self.board[i].cardType == Nigiri:
    #             self.score += self.board[i].pointvalue

    # def generateHand():
    #     if len(self.hand < (12 - numPlayers))
            # self.hand.append(random.choice([Card('nigiri'),Card('Sashimi')]))#may want to change if we want to incorporate the number of times a card appears in the deck
