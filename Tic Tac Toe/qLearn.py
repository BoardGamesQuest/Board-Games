import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, main
from main import Agent, Board

boardParams = main.boardParams
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}



ticTac = Board(boardParams, debugMode=True)
agents = main.compileAgents(boardParams, numRand=1) + [Q(boardParams)]
ticTac.setAgents(agents)
ticTac.runGames()

class Q(Agent):
    def __init__(self, boardParams, learningRate=1, discountRate=1, randomness=0.2, debugMode=False):
        super(NeuralCoords, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        # self.qVals = np.zeros((self.size,)*self.dimension + (self.numPlayers+1) + (self.size,)*self.dimension) # First is for current state, second is for action
        self.qVals = {}

    # Should the Q function only calculate when it's about to be my turn? Yes
    # Look further ahead?

    def boolState(self, state, player): # 2D
        for i in range(self.size):
            for j in range(self.size):
                if state[i,j] == player:
                    state[i,j] = 0
                elif state != 0:
                    state[i,j] = -1
        return state

    def nextState(self, state, move):
        state[move] = 1

    def bestQVal(self, state, possibleMoves):
        bestMove = possibleMoves[0]
        bestVal = self.qVals.get((state, bestMove), default=0)
        for move in possibleMoves[1:]:
            val = self.qVals.get((state, move), default=0)
            if val > bestVal:
                bestMove = move
                bestVal = val
        return bestVal #, bestMove

    def action(self, state, turn, playerNum, possibleMoves):
        state = self.boolState(state, playerNum)
        bestMove = bestTotalVal = bestVal = bestNextVal = 0
        for i in range(len(possibleMoves)):
            val = self.qVals.get((state, possibleMoves[i]), default=0)
            newState = np.negative(self.nextState(state, possibleMoves[i]))
            newMoves = possibleMoves[:i] + possibleMoves[i+1:]
            nextVal = self.discountRate * bestQVal(newState, newMoves) # Opponent's best move
            totalVal = val - nextVal
            if totalVal > bestTotalVal:
                bestMove, bestTotalVal, bestVal, bestNextVal = i, totalVal, val, nextVal
        bestMove = possibleMoves[bestMove]
        self.qVals[state, bestMove] = bestVal + self.learningRate * (bestTotalVal - bestVal)
        return possibleMoves[bestMove]

    def end(self, reward, winner, playerNum, state, move):
        state = self.boolState(state, playerNum)
        self.qVals[(state, move)] = reward
