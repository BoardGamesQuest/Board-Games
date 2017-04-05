#import the players/algorithms here
from SushiGo import SushiGoBoard

game = SushiGoBoard([4,3], False)
game.setAgents(numHuman=1, numLearner=1)
game.run()
