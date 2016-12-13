import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, main, copy
from main import Agent, Board

class Q(Agent):
    def __init__(self, boardParams, learningRate=0.99, discountRate=0.5, randomness=0.2, debugMode=False):
        super(Q, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        self.Q, self.R = {}, {}
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
        state[move] = change
        return state

    def bestQ(self, state, possibleMoves, returnVal=False):
        bestMove, bestVal = possibleMoves[0], 0
        for move in possibleMoves:
            val = self.Q.get((str(state), move), 0)
            if val > bestVal:
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
        self.updateQ(state, possibleMoves, move)
        return move

    def updateQ(self, state, possibleMoves, move):
        if len(possibleMoves) <= 1: return
        newState = np.negative(self.nextState(state, move))
        newMoves = copy.deepcopy(possibleMoves)
        newMoves.remove(move)
        val = np.negative(self.discountRate * self.bestQ(newState, newMoves, returnVal=True)) # Opponent's best move
        if self.debugMode: print val
        self.updateQVal(state, move, val)

    def end(self, reward, winner, playerNum, state, move):
        state = self.boolState(state, playerNum)
        oldState = np.negative(self.nextState(state, move, change=0))
        self.R[(str(oldState), move)] = reward
        self.updateQVal(oldState, move, reward)
        if self.debugMode: print self.Q.values()

    def smartAction(self, state, turn, playerNum, possibleMoves):
        state = self.boolState(state, playerNum)
        bestMove = bestTotalVal = bestVal = bestNextVal = 0
        for i in range(len(possibleMoves)):
            Rval = self.R.get((str(state), possibleMoves[i]), default=0)
            newState = np.negative(self.nextState(state, possibleMoves[i]))
            newMoves = possibleMoves[:i] + possibleMoves[i+1:]
            nextVal = self.discountRate * self.bestQVal(newState, newMoves) # Opponent's best move
            val = Rval - nextVal # nextVal is opponent's Q, so we subtract it
            if val > bestval:
                bestMove, bestVal = i, val
        bestMove = possibleMoves[bestMove]
        currentVal = self.Q.get((str(state), bestMove), default=0)
        self.Q[str(state), bestMove] = currentVal + self.learningRate * (bestVal - currentVal) # Update Q
        return bestMove

boardParams = main.boardParams
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}



deterministic = Q(boardParams, randomness=0.001)
normal = Q(boardParams, randomness=0.2)
rand = Q(boardParams, randomness=0.8)
for agent in [deterministic, normal, rand]:
    agents = main.compileAgents(boardParams, numRand=1) + [agent]

    test = Board(boardParams)
    test.setAgents(agents)
    testWins = test.runGames(numGames=100)
    print testWins.count(2)

    train = Board(boardParams) #, debugMode=True)
    train.setAgents(agents)
    trainWins = train.runGames(numGames=300)
    print trainWins.count(2)

    agents[1].randomness = 0.001
    test = Board(boardParams)
    test.setAgents(agents)
    testWins = test.runGames(numGames=100)
    print testWins.count(2)
    test.debugMode = True
    agents[1].debugMode = True
    test.runGames()



# Testing with discount rate and qvals, I found that the q function is recording reward correctly, but only propogating losses one move and nothing else (sometimes multiple times?) 
