import copy
import random
import numpy as np
from Deck import *
from Cards import *
#import the players/algorithms here
from SamplePlayer import Sample
from SamplePlayer2 import Sample2
from MachineLearning2 import Learner2
from Human import Interactive
from CardEval import CardEvaluator
import math

distribution = {'Nigiri': 30, 'Wasabi': 10, 'Maki': 30, 'Dumpling': 30, 'Tempura': 30, 'Sashimi': 30, 'Pudding': 30}# someone needs to find the actuall distribution for cards

class SushiGoBoard:
    def __init__(self, numPlayers=4, maxRounds=3, debugMode=False):
        self.numPlayers, self.maxRounds, self.debugMode = numPlayers, maxRounds, debugMode
        self.handSize = 12 - self.numPlayers
        self.setAgents(agents=CardEvaluator(0, numPlayers, self), numLearner=1)

    def setAgents(self, agents=[], numHuman=0, numLearner=0):
        self.players = []
        if type(agents) == list:
            numCustom = len(agents)
            for i in range(numCustom):
                self.players.append(agents[i])
        else:
            numCustom = 1
            self.players.append(agents)
        for i in range(numCustom, numLearner):
            self.players.append(Learner2(i, self.numPlayers, True))
        for i in range(numCustom + numLearner, numLearner + numHuman):
            self.players.append(Interactive(i, self.numPlayers))
        for i in range(numCustom + numLearner + numHuman, self.numPlayers):
            self.players.append(Sample(i, self.numPlayers))

    def display(self):
        for player in self.players:
            print "This is player {}'s hand:".format(player.playerNum), player.hand
            print "This is player {}'s board:".format(player.playerNum), player.board
        #maybe move print winners to here and make scores a property of the class

    def generateDeck(self):
        self.deck = Deck()
        self.deck.generate(distribution)
        self.deck.shuffle()

    def dealHands(self):
        for player in self.players:
            player.takeHand(self.deck.getHand(self.handSize))

    def passHands(self):
        firstHand = copy.deepcopy(self.players[0].hand)
        for i in range(self.numPlayers-1):
            self.players[i].takeHand(self.players[i+1].hand)
        self.players[-1].takeHand(firstHand)

    def scoreNigiri(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Nigiri:
                    boardScores[-1] += card.pointValue
        
        print("Nigiri: " + str(boardScores))

        return boardScores

    def scoreSashimi(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Sashimi:
                    boardScores[-1] += 1
            boardScores[-1] =  np.floor(boardScores[-1]/3) * 10

        print("Sashimi: " + str(boardScores))

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

        print("Dumpling: " + str(boardScores))

        return boardScores

    def scoreWasabi(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Wasabi:
                    if card.nigiri:
                        boardScores[-1] += (2*card.nigiriCard.pointValue) # only * 2 becuase we already evaluate the point value once when scoring nigiri

        print("Wasabi: " + str(boardScores))

        return boardScores

    def scoreTempura(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Tempura:
                    boardScores[-1] += 1
            boardScores[-1] =  np.floor(boardScores[-1]/2) * 5
        print("Tempura: " + str(boardScores))
# use IsInstance function
        return boardScores

    def scoreMaki(self, boards): # is there anything more eficient?
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Maki:
                    boardScores[-1] += card.size
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
            elif i in seconds:
                boardScores[i] = np.floor(3/(len(seconds)))
            else:
                boardScores[i] = 0

        print("Maki: " + str(boardScores))

        return boardScores

    def scorePudding(self, boards):
        boardScores = []
        for board in boards:
            boardScores.append(0)
            for card in board:
                if type(card) == Cards.Pudding:
                    boardScores[-1] += 1
        sortScores = sorted(boardScores)
        firsts = []
        lasts = []
        for i in range(len(boardScores)):
            if boardScores[i] == sortScores[-1]:
                firsts.append(i)
            elif boardScores[i] == sortScores[1]:
                lasts.append(i)
        for i in range(len(boardScores)):
            if i in firsts:
                boardScores[i] = np.floor(6/(len(firsts)))
            elif i in lasts:
                boardScores[i] = np.floor(-6/(len(lasts)))
            else:
                boardScores[i] = 0

        print("Pudding: " + str(boardScores))

        return boardScores



    def score(self, lastRound=False):
        boards = [player.board for player in self.players]
        scores = np.array([self.scoreNigiri(boards), self.scoreSashimi(boards), self.scoreDumpling(boards), self.scoreWasabi(boards), self.scoreTempura(boards), self.scoreMaki(boards)])
        if lastRound:
            scores = np.append(scores, np.array([self.scorePudding(boards)]), axis=0)
        scores = np.sum(scores, axis=0)
        return scores

    def scoreSingle(self, Board):
        Score = self.scoreNigiri([Board])[0] + self.scoreSashimi([Board])[0] + self.scoreDumpling([Board])[0] + self.scoreWasabi([Board])[0] + self.scoreTempura([Board])[0]
        return Score

    def setup(self):
        for player in self.players:
            player.round += 1
            player.setup()
        #put any other code here to setup the cycle

    def cleanup(self):
        for player in self.players:
            player.cleanup()


    def cycle(self): # think of a better name, but round is already defined in python
        self.dealHands()
        hands = []
        for turn in range(self.handSize):
            for i in range(self.numPlayers):
                move = self.players[i].move(self)
                self.players[i].board.append(move)
                if self.debugMode:
                    print "Player " + str(i+1) + " played a " + move.cardType + "."
            if turn != self.handSize - 1:
                self.passHands()
                if self.debugMode:
                    print "Passing Hands. Next Turn."

    def printWinners(self, scores, roundNum=False):
        sortedPlayers = sorted(self.players, key=lambda player: player.score)
        if type(roundNum) == int:
            print "Round " + str(roundNum+1) + ", Stop."
        print "Score Board:"
        for i in range(self.numPlayers):
            sortedPlayers[i].place = self.numPlayers - i
            print "    Player " + str(i+1) + " Scored " + str(scores[i]) + " Points this round, for a total of " +str(self.players[i].score) + " Points."
        print "Player " + str(sortedPlayers[-1].playerNum + 1) + " is in the lead"

    def run(self):
        self.generateDeck()
        winners = []
        for roundNum in range(self.maxRounds):
            if self.debugMode:
                print "Round " + str(roundNum+1) + ", Start."
            self.setup()
            self.cycle()
            if roundNum != (self.maxRounds - 1):
                scores = self.score()
            else:
                scores = self.score(lastRound=True)
            for k in range(self.numPlayers):
                self.players[k].score += scores[k]
            self.cleanup()
            self.printWinners(scores, roundNum)
        sortedPlayers = sorted(self.players, key=lambda player: player.score)
        winner = sortedPlayers[-1].playerNum
        return winner

    def test(self, player, numGames=100):
        self.setAgents(agents=player)
        oldDebugMode = copy.copy(self.debugMode)
        self.debugMode = False
        winners = []
        for i in range(numGames):
            winners.append(self.run())
        sortedPlayers = sorted(self.players, key=lambda player: player.score)
        place = self.numPlayers - sortedPlayers.index(player)
        numWins = winners.count(0)
        self.debugMode = oldDebugMode
        print winners
        return np.divide(numWins, numGames), place

    def normalDistribution(self):
            jankrandomarray = []
            ODDdistribution = {}
            normHand = []
            myHypoDeckSize = 190.0#len(self.deck)
            for k,v in distribution.items(): #calculates normal distribution based on 'distribution' parameter
                print k
                if k == 'Maki':
                    ODDdistribution[k + '1'] = v/(3.0*myHypoDeckSize)
                    ODDdistribution[k + '2'] = v/(3.0*myHypoDeckSize)
                    ODDdistribution[k + '3'] = v/(3.0*myHypoDeckSize)
                elif k == 'Nigiri':
                    ODDdistribution[k + '1'] = v/(3.0*myHypoDeckSize)
                    ODDdistribution[k + '2'] = v/(3.0*myHypoDeckSize)
                    ODDdistribution[k + '3'] = v/(3.0*myHypoDeckSize)
                else:
                    ODDdistribution[k] = v/myHypoDeckSize
                    print ODDdistribution[k]
            for k in ODDdistribution.keys():
                #if ((math.floor(ODDdistribution[k]*self.handSize)) != 0) : #the expected value for a single card being in the balanced hand
                print k + str(ODDdistribution[k])
                for i in range(int(np.floor(ODDdistribution[k]*self.handSize))):
                    if k == 'Nigiri1': # we need a more efficient method
                            normHand.append(Cards.Nigiri(1))
                    if k == 'Nigiri2': # we need a more efficient method
                            normHand.append(Cards.Nigiri(2))
                    if k == 'Nigiri3': # we need a more efficient method
                            normHand.append(Cards.Nigiri(3))
                    if k == 'Wasabi':
                            normHand.append(Cards.Wasabi())
                    if k == 'Sashimi':
                            normHand.append(Cards.Sashimi())
                    if k == 'Dumpling':
                            normHand.append(Cards.Dumpling())
                    if k == 'Tempura':
                            normHand.append(Cards.Tempura())
                    if k == 'Maki1':
                            normHand.append(Cards.Maki(1))
                    if k == 'Maki2':
                            normHand.append(Cards.Maki(2))
                    if k == 'Maki3':
                            normHand.append(Cards.Maki(3))
                    if k == 'Pudding':
                            normHand.append(Cards.Pudding())
            for k in distribution:
                print k
                 # JANKYJANkJANK
                if k == 'Nigiri': # we need a more efficient method
                    for j in range(distribution[k]/3):
                        jankrandomarray.append(Cards.Nigiri(1))
                        jankrandomarray.append(Cards.Nigiri(2))
                        jankrandomarray.append(Cards.Nigiri(3))
                if k == 'Wasabi':
                    for j in range(distribution[k]):
                        jankrandomarray.append(Cards.Wasabi())
                if k == 'Sashimi':
                    for j in range(distribution[k]):
                        jankrandomarray.append(Cards.Sashimi())
                if k == 'Dumpling':
                    for j in range(distribution[k]):
                        jankrandomarray.append(Cards.Dumpling())
                if k == 'Tempura':
                    for j in range(distribution[k]):
                        jankrandomarray.append(Cards.Tempura())
                if k == 'Maki':
                    for z in range(distribution[k]/3):
                        jankrandomarray.append(Cards.Maki(1))
                        jankrandomarray.append(Cards.Maki(2))
                        jankrandomarray.append(Cards.Maki(3))
                if k == 'Pudding':
                    for j in range(distribution[k]):
                        jankrandomarray.append(Cards.Pudding())
            while (len(normHand) < self.handSize): # fill remaining cards based on pure probability
                normHand.append(jankrandomarray[random.randint(0,myHypoDeckSize)])



    #                normHand.append(thisCard)

            print normHand
            return normHand

# SushiGo= SushiGoBoard([4,1], False)
# SushiGo.normalDistribution()
