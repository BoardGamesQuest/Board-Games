import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, copy
from board import Board, boardParams
from Agents.compileAgents import Agent, Human, RandomChoose, compileAgents
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}




ticTac = Board(boardParams, debugMode=True)
agents = compileAgents(boardParams, numRand=1, numHuman=1)
ticTac.setAgents(agents)
ticTac.runGames()
