import numpy as np

class board:
    # TODO:
    #   Make an efficient clone
    #   Standardize errors (like logkitten)
    #       Type errors (could we just expect that they don't happen? Only for debugging)
    #       Invalid moves
    # Move this To Do stuff into readme?

    def __init__(numPlayers=2, size=3, dimension=2, debug=False):
        self.numPlayers, self.size, self.dimension = numPlayers, size, dimension
        self.state = np.zeros(*[size]*dimension)

    def act(self, player, position):
        if self.state[*position] != 0:
            print "Invalid Move: {} by Player {}".format(position, player)
            return
        self.state[*position] = player2

    def checkWin(self):
        rows = [] #generate rows
        diag1 = []
        diag2 = []
        for i in range(size):
            rows.append(self.state(i,:))
            rows.append(self.state(:,i))
            diag1.append(self.state(i,i))
            diag2.append(self.state(i,size-i))
        rows.append(diag1)
        rows.append(diag2)
        for row in rows
            player = row[0]
            if all(map(lambda i: i == player, row[0:])):
                return player
            #eliminate possible rows?
