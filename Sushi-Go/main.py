#import the players/algorithms here
from SushiGo import SushiGoBoard
from MachineLearning2 import Learner2
from SamplePlayer import Sample
from CardEval import CardEvaluator
game = SushiGoBoard(numPlayers=4, debugMode=True)
# cardEval = CardEvaluator(0, game.numPlayers, game)
ml = Learner2(0, game.numPlayers)
game.setAgents(agents=ml, numLearner=1)
game.run()
agent = Sample(0, game.numPlayers)
# game.setAgents(agents=agent)


print game.test(agent)
