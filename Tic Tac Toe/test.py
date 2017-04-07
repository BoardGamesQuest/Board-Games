from board import Board, boardParams
from Agents.turnBasedQ import Q
import numpy as np

# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}



# deterministic = Q(boardParams, randomness=0.001)
board = Board(boardParams)
alg = Q(boardParams)
# print board.test(alg, 500)
# board.train(alg, numGames=50000)
# print board.test(alg, 500)
alg.Q = np.load("q.npy")
print len(alg.Q)
board.interactiveTest(alg)
# rand = Q(boardParams, randomness=0.8)
# agents = [deterministic, normal, rand]


# print "learningRate, discountRate, originalPerformance, finalPreformannce"
# for learningRate in [0.001, 0.01, 0.1, 1]: #0.001 is really bad with 200 iterations
#     for discountRate in [0.5, 0.75, 1]:
#         agent = Q(boardParams, learningRate=learningRate, discountRate=discountRate)
#         originalPerformance = agent.test(50)
#         agent.randomness = 0.8
#         agent.train(20000)
#         agent.randomness = 0
#         finalPreformannce = agent.test(500)
#         print learningRate, discountRate, originalPerformance, finalPreformannce
