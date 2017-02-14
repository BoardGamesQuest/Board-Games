import copy
import random
import numpy as np
from Deck import *
from Cards import *
#import the players/algorithms here
from SamplePlayer import Sample


class SushiGoBoard:
    def __init__(self, params, debugMode=False):
        if type(params) == list:
            self.numPlayers = params[0]
        if type(params) == list and len(params) > 1:
            self.maxRounds = params[1] #default should be 3
        else:
            self.maxRounds = 3
        self.debugMode = debugMode
        self.players = []
        for i in range(self.numPlayers):
            self.players.append(Sample(i, self.numPlayers))
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
        distribution = {'Nigiri': 30, 'Wasabi': 10}# someone needs to find the actuall distribution for cards
        self.deck = Deck()
        self.deck.generate(distribution)
        self.deck.shuffle()
        print (self.deck.cards)
 #       self.deck = np.array([])
#        for cardType in distribution:
#            # print cardType
#            if type(distribution[cardType]) == list:
#                for variation in range(len(distribution[cardType])):
#                    # print np.repeat(cardType(variation), distribution[cardType][variation])
#                    self.deck = np.append(self.deck, np.repeat(cardType(variation), distribution[cardType][variation]))
#            else:
#                self.deck = np.append(self.deck, np.repeat(cardType(), distribution[cardType]))
#        print self.deck

#    def shuffleDeck(self):
#        np.random.shuffle(self.deck) # already in the Deck class

    def dealHands(self):
        handSize = 12 - self.numPlayers
        for player in self.players:
            player.takeHand(self.deck.getHand(handSize))
            # player.hand = hand

#    def selectCards(self):
#        # temporary
#        move = Card("Squid Nigiri")


# not needed for this version of game, might be usefull for debugging
#    def getCard(self):
#        return self.deck.getCard() # if already shuffled otherwise we should take a random card

#    def removeCard(self, card):
#        self.deck.removeCard(card) # removes the first instance of the given card from the deck

#    def addCard(self, card):
#        self.deck.addCard(card) # adds a card to a random spot in the deck

#    def processMoves(self, player, move):
#        player.hand.remove(move)
#        player.board.append(move)

    def passHands(self):
        # this might be pretty inefficient, optimize plz
        tempPlayers = copy.deepcopy(self.players)
        for player in self.players:
            player.hand = tempPlayers[(player.playerNum+1)%numPlayers]

    def scoreNigiri(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Nigiri:
                    boardScores[-1] += card.pointValue

        return boardScores

    def scoreSashimi(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Sashimi:
                    boardScore[-1] += 1
            boardScores[-1] =  np.floor(boardScores[-1]/3) * 10

        return boardScores

    def scoreDumpling(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Dumpling:
                    boardScores[-1] += 1
            score = 0
            if (boardScores[-1] < 5):
                for i in range(boardScores[-1]): # there might be something more efficient
                    score += i
                boardScores[-1] = score
            else:
                boardScores[-1] = 15

        return boardScores

    def scoreWasabi(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Wasabi:
                    if card.nigiri:
                        boardScores[-1] += (2*card.nigiriCard.pointvalue) # only * 2 becuase we already evaluate the point value once when scoring nigiri

        return boardScores

    def scoreTempura(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Tempura:
                    boardScore[-1] += 1
            boardScores[-1] =  np.floor(boardScores[-1]/2) * 5
# use IsInstance function
        return boardScores

    def scoreMaki(self, boards): # is there anything more eficient?
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Maki:
                    boardScore[-1] += card.size
        sortScores = sorted(boardScores)
        firsts = []
        seconds = []
        for i in range(len(boardScores)):
            if boardScores[i] == sortScores[-1]:
                firsts.append(i)
            elif boardScores[i] == sortScores[- (1+sortScores.count(sortScores[-1]))]:
                seconds.append(i)
        for i in range(len(boardScores)):
            if i in firsts:
                boardScores[i] = np.floor(6/(len(firsts)))
            elif i in second:
                boardScores[i] = np.floor(3/(len(seconds)))
            else:
                boardScores[i] = 0

        return boardScores

    def scorePudding(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Pudding:
                    boardScore[-1] += 1
        sortScores = sorted(boardScores)
        firsts = []
        lasts = []
        for i in range(len(boardScores)):
            if boardScores[i] == sortScores[-1]:
                firsts.append(i)
            elif boardScores[i] == sortedScores[1]:
                lasts.append(i)
        for i in range(len(boardScores)):
            if i in firsts:
                boardScores[i] = np.floor(6/(len(firsts)))
            elif i in lasts:
                boardScores[i] = np.floor(-6/(len(seconds)))
            else:
                boardScores[i] = 0

        return boardScores



    def score(self, lastround):
        boards = []
        for player in self.players:
            boards.append(player.board)
        scores = []
        scores.append(self.scoreNigiri(boards))
        scores.append(self.scoreSashimi(boards))
        scores.append(self.scoreDumpling(boards))
        scores.append(self.scoreWasabi(boards))
        scores.append(self.scoreTempura(boards))
        scores.append(self.scoreMaki(boards))
        if lastround:
            scores.append(self.scorePudding(boards))
        finalScore = []
        for i in range(len(scores[0])):
            finalScore.append(0)
            for score in scores:
                finalScore[-1] += score[i]

        return finalScore


    def cycle(self): # think of a better name, but round is already defined in python
        self.generateDeck()
        self.dealHands()
        hands = []
        emptyHands = 0
        while True:
            for player in self.players:
                move = player.move()
                print (move)
            for player in self.players:
                hands.append(player.giveHand())
            for hand in hands:
                if len(hand) == 0:
                    emptyHands += 1
            if emptyHands == len(hands):
                print('round over')
                break
            hands.append(hands[0])
            hands = hands[1:]
            for player in self.players:
                player.takeHand(hands[0])
                hands = hands[1:]


    def run(self):
        for i in range(self.maxRounds):
            self.cycle()
            if i != (self.maxRounds - 1):
                scores = self.score(False)
            else:
                scores = self.score(True)
            print (scores)
            for i in range(len(scores)):
                self.players[i].score += scores[i]



    # def runGame():
    #     numRound = 0
    #     for player in self.players:
    #         player.generateHand()
    #     self.display()
    #     while player.
