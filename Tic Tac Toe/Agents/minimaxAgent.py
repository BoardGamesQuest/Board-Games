import copy, math
from abstractAgent import Agent

class Minimax(Agent):
    def action(self, board, state, turn, playerNum, legalMoves):
        temp = ([],50)
        # print legalMoves
        for i in legalMoves:
            newBoard = copy.deepcopy(board)
            newBoard.act2(i)
            # print self.scoreState(newBoard, (playerNum%2)+1)
            if self.scoreState(newBoard, (playerNum%2)+1)<temp[1]:
                temp = (i,self.scoreState(newBoard,(playerNum%2)+1))
        # newBoard = copy.deepcopy(board)
        # newBoard.act2(temp[0])
        # self.scoreStateDebug(newBoard, (playerNum%2)+1)
        # print temp
        return temp[0]


    def scoreState(self, board, toMove):
        if type(board.checkWin()) != int:
            scores = []
            for i in board.emptyIndices:
                newBoard = copy.deepcopy(board)
                newBoard.act2(i)
                scores.append(-self.scoreState(newBoard, (toMove%2)+1))
            return (abs(max(scores))-1)*cmp(max(scores),0)
        elif board.checkWin() == 0:
            return 0
        elif board.checkWin() == toMove:
            return 10
        return -10

    # def scoreStateDebug(self, board, toMove):
    #     print board.emptyIndices
    #     if type(board.checkWin()) != int:
    #         scores = []
    #         for i in board.emptyIndices:
    #             newBoard = copy.deepcopy(board)
    #             newBoard.act2(i)
    #             scores.append(-self.scoreStateDebug(newBoard, (toMove%2)+1))
    #         print (abs(max(scores))-1)*cmp(max(scores),0)
    #         return (abs(max(scores))-1)*cmp(max(scores),0)
    #     elif board.checkWin() == 0:
    #         print 0
    #         return 0
    #     elif board.checkWin() == toMove:
    #         print 10
    #         return 10
    #     print -10
    #     return -10
