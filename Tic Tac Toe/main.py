import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, copy

boardParams = [2, 3, 2, 10]
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}

class Board:
    def __init__(self, boardParams=boardParams, debugMode=False):
        if type(boardParams) == hash:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams["numPlayers"], boardParams["size"], boardParams["dimension"], boardParams["limit"] # **boardParams
        elif type(boardParams) == list:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams[0], boardParams[1], boardParams[2], boardParams[3] # *boardParams
        else:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams

        self.debugMode = debugMode
        self.rowIndices, self.allIndices = self.findRowIndices() # A list of all the rows, where each row is represented by a list of the positions of its elements
        self.winners = [] # record of who won every game
        self.reset()

    def setAgents(self, agents):
        self.agents = agents

    def reset(self):
        self.currentPlayer = 1
        self.state = np.zeros(tuple([self.size]*self.dimension), dtype=np.int)
        self.emptyIndices = copy.deepcopy(self.allIndices)

    def display(self):
        print self.state

    def findRowIndices(self):
        # Compiles row indices as described in __init__
        # Currently only 2d
        rows, diag1, diag2, total = [], [], [], []
        for i in range(self.size):
            row, column = [], []
            for j in range(self.size):
                total.append((i,j))
                row.append((i,j))
                column.append((j,i))
            rows.append(row)
            rows.append(column)
            diag1.append((i,i))
            diag2.append((i,self.size-i-1))
        rows.append(diag1)
        rows.append(diag2)
        return rows, total

    def act(self, position):
        if position in self.emptyIndices: # Valid move
            self.state[position] = self.currentPlayer
            self.emptyIndices.remove(position)
            return True
        return False

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
        # if len(self.emptyIndices) == 0:
        #     return 0

        return "no winner"

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

            boardInfo = (self.state, turn, self.currentPlayer, self.emptyIndices) # self.emptyIndices, self.rowIndices)
            move = self.agents[self.currentPlayer-1].action(*boardInfo)
            if type(move) != tuple: move = tuple(move)
            moveIsLegal = self.act(move)

            if not moveIsLegal:
                for i in xrange(self.limit):
                    if self.debugMode: print "Invalid Move by Player {}".format(self.currentPlayer)
                    self.agents[self.currentPlayer-1].illegal(move)
                    move = self.agents[self.currentPlayer-1].action(*boardInfo)
                    if type(move) != tuple: move = tuple(move)
                    moveIsLegal = self.act(move)
                    if moveIsLegal: break
                else: # If loop not broken
                    if self.debugMode: print "Too many invalid moves. Terminating game"
                    return False

            if self.debugMode: self.display()

            winner = self.checkWin()
            if type(winner) == int: # checkWin returns None type if there is no winner, 0 for a tie, and playerNum for victory
                if self.debugMode: self.printEnd(winner)
                for i in range(self.numPlayers):
                    if i == winner:
                        self.agents[i].end(1, self.currentPlayer, i, self.state, move)
                    else:
                        self.agents[i].end(-0.9, self.currentPlayer, i, self.state, move)
                return winner

            self.currentPlayer = (self.currentPlayer % self.numPlayers) + 1

        if self.debugMode: self.printEnd(0)
        for i in range(self.numPlayers):
            self.agents[i].end(0, self.currentPlayer, i, self.state, move)
        return 0

    def runGames(self, numGames=1, shuffle=True):
        for i in xrange(numGames):
            if i % 100 == 99:
                print "RUNNING GAME: ", i+1
            if shuffle: random.shuffle(self.agents)
            self.winners.append(self.run())
            self.reset()
        if self.debugMode: print self.winners
        return self.winners



class Agent:
    # A structure for agents.
    # Your program should inherit this (as seen in RandomChoose), meaning that it should have an action(self, state, turn, playerNum) that returns a position (an array self.dimension long)
    # We should probably find a way to restrict the output of action
    __metaclass__ = ABCMeta
    def __init__(self, boardParams, debugMode=False):
        self.numPlayers, self.size, self.dimension, self.limit = self.boardParams = boardParams
        self.debugMode = debugMode

    def illegal(self, move):
        return

    def end(self, reward, winner, playerNum, state, move):
        return

    @abstractmethod
    def action(self, state, turn, playerNum, legalMoves):
        return [0]*self.dimension


class RandomChoose(Agent):

    def action(self, state, turn, playerNum, legalMoves):
        # availableSpots = []
        # for i in range(self.size):
        #     for j in range(self.size):
        #         if state[i,j] == 0:
        #             availableSpots.append((i,j))
        #             if self.debugMode: print i,j
        return random.choice(legalMoves)

class Human(Agent):

    def action(self, state, turn, playerNum, legalMoves):
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

# ticTac = Board(boardParams, debugMode=True)
# agents = compileAgents(boardParams, numRand=2, numHuman=0)
# ticTac.setAgents(agents)
# ticTac.runGames()
