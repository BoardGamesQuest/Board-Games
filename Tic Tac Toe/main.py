from board import Board, boardParams
from Agents.compileAgents import Agent, Human, RandomChoose, Minimax, compileAgents
# boardParams = {"numPlayers" : 2, "size" : 3, "dimension" : 2, "limit" : 10}
from Agents.turnBasedQ import Q
# from Agents.randomAgent import  


ticTac = Board(boardParams, debugMode=True)
agents = compileAgents(boardParams)
# agents = []
ticTac.setAgents(agents)
ticTac.runGames()
