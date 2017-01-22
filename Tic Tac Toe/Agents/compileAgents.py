from abstractAgent import Agent
from humanAgent import Human
from randomAgent import RandomChoose
from minimaxAgent import Minimax

def compileAgents(boardParams, numRand=1, numHuman=0, numMinimax=1):
    agents = []
    for i in range(numRand):
        agents.append(RandomChoose(boardParams))
    for i in range(numHuman):
        agents.append(Human(boardParams))
    for i in range(numMinimax):
        agents.append(Minimax(boardParams))

    return agents

# def compileAgents(boardParams):
#     return [Human(boardParams),minimaxAgent(boardParams)]
