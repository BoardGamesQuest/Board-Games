import copy
import random
import numpy as np
from Deck import *
from Cards import *
from scoring import *
#import the players/algorithms here
from SamplePlayer import Sample
from SamplePlayer2 import Sample2
from MachineLearning2 import Learner2
from Human import Interactive
from CardEval import CardEvaluator
import math

distribution = {'Nigiri': 5, 'Wasabi': 0, 'Maki': 2, 'Dumpling': 14, 'Tempura': 14, 'Sashimi': 14, 'Pudding': 10}# someone needs to find the actuall distribution for cards

class SushiGoBoard:
    def __init__(self, numPlayers=4, maxRounds=3, debugMode=False):
        self.numPlayers, self.maxRounds, self.debugMode = numPlayers, maxRounds, debugMode
        self.handSize = 12 - self.numPlayers
        self.setAgents()
        self.generateDeck()

    def setAgents(self, agents=[], numHuman=0, numLearner=0):
        self.players = []
        if type(agents) == list:
            numCustom = len(agents)
            for i in range(numCustom):
                self.players.append(agents[i])
        else:
            numCustom = 1
            self.players.append(agents)
        for i in range(numCustom, numCustom + numLearner):
            self.players.append(Learner2(i, self.numPlayers, True))
        for i in range(numCustom + numLearner, numCustom + numLearner + numHuman):
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

    def score(self, lastRound=False):
        boards = [player.board for player in self.players]
        scores = np.array([scoreNigiri(boards), scoreSashimi(boards), scoreDumpling(boards), scoreWasabi(boards), scoreTempura(boards), scoreMaki(boards)])
        if lastRound:
            scores = np.append(scores, np.array([scorePudding(boards)]), axis=0)
        scores = np.sum(scores, axis=0)
        return scores

    def scoreSingle(self, Board):
        Score = scoreNigiri([Board])[0] + scoreSashimi([Board])[0] + scoreDumpling([Board])[0] + scoreWasabi([Board])[0] + scoreTempura([Board])[0]
        return Score

    def reset(self):
        self.generateDeck()
        for player in self.players:
            player.score = 0
            player.round = 0

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
                self.players[i].chosenCard = self.players[i].move(self)
                #self.players[i].board.append(move)
            for i in range(self.numPlayers):
                self.players[i].board.append(self.players[i].chosenCard)
                self.players[i].hand.remove(self.players[i].chosenCard)
                if self.debugMode:
                    print "Player " + str(i+1) + " played a " + self.players[i].chosenCard.cardType + "."

            if turn != self.handSize - 1:
                self.passHands()
                if self.debugMode:
                    print "Passing Hands. Next Turn."

    def printWinners(self, scores, roundNum=False):
        sortedPlayers = sorted(self.players, key=lambda player: player.score, reverse=True)
        if type(roundNum) == int:
            print "Round " + str(roundNum+1) + ", Stop."
        print "Score Board:"
        for i in range(self.numPlayers):
            sortedPlayers[i].place = i + 1 # What about ties?
            print "    Player " + str(i+1) + " Scored " + str(scores[i]) + " Points this round, for a total of " +str(self.players[i].score) + " Points."
        print "Player " + str(sortedPlayers[0].playerNum + 1) + " is in the lead"

    def run(self, withScores=False):
        self.reset()
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
            if self.debugMode:
                self.printWinners(scores, roundNum)
        sortedPlayers = sorted(self.players, key=lambda player: player.score)
        winner = sortedPlayers[-1].playerNum
        return winner

    def test(self, player, numGames=100):
        print "TESTING"
        oldAgents = copy.deepcopy(self.players)
        oldDebugMode = copy.copy(self.debugMode)
        self.debugMode = False
        winners, scores = [], []
        self.setAgents(agents=player)
        for i in range(numGames):
            winners.append(self.run())
            scores.append([player.score for player in self.players])
        absoluteScores = np.sum(scores, axis=0)
        print absoluteScores
        # print scores
        numWins = winners.count(0)
        self.debugMode = oldDebugMode
        self.setAgents(agents=oldAgents)
        return np.true_divide(numWins, numGames), winners

    def normalDistribution(self):
            jankrandomarray = Deck()
            jankrandomarray.generate(distribution)
            jankrandomarray.shuffle()
            ODDdistribution = {}
            normHand = []
            myHypoDeckSize = len(jankrandomarray.cards)
            for k,v in distribution.items(): #calculates normal distribution based on 'distribution' parameter
                #print k
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
                    #print ODDdistribution[k]
            for k in ODDdistribution.keys():
                #if ((math.floor(ODDdistribution[k]*self.handSize)) != 0) : #the expected value for a single card being in the balanced hand
                #print k + str(ODDdistribution[k])
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
            # for k in distribution:
            #     #print k
            #      # JANKYJANkJANK
            #     if k == 'Nigiri': # we need a more efficient method
            #         for j in range(distribution[k]/3):
            #             jankrandomarray.append(Cards.Nigiri(1))
            #             jankrandomarray.append(Cards.Nigiri(2))
            #             jankrandomarray.append(Cards.Nigiri(3))
            #     if k == 'Wasabi':
            #         for j in range(distribution[k]):
            #             jankrandomarray.append(Cards.Wasabi())
            #     if k == 'Sashimi':
            #         for j in range(distribution[k]):
            #             jankrandomarray.append(Cards.Sashimi())
            #     if k == 'Dumpling':
            #         for j in range(distribution[k]):
            #             jankrandomarray.append(Cards.Dumpling())
            #     if k == 'Tempura':
            #         for j in range(distribution[k]):
            #             jankrandomarray.append(Cards.Tempura())
            #     if k == 'Maki':
            #         for z in range(distribution[k]/3):
            #             jankrandomarray.append(Cards.Maki(1))
            #             jankrandomarray.append(Cards.Maki(2))
            #             jankrandomarray.append(Cards.Maki(3))
            #     if k == 'Pudding':
            #         for j in range(distribution[k]):
            #             jankrandomarray.append(Cards.Pudding())
            for n in range(self.handSize - len(normHand)): # fill remaining cards based on pure probability
                if (self.handSize - len(normHand) != 0) :
                    normHand.append(jankrandomarray.cards[random.randint(0,myHypoDeckSize-1)])
            #print normHand
            return normHand

# SushiGo= SushiGoBoard([4,1], False)
# SushiGo.normalDistribution()
