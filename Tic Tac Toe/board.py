# import numpy as np

class board:
    # TODO:
    #   Make an efficient clone
    #   Standardize errors (like logkitten)
    #       Type errors (could we just expect that they don't happen? Only for debugging)
    #       Invalid moves
    # Move this To Do stuff into readme?

    def __init__(numPlayers=2, size=3, dimension=2, debug=False):
        self.numPlayers, self.size, self.dimension = numPlayers, size, dimension
        # self.state = np.zeros(*[size]*dimension)
        state = [0]*size
        for i in range(dimension):
            state = [state] * size
        self.state = state

    def tile(position):
        # if len(position) != dimension
        out = self.state
        for index in position:
            out = out[index]
        return out

    def act(player, position):
        activeTile = tile(position)
        if activeTile != 0:
            print "Invalid Move: {} by Player {}".format(position, player)
            return
