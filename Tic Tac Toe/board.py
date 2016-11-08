class board:

    def __init__(numPlayers=2, size=3, dimension=2):
        state = [0] * size
        for i in range(dimension):
            state = [state] * size
        self.state = state
        
# test
