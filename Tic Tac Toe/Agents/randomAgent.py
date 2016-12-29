import random
from abstractAgent import Agent

class RandomChoose(Agent):

    def action(self, board, state, turn, playerNum, legalMoves):
        # availableSpots = []
        # for i in range(self.size):
        #     for j in range(self.size):
        #         if state[i,j] == 0:
        #             availableSpots.append((i,j))
        #             if self.debugMode: print i,j
        return random.choice(legalMoves)
