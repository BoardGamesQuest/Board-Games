#import the players/algorithms here
from SushiGo import SushiGoBoard
from MachineLearning2 import Learner2
from SamplePlayer2 import Sample2
game = SushiGoBoard(numPlayers=4, debugMode=False)
# game.setAgents(numHuman=1, numLearner=1)
game.run()
agent = Sample2(0, game.numPlayers)
# game.setAgents(agents=agent)


print game.test(agent)
