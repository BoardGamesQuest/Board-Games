import numpy as np
import random, copy
from abstractAgent import Agent

class Q(Agent):
    def __init__(self, boardParams, learningRate=0.1, discountRate=0.9, randomness=0.2, debugMode=False):
        super(Q, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        self.Q, self.R = {}, {}
        self.debugMode = debugMode

    # def updateQ(state, move):
    #     Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
    #     currentVal = self.Q.get((str(state), move), 0)
    #     self.Q[(str(state), move)] = currentVal + self.learningRate * (val - currentVal)

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
        strState = str(state)
        vals = [self.Q.get((strState, move), 0) for move in possibleMoves]
        sortedVals = np.argsort(vals)
        bestValIndex = sortedVals[-1]
        return possibleMoves[bestValIndex]

    # def trainAction(self, state, possibleMoves, numEmpty):
    #     move = possibleMoves.pop(random.randrange(numEmpty)) # make not always random? # possibly implement a random choice with weighted distribution?
    #     if len(possibleMoves) <= 1:
    #         return move
    #     newState = np.negative(self.nextState(state, move))
    #     newMoves = copy.deepcopy(possibleMoves)
    #     newMoves.remove(move)

    def train(self, state, oldState, move, possibleMoves):
        strState, strOldState = str(state), str(oldState)
        val = np.amax([self.Q.get((strState, possibleMove), 0) for possibleMove in possibleMoves])
        val = np.multiply(val, np.negative(self.discountRate))
        currentVal = self.Q.get((strOldState, move), 0)
        self.Q[(strOldState, move)] = np.add(currentVal, np.multiply(self.learningRate, np.subtract(val, currentVal)))

    def action(self, board, state, turn, playerNum, possibleMoves):
        state = self.boolState(state, playerNum)
        return self.bestQ(state, possibleMoves) 


    # def end(self, reward, winner, playerNum, state, move):
    #     state = self.boolState(state, playerNum)
    #     oldState = np.negative(self.nextState(state, move, change=0))
    #     self.R[(str(oldState), move)] = reward
    #     self.updateQVal(oldState, move, reward)
        # if self.debugMode: print self.Q.values()

    def won(self, state, move, winner):
        self.Q[(str(state), move)] = winner

