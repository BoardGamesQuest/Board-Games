import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, main
from main import Agent, Board

boardParams = main.boardParams
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}

class Q(Agnet):
    def __init__(self, boardParams, learningRate=0.1, discountRate=0.99, randomness=0.4, debugMode=False):
        super(NeuralCoords, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        self.qVals = np.zeros((self.size,)*self.dimension + (self.numPlayers+1) + (self.size,)*self.dimension) # First is for current state, second is for action # Use dictionary

    # Should the Q function only calculate when it's about to be my turn? Yes
    def action(self, state, turn, playerNum, possibleMoves):
        bestMove = (0)*dimension
        bestVal = 0
        for move in possibleMoves:
            val = self.qVals[*self.state, *move]
            if val > bestVal
                bestVal = val
                bestMove = move


class NeuralCoords(Agent):
    def __init__(self, boardParams, debugMode=False, numHidden=1, learningRate=3):
        super(NeuralCoords, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.numHidden = learningRate, numHidden
        self.inputLength = self.size*2 + 2
        self.initializeWeights()

    # Input a list of rows (8 long, or size*2 + 2)
    # List of rows dotted with params in first layer? (loses some information)
    # Neural netted
    # Output? 9 neurons for classification? 2 neurons for coordinate of position?
    def initializeWeights(self):
        self.firstW = np.random.rand(self.inputLength, self.inputLength, self.size) # Add biases per row dotted? per neuron?
        self.firstB = np.random.rand(self.inputLength, self.inputLength)
        self.hidW = np.random.rand(self.numHidden, self.inputLength, self.inputLength)
        self.hidB = np.random.rand(self.numHidden, self.inputLength)
        self.outW = np.random.rand(self.dimension, self.inputLength)
        self.outB = np.random.rand(self.dimension)

    def compute(self, X, allActivations=False):
        firstActs = np.array()
        for n in range(inputLength):
            firstActs.append(np.dot(firstW[n], X))

class NeuralQ(Agent):
    def __init__(self, boardParams, debugMode=False, numHidden=1, learningRate=3):
        super(NeuralQ, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.numHidden = learningRate, numHidden
        self.inputLength = self.size*2 + 2
        self.initializeWeights()

    # Input a list of rows (8 long, or size*2 + 2)
    # List of rows dotted with params in first layer? (loses some information)
    # Neural netted
    # Output? 9 neurons for classification? 2 neurons for coordinate of position?
    def initializeWeights(self):
        self.firstW = np.random.rand(self.inputLength, self.inputLength, self.size) # Add biases per row dotted? per neuron?
        self.firstB = np.random.rand(self.inputLength)
        self.hidW = np.random.rand(self.numHidden, self.inputLength, self.inputLength)
        self.hidB = np.random.rand(self.numHidden, self.inputLength)
        self.outW = np.random.rand(self.inputLength)
        self.outB = np.random.rand()

    def compute(self, X, allActivations=False):
        firstActs = np.array()
        for n in range(inputLength):
            comps = np.dot(firstW[n], np.transpose(X))
            firstActivations =  = np.add(np.sum(comps, axis=1), firstB)
            firstActs.append()

            # for i in range(inputLength):
            #     dot = np.dot(X[i], firstW[n][i])


        for layer in self.W:
            y = np.array([np.dot(x, w[1:]) + w[0] for w in layer])
            y = np.reciprocal(np.add(np.exp(np.negative(y)), 1))
            if allActivations:
                X = np.concatenate((X, np.transpose([[yi] for yi in y])))
            x = y
        if allActivations:
            return X
        return x

    def backprop(self, x, y):
        activations = self.efficientCompute(x, allActivations=True)
        delta = np.empty((self.numLayers, self.height))
        dCost = np.subtract(activations[self.numLayers], y)
        dActivations = np.multiply(activations, np.subtract(1, activations))
        delta[self.numLayers-1] = np.multiply(dCost, dActivations[self.numLayers])
        for layer in reversed(range(self.numLayers-1)):
            delta[layer] = np.multiply(np.dot(np.transpose(self.W[layer+1,:,1:]), delta[layer+1]), dActivations[layer+1])
        self.W[:,:,0] = np.subtract(self.W[:,:,0], delta)
        self.W[:,:,1:] = np.subtract(self.W[:,:,1:], self.learningRate * np.multiply(activations[1:], delta))

    def normalizeInput(state, playerNum):
        for i in range(self.size):
            for j in range(self.size):
                if not (state[i,j] == 0 or state[i,j] == playerNum):
                    state[i,j] = -1 # Only two player
        return state

    def action(self, state, turn, playerNum):
        state = normalizeInput(state, playerNum)






def compileAgents(boardParams, numRand=0, numHuman=0):
    agents = []
    for i in range(numRand):
        agents.append(RandomChoose(boardParams))
    for i in range(numHuman):
        agents.append(human(boardParams))
    return agents

ticTac = Board(boardParams, debugMode=True)
agents = compileAgents(boardParams, numRand=2)
ticTac.setAgents(agents)
