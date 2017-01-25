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
        distribution = {Sashimi: [10,10,10], Wasabi: 10}
        self.deck = np.array([])
        for cardType in distribution:
            # print cardType
            if type(distribution[cardType]) == list:
                for variation in range(len(distribution[cardType])):
                    # print np.repeat(cardType(variation), distribution[cardType][variation])
                    self.deck = np.append(self.deck, np.repeat(cardType(variation), distribution[cardType][variation]))
            else:
                self.deck = np.append(self.deck, np.repeat(cardType(), distribution[cardType]))
        print self.deck

    def shuffleDeck(self):
        np.random.shuffle(self.deck)

    def dealHands(self, numplayers, numCards):
        for i in range(numplayers):
            hand = self.deck[:numCards]
            self.deck = self.deck[numCards+1:]
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
