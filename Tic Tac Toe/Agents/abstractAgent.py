from abc import ABCMeta, abstractmethod



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
    def action(self, board, state, turn, playerNum, legalMoves):
        return [0]*self.dimension
