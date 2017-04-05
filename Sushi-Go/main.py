#import the players/algorithms here
from SushiGo import SushiGoBoard
from MachineLearning2 import Learner2
game = SushiGoBoard(numPlayers=4, debugMode=True)
# game.setAgents(numHuman=1, numLearner=1)
game.run()

agent = Learner2(0, game.numPlayers)
# print game.test(agent)
