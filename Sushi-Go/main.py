import copy
import random
import numpy as np
from Deck import *
from Cards import *
#import the players/algorithms here
from SamplePlayer import Sample
from SushiGo import SushiGoBoard

game = SushiGoBoard([2,3], True)
game.run()
