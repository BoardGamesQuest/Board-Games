import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, main, copy
from main import Agent, Board

class Q(Agent):
    def __init__(self, boardParams, learningRate=0.9, discountRate=0.5, randomness=0.2, debugMode=False):
        super(Q, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        self.Q, self.R = {}, {}
        self.withLearn = True
        self.debugMode = debugMode

    # Look further ahead?

    def boolState(self, State, player): # 2D
        state = copy.deepcopy(State)
        for i in range(self.size):
            for j in range(self.size):
                if state[i,j] == player:
                    state[i,j] = 1
                elif state[i,j] != 0:
                    state[i,j] = -1
        return state

    def nextState(self, state, move, change=1):
        newState = copy.deepcopy(state)
        newState[move] = change
        return newState

    def bestQ(self, state, possibleMoves, returnVal=False):
        bestMove, bestVal = random.choice(possibleMoves), 0
        for move in possibleMoves:
            val = self.Q.get((str(state), move), 0)
            if val > bestVal:
                # print val, "VALLLLLLLLLL", move, state
                bestMove, bestVal = move, val
        if returnVal:
            return bestVal
        return bestMove

    def updateQVal(self, state, move, val):
        currentVal = self.Q.get((str(state), move), 0)
        self.Q[str(state), move] = currentVal + self.learningRate * (val - currentVal)

    def action(self, state, turn, playerNum, possibleMoves):
        state = self.boolState(state, playerNum)
        move = (0, 0)
        if random.random() < self.randomness:
            move = random.choice(possibleMoves)
        else:
            move = self.bestQ(state, possibleMoves) # possibly implement a random choice with weighted distribution?
        if self.withLearn: self.updateQ(state, possibleMoves, move)
        return move

    def updateQ(self, state, possibleMoves, move):
        if self.debugMode: print "move" + str(move)
        if len(possibleMoves) <= 1:
            if self.debugMode: print "moves", possibleMoves
            return
        newState = np.negative(self.nextState(state, move))
        newMoves = copy.deepcopy(possibleMoves)
        newMoves.remove(move)
        val = self.bestQ(newState, newMoves, returnVal=True) # Opponent's best move
        # if val < 0.99 and val != 0: print "NNEEPOSIBF", val
        val *= -self.discountRate
        if self.debugMode: print val
        self.updateQVal(state, move, val)

    def end(self, reward, winner, playerNum, state, move):
        state = self.boolState(state, playerNum)
        oldState = np.negative(self.nextState(state, move, change=0))
        self.R[(str(oldState), move)] = reward
        self.updateQVal(oldState, move, reward)
        # if self.debugMode: print self.Q.values()

    def train(self, iterations, withRand=True):
        agents = [self, main.RandomChoose(self.boardParams)]
        train = Board(boardParams)
        train.setAgents(agents)
        trainWins = train.runGames(numGames=iterations)
        return trainWins

    def test(self, numGames, withRand=False, withLearn=False):
        if withLearn:
            wasWin = copy.deepcopy(self.withLearn)
            self.withLearn = False
        if withRand:
            wasRand = copy.deepcopy(self.randomness)
            self.randomness = 0
        agents = [self, main.RandomChoose(self.boardParams)]
        test = Board(boardParams)
        test.setAgents(agents)
        firstWins = test.runGames(numGames=numGames, shuffle=False).count(1)
        agents = [agents[1], agents[0]]
        test.setAgents(agents)
        secondWins = test.runGames(numGames=numGames, shuffle=False).count(2)
        if withLearn:
            self.withLearn = wasWin
        if withRand:
            self.randomness = wasRand
        return firstWins + secondWins #Only tests second player position currently


boardParams = main.boardParams
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}



deterministic = Q(boardParams, randomness=0.001)
normal = Q(boardParams, randomness=0.2)
rand = Q(boardParams, randomness=0.8)

print normal.test(100)
normal.train(3000)
print normal.test(100)

normal.debugMode = True
agents = main.compileAgents(boardParams, numHuman=1) + [normal]
interactiveTest = Board(boardParams, debugMode=True)
interactiveTest.setAgents(agents)
interactiveTest.runGames(10)

# for agent in [normal]:#[deterministic, normal, rand]:
#     agents = main.compileAgents(boardParams, numRand=1) + [agent]
#
#     test = Board(boardParams)
#     test.setAgents(agents)
#     testWins = test.runGames(numGames=100)
#     print testWins.count(2)
#
#     train = Board(boardParams) #, debugMode=True)
#     train.setAgents(agents)
#     trainWins = train.runGames(numGames=10000)
#     print trainWins.count(2)
#     #
#     agents[1].randomness = 0.001
#     test = Board(boardParams)
#     test.setAgents(agents)
#     testWins = test.runGames(numGames=100)
#     print testWins.count(2)
#
