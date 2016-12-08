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
    def __init__(self, boardParams, learningRate=0.1, discountRate=0.99, randomness=0.2, debugMode=False):
        super(NeuralCoords, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        # self.qVals = np.zeros((self.size,)*self.dimension + (self.numPlayers+1) + (self.size,)*self.dimension) # First is for current state, second is for action
        self.qVals = {}

    def qVal(self, state, move):
        return self.qVals.get((state, move), default=0)
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
        bestVal = self.qVal(bestMove)
        for move in possibleMoves[1:]:
            val = self.qVal(state, move)
            if val > bestVal:
                bestMove = move
                bestVal = val
        return bestVal #, bestMove

    def action(self, state, turn, playerNum, possibleMoves):
        state = self.boolState(state, playerNum)
        bestMove = bestVal = 0
        for i in range(len(possibleMoves)):
            val = self.qVal(state, possibleMoves[i])
            newState = np.negative(self.nextState(state, possibleMoves[i]))
            newMoves = possibleMoves[:i] + possibleMoves[i+1:]
            val -= self.discountRate * bestQVal(state, newMoves) # Opponent's best move
            if val > bestVal:
                bestMove, bestVal = i, val
        return possibleMoves[bestMove]

    def end(self, reward, winner, playerNum, state, move):
