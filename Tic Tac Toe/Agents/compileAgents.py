from abstractAgent import Agent
from humanAgent import Human
from randomAgent import RandomChoose


def compileAgents(boardParams, numRand=0, numHuman=0):
    agents = []
    for i in range(numRand):
        agents.append(RandomChoose(boardParams))
    for i in range(numHuman):
        agents.append(Human(boardParams))
    return agents
