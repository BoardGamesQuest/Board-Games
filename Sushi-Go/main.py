#import the players/algorithms here
from SushiGo import SushiGoBoard
from MachineLearning2 import Learner2
from SamplePlayer2 import Sample2
#from CardEval import CardEvaluator
game = SushiGoBoard(numPlayers=4, debugMode=True)

game.setAgents(numLearner=1)
# game.setAgents(numHuman=1, numLearner=1)

# cardEval = CardEvaluator(0, game.numPlayers, game)
# game.setAgents(agents=cardEval, numLearner=1)

game.run()
#agent = Sample2(0, game.numPlayers)
# game.setAgents(agents=agent)


#print game.test(agent)
