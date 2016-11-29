import numpy as np
from abc import ABCMeta, abstractmethod

class Board:
    def __init__(self, agents, numPlayers=2, size=3, dimension=2, debug=False, limit=10):
        self.agents, self.numPlayers, self.size, self.dimension, self.limit = agents, numPlayers, size, dimension, limit
        self.state = np.zeros(tuple([size]*dimension), dtype=np.int)
        self.rowIndices = self.findRowIndeces()
        self.emptyIndices = self.rowIndices[:self.size] # Unfinished. Quick way to know which spaces are empty
        print self.run(doPrint=debug)

    def compileAgents

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
    def __init__(self, numPlayers, size, dimension, limit, debug=False):
        self.numPlayers, self.size, self.dimension, self.limit = numPlayers, size, dimension, limit

    @abstractmethod
    def action(self, state, turn, playerNum):
        return [0]*self.dimension


class randomChoose(Agent):
    def __init__(self, boardParams, debug=False):
        super().__init__(*boardParams, debug=debug)

    def action(self, state, turn, playerNum):
        for i in range(self.size):
            for j in range(self.size):s
                if state[i,j] == 0:
                    if debug: print i,j
                    return (i,j)
agents = []
boardParams = []
for i in range(3):
    agents.append(randomChoose(boardParams))
print agents
ticTac = Board(agents, numPlayers=3, debug=True)
# ticTac.display()
# ticTac.act((1,1))
ticTac.display()
# ticTac.checkWin()
