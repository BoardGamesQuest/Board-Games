import numpy as np
from abc import ABCMeta, abstractmethod
import re, random, copy
from board import Board, boardParams
from Agents.compileAgents import Agent, Human, RandomChoose, Minimax, compileAgents
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}




ticTac = Board(boardParams, debugMode=True)
agents = compileAgents(boardParams)
ticTac.setAgents(agents)
ticTac.runGames()
