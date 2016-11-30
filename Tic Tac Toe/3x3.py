import numpy as np
from abc import ABCMeta, abstractmethod
import re

class Board:
    def __init__(self, agents, boardParams=[2, 3, 2, 10], debugMode=False):
        if type(boardParams) == hash:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams["numPlayers"], boardParams["size"], boardParams["dimension"], boardParams["limit"] # **boardParams
        elif type(boardParams) == list:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams[0], boardParams[1], boardParams[2], boardParams[3] # *boardParams
        self.agents = agents #work on initializing agents
        self.state = np.zeros(tuple([self.size]*self.dimension), dtype=np.int)
        self.rowIndices = self.findRowIndeces()
        self.emptyIndices = self.rowIndices[:self.size] # Unfinished. Quick way to know which spaces are empty
        print self.run(doPrint=debugMode)

    # def compileAgents

    def findRowIndeces(self):
        # Compile a list of all the rows, where each row is represented by a list of the positions of its elements
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

    def display(self):
        print self.state

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
        # Checks if there is empty room left
        # TODO: Can be optimized - just do when turns run out. Also, can use info from the for loop above.
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i,j] == 0:
                    return
        return 0

    def end(self, winner):
        if winner == 0:
            print "TIE:\n", self.state
        else:
            print winner, "WON"

    def run(self, doPrint=False):
        self.currentPlayer = 1

        for turn in range(self.size ** self.dimension):
            if doPrint: print "Player {}, make your move.".format(self.currentPlayer)

            boardInfo = (self.state, turn, self.currentPlayer) # self.emptyIndices, self.rowIndices)
            move = self.agents[self.currentPlayer-1].action(*boardInfo)
            moveIsLegal = self.act(move)

            if not moveIsLegal:
                if doPrint: print "Invalid Move by Player {}".format(self.currentPlayer)
                for i in xrange(self.limit):
                    move = self.agents[self.currentPlayer-1].action(*boardInfo)
                    moveIsLegal = self.act(move)
                    if moveIsLegal: break
                if doPrint: print "Too many invalid moves. Terminating game"
                return False

            winner = self.checkWin()
            if type(winner) == int:
                self.end(winner)
                return winner

            self.currentPlayer = (self.currentPlayer % self.numPlayers) + 1



class Agent:
    # A structure for agents. Your program should inherit this (as seen in randomChoose), meaning that it should
    __metaclass__ = ABCMeta
    def __init__(self, numPlayers, size, dimension, limit, debugMode=False):
        self.numPlayers, self.size, self.dimension, self.limit = numPlayers, size, dimension, limit
        self.debugMode = debugMode

    @abstractmethod
    def action(self, state, turn, playerNum):
        return [0]*self.dimension


class randomChoose(Agent):
    def __init__(self, boardParams, debugMode=False):
        print boardParams
        super(randomChoose, self).__init__(*boardParams, debugMode=debugMode)

    def action(self, state, turn, playerNum):
        for i in range(self.size):
            for j in range(self.size):
                if state[i,j] == 0:
                    if self.debugMode: print i,j
                    return (i,j)

class human(Agent):
    def __init__(self, boardParams, debugMode=False):
        super().__init__(boardParams, debugMode=debugMode)

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


agents = []
boardParams = [2, 3, 2, 10]
# [numPlayers=2, size=3, dimension=2, limit=10]
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}
for i in range(3):
    agents.append(randomChoose(boardParams))
print agents
ticTac = Board(agents, boardParams, debugMode=True)
# ticTac.display()
# ticTac.act((1,1))
ticTac.display()
# ticTac.checkWin()
