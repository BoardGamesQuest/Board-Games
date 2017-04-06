#import the players/algorithms here
from SushiGo import SushiGoBoard
from MachineLearning2 import Learner2
from SamplePlayer import Sample
from CardEval import CardEvaluator
from SamplePlayer2 import Sample2
game = SushiGoBoard(numPlayers=4, debugMode=True)

# game.setAgents(numLearner=1)
# game.setAgents(numHuman=1, numLearner=1)

# cardEval = CardEvaluator(0, game.numPlayers, game)
# game.setAgents(agents=cardEval, numLearner=1)

# game.run()
agent = CardEvaluator(0, game.numPlayers, game)
# game.setAgents(agents=agent)
game.setAgents(agents=agent, numHuman=1)
game.run()
#print game.test(agent)
