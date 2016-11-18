import numpy as np

class Board:
    # TODO:
    #   Make an efficient clone
    #   Standardize errors (like logkitten)
    #       Type errors (could we just expect that they don't happen? Only for debugging)
    #       Invalid moves
    # Move this To Do stuff into readme?
    currentPlayer = 1
    def __init__(self, numPlayers=2, size=3, dimension=2, debug=False):
        self.numPlayers, self.size, self.dimension = numPlayers, size, dimension
        self.state = np.zeros(tuple([size]*dimension), dtype=np.int)

    def display(self):
        print self.state

    def act(self, position, player=currentPlayer):
        if type(position) != tuple:
            position = tuple(position)
        # print "Player {}, make your move.".format(player)
        if self.state[position] != 0:
            print "Invalid Move: {} by Player {}".format(position, player)
            return
        self.state[position] = player
        # print self.state[position]
        self.currentPlayer = (self.currentPlayer % self.numPlayers) + 1

    def checkWin(self):
        rows = [] #generate rows
        diag1 = []
        diag2 = []
        for i in range(self.size):
            rows.append(self.state[i,:])
            rows.append(self.state[:,i])
            print rows
            diag1.append(self.state[i,i])
            diag2.append(self.state[i,self.size-i-1])
        rows.append(diag1)
        rows.append(diag2)
        for row in rows:
            player = row[0]
            if all(map(lambda i: i == player, row[0:])):
                return player
            #eliminate possible rows?

ticTac = Board(numPlayers=3)
ticTac.display()
ticTac.act((1,1))
ticTac.display()
ticTac.checkWin()
