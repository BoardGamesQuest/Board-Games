import numpy as np
from abc import ABCMeta, abstractmethod
import re, random

boardParams = [2, 3, 2, 10]
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}

class Board:
    def __init__(self, boardParams=boardParams, numGames=1, debugMode=False):
        if type(boardParams) == hash:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams["numPlayers"], boardParams["size"], boardParams["dimension"], boardParams["limit"] # **boardParams
        elif type(boardParams) == list:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams[0], boardParams[1], boardParams[2], boardParams[3] # *boardParams

        self.debugMode = debugMode
        self.numGames = numGames
        self.rowIndices = self.findRowIndeces() # A list of all the rows, where each row is represented by a list of the positions of its elements
        self.winners = [] # record of who won every game
        self.reset()

    def setAgents(self, agents):
        self.agents = agents
        self.runGames(self.numGames)

    def reset(self):
        self.currentPlayer = 1
        self.state = np.zeros(tuple([self.size]*self.dimension), dtype=np.int)
        self.emptyIndices = self.rowIndices[:self.size] # Unfinished. Quick way to know which spaces are empty. Possibly send to players in boardInfo

    def display(self):
        print self.state

    def findRowIndeces(self):
        # Compiles row indices as described in __init__
        # Currently only 2d
        rows, diag1, diag2 = [], [], []
        for i in range(self.size):
            row, column = [], []
            for j in range(self.size):
                row.append((i,j))
                column.append((j,i))
            rows.append(row)
            rows.append(column)
            diag1.append((i,i))
            diag2.append((i,self.size-i-1))
        rows.append(diag1)
        rows.append(diag2)
        return rows

    def act(self, position, player=0):
        # Make sure everything is what it needs to be
        if player == 0:
            player = self.currentPlayer
        if type(position) != tuple:
            position = tuple(position)

        if self.state[position] != 0:
            return False # Position taken, invalid move
        self.state[position] = player
        return True # Valid move

    def checkWin(self):
        # Checks every row for winner
        for row in self.rowIndices:
            player = self.state[row[0]]
            if player != 0:
                if all(map(lambda i: self.state[i] == player, row[0:])):
                    return int(player)
        # Checks if there is empty room left, and if there isn't, declares a tie (represented as 'player 0' winnning)
        # TODO: Can be optimized - just do when turns run out. Also, can use info from the for loop above.
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i,j] == 0:
                    return
        return 0

    def printEnd(self, winner):
        if winner == 0:
            print "TIE"
        else:
            print winner, "WON"
        self.display()

    def run(self):
        self.currentPlayer = 1

        for turn in range(self.size ** self.dimension):
            if self.debugMode: print "Player {}, make your move.".format(self.currentPlayer)

            boardInfo = (self.state, turn, self.currentPlayer) # self.emptyIndices, self.rowIndices)
            move = self.agents[self.currentPlayer-1].action(*boardInfo)
            moveIsLegal = self.act(move)

            if not moveIsLegal:
                if self.debugMode: print "Invalid Move by Player {}".format(self.currentPlayer)
                for i in xrange(self.limit):
                    move = self.agents[self.currentPlayer-1].action(*boardInfo)
                    moveIsLegal = self.act(move)
                    if moveIsLegal: break
                if self.debugMode: print "Too many invalid moves. Terminating game"
                return False

            winner = self.checkWin()
            if type(winner) == int: # checkWin returns None type if there is no winner, 0 for a tie, and playerNum for victory
                if self.debugMode: self.printEnd(winner)
                return winner

            self.currentPlayer = (self.currentPlayer % self.numPlayers) + 1

    def runGames(self, numGames):
        for i in xrange(numGames):
            self.winners.append(self.run())
        return self.winners



class Agent:
    # A structure for agents.
    # Your program should inherit this (as seen in RandomChoose), meaning that it should have an action(self, state, turn, playerNum) that returns a position (an array self.dimension long)
    # We should probably find a way to restrict the output of action
    __metaclass__ = ABCMeta
    def __init__(self, numPlayers, size, dimension, limit, debugMode=False):
        self.numPlayers, self.size, self.dimension, self.limit = numPlayers, size, dimension, limit
        self.debugMode = debugMode

    @abstractmethod
    def action(self, state, turn, playerNum):
        return [0]*self.dimension


class RandomChoose(Agent):
    def __init__(self, boardParams, debugMode=False):
        super(RandomChoose, self).__init__(*boardParams, debugMode=debugMode)

    def action(self, state, turn, playerNum):
        availableSpots = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i,j] == 0:
                    availableSpots.append((i,j))
                    if self.debugMode: print i,j
        return random.choice(availableSpots)

class Human(Agent):
    def __init__(self, boardParams, debugMode=False):
        super(Human, self).__init__(boardParams, debugMode=debugMode)

    def action(self, state, turn, playerNum):
        print "Current State"
        print self.state
        userInput = raw_input('It\'s turn {}. Your Move, Player {}: '.format(turn, playerNum))
        # Cleaning input to standardized form
        userInput.replace(userInput, r"$[0-9]* $[0-9]*", r"\1,\2") # fix for higher dimension
        userInput = re.replace(userInput, r"\[\] ", "")
        position = userInput.split(',')
        for i in range(len(position)):
            position[i] = int(position[i])
        return position

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
            activations = np.add(np.sum(comps, axis=1), firstB)
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
