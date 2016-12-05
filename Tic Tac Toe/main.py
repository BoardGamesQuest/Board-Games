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

    def act(self, position):
        if type(position) != tuple:
            position = tuple(position)
        if self.isLegal(position, self.currentPlayer):
            self.state[position] = self.currentPlayer
            return True # Valid move
        return False

    def isLegal(self, position, player):
        if len(position) != self.dimension:
            return False
        for i in position:
            if i >= self.size or i < 0:
                return False
        if self.state[position] != 0:
            return False # Position taken, invalid move
        return True

    def checkWin(self):
        # TODO: Optimize knowing the last move and player who made it, only check the appropriate rows. If all full, run checkTie()
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
                for i in xrange(self.limit):
                    if self.debugMode: print "Invalid Move by Player {}".format(self.currentPlayer)
                    self.agents[self.currentPlayer-1].illegal(move)
                    move = self.agents[self.currentPlayer-1].action(*boardInfo)
                    moveIsLegal = self.act(move)
                    if moveIsLegal: break
                if self.debugMode: print "Too many invalid moves. Terminating game"
                return False
            if self.debugMode:
                self.display()
            winner = self.checkWin()
            if type(winner) == int: # checkWin returns None type if there is no winner, 0 for a tie, and playerNum for victory
                if self.debugMode: self.printEnd(winner)
                if winner == 0:
                    for i in range(self.numPlayers):
                        self.agents[i].end(0)
                for i in range(self.numPlayers):
                    if i == winner:
                        self.agents[i].end(1)
                    else:
                        self.agents[i].end(-1)
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
    def __init__(self, boardParams, debugMode=False):
        self.numPlayers, self.size, self.dimension, self.limit = boardParams
        self.debugMode = debugMode

    def illegal(self, move):
        return

    def end(self, reward):
        return

    @abstractmethod
    def action(self, state, turn, playerNum):
        return [0]*self.dimension


class RandomChoose(Agent):

    def action(self, state, turn, playerNum):
        availableSpots = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i,j] == 0:
                    availableSpots.append((i,j))
                    if self.debugMode: print i,j
        return random.choice(availableSpots)

class Human(Agent):

    def action(self, state, turn, playerNum):
        # print "Current State"
        # print state
        userInput = raw_input('It\'s turn {}. Your Move, Player {}: '.format(turn, playerNum))
        # Cleaning input to standardized form
        # userInput.replace(userInput, r"$[0-9]* $[0-9]*", r"\1,\2") # fix for higher dimension
        # userInput = re.replace(userInput, r"\[\] ", "")
        position = userInput.split(',')
        for i in range(len(position)):
            position[i] = int(position[i])
        return position

def compileAgents(boardParams, numRand=0, numHuman=0):
    agents = []
    for i in range(numRand):
        agents.append(RandomChoose(boardParams))
    for i in range(numHuman):
        agents.append(Human(boardParams))
    return agents

ticTac = Board(boardParams, debugMode=True)
agents = compileAgents(boardParams, numRand=1, numHuman=1)
ticTac.setAgents(agents)