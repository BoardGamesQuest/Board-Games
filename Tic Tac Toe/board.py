import numpy as np
import copy, random
boardParams = [2, 3, 2, 10]
class Board:
    def __init__(self, boardParams=boardParams, debugMode=False):
        if type(boardParams) == hash:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams["numPlayers"], boardParams["size"], boardParams["dimension"], boardParams["limit"] # **boardParams
        elif type(boardParams) == list:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams[0], boardParams[1], boardParams[2], boardParams[3] # *boardParams
        else:
            self.numPlayers, self.size, self.dimension, self.limit = boardParams

        self.debugMode = debugMode
        self.rowIndices, self.allIndices = self.findRowIndices() # A list of all the rows, where each row is represented by a list of the positions of its elements
        self.reset()

    def setAgents(self, agents):
        self.agents = agents

    def reset(self):
        self.currentPlayer = 1
        self.state = np.zeros(tuple([self.size]*self.dimension), dtype=np.int)
        self.emptyIndices = copy.deepcopy(self.allIndices)

    def display(self):
        newState = []
        for row in self.state:
            newRow = []
            for element in row:
                if element == 0:
                    newRow.append(' ')
                elif element == 1:
                    newRow.append('X')
                elif element == 2:
                    newRow.append('O')
            newState.append(newRow)

    def findRowIndices(self):
        # Compiles row indices as described in __init__
        # Currently only 2d
        rows, diag1, diag2, total = [], [], [], []
        for i in range(self.size):
            row, column = [], []
            for j in range(self.size):
                total.append((i,j))
                row.append((i,j))
                column.append((j,i))
            rows.append(row)
            rows.append(column)
            diag1.append((i,i))
            diag2.append((i,self.size-i-1))
        rows.append(diag1)
        rows.append(diag2)
        return rows, total

    def act(self, position):
        if position in self.emptyIndices: # Valid move
            self.state[position] = self.currentPlayer
            self.emptyIndices.remove(position)
            return True
        return False

    def act2(self, position):
        if position in self.emptyIndices: # Valid move
            self.state[position] = self.currentPlayer
            self.emptyIndices.remove(position)
            self.currentPlayer = (self.currentPlayer % self.numPlayers) + 1
            return True
        return False

    def checkWin(self):
        # TODO: Optimize knowing the last move and player who made it, only check the appropriate rows. If all full, run checkTie()
        # Checks every row for winner
        for row in self.rowIndices:
            player = self.state[row[0]]
            if player != 0:
                if all(map(lambda i: self.state[i] == player, row[0:])):
                    return int(player)
        # Checks if there is empty room left, and if there isn't, declares a tie (represented as 'player 0' winnning)
        # TODO: Can be optimized - just do when turns run out. Also, can use info from the for loop above.
        if len(self.emptyIndices) == 0:
            return 0

        return "no winner"

    def printEnd(self, winner):
        if winner == 0:
            print "TIE"
        else:
            print winner, "WON"
        self.display()

    def run(self):
        self.reset()
        self.currentPlayer = 1
        for turn in range(self.size ** self.dimension):
            if self.debugMode: print "Player {}, make your move.".format(self.currentPlayer)

            boardInfo = (self, self.state, turn, self.currentPlayer, self.emptyIndices) # self.emptyIndices, self.rowIndices)
            move = self.agents[self.currentPlayer-1].action(*boardInfo)
            if type(move) != tuple: move = tuple(move)
            moveIsLegal = self.act(move)

            if not moveIsLegal:
                for i in xrange(self.limit):
                    if self.debugMode: print "Invalid Move by Player {}".format(self.currentPlayer)
                    self.agents[self.currentPlayer-1].illegal(move)
                    move = self.agents[self.currentPlayer-1].action(*boardInfo)
                    if type(move) != tuple: move = tuple(move)
                    moveIsLegal = self.act(move)
                    if moveIsLegal: break
                else: # If loop not broken
                    if self.debugMode: print "Too many invalid moves. Terminating game"
                    return False

            if self.debugMode: self.display()

            winner = self.checkWin()
            if type(winner) == int: # checkWin returns None type if there is no winner, 0 for a tie, and playerNum for victory
                if self.debugMode: self.printEnd(winner)
                for i in range(self.numPlayers):
                    if i == winner:
                        self.agents[i].end(1, self.currentPlayer, i, self.state, move)
                    else:
                        self.agents[i].end(-0.9, self.currentPlayer, i, self.state, move)
                return winner

            self.currentPlayer = (self.currentPlayer % self.numPlayers) + 1

        if self.debugMode: self.printEnd(0)
        for i in range(self.numPlayers):
            self.agents[i].end(0, self.currentPlayer, i, self.state, move)
        return 0

    def runGames(self, numGames=1, shuffle=True):
        winners = []
        for i in xrange(numGames):
            if i % 100 == 99:
                print "RUNNING GAME: ", i+1
            if shuffle: random.shuffle(self.agents)
            winners.append(self.run())
        if self.debugMode: print winners
        return winners

    def interactiveTest(self, agent):
        from Agents.humanAgent import Human
        oldMode = copy.copy(self.debugMode)
        self.debugMode = True
        self.setAgents([Human(boardParams), agent])
        self.runGames()
        self.debugMode = oldMode

    def test(self, agent, numGames, withRand=False, withLearn=False): #make efficient like train
        from Agents.randomAgent import RandomChoose
        if withLearn:
            wasWin = copy.deepcopy(agent.withLearn)
            agent.withLearn = False
        if withRand:
            wasRand = copy.deepcopy(agent.randomness)
            agent.randomness = 0
        agents = [agent, RandomChoose(boardParams)]
        self.setAgents(agents)
        firstWins = self.runGames(numGames=numGames, shuffle=False)
        agents = [agents[1], agents[0]]
        self.setAgents(agents)
        secondWins = self.runGames(numGames=numGames, shuffle=False)
        if withLearn:
            agent.withLearn = wasWin
        if withRand:
            agent.randomness = wasRand
        return [("wins", firstWins.count(1), secondWins.count(2)), ("losses", firstWins.count(2), secondWins.count(1)), ("ties", firstWins.count(0), secondWins.count(0))]

    def checkWinSpecific(self, state, move):
        if state[(move[0], 0)] == state[(move[0], 1)] == state[(move[0], 2)]:
            return True
        if state[(0, move[1])] == state[(1, move[1])] == state[(2, move[1])]:
            return True
        if move[0] == move[1]:
            if state[(0, 0)] == state[(1, 1)] == state[(2, 2)]:
                return True
        if move[0] == 2 - move[1]:
            if state[(0, 2)] == state[(1, 1)] == state[(2, 0)]:
                return True
        return False

    def train(self, agent, numGames=1000):
        for i in xrange(numGames):
            if i % 1000 == 0:
                print "RUNNING GAME: ", i

            # goingSecond = np.random.choice([True, False])
            # winner = 0
            state = np.zeros([3,3], dtype=np.int)
            emptyIndices = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
            numEmpty = 9

            # Make less random later. Weighted moves
            for turn in xrange(8):
                move = emptyIndices.pop(np.random.randint(numEmpty))
                numEmpty = np.subtract(numEmpty, 1)
                newState = np.negative(state)
                newState[move] = -1
                agent.train(newState, state, move, emptyIndices)
                if self.checkWinSpecific(newState, move):
                    agent.won(state, move, 1)
                    # newState[move] = 0
                    # agent.won(newState, move, -1)
                    break
                state = newState
            else:
                move = emptyIndices[0]
                state[move] = 1
                if self.checkWinSpecific(newState, move):
                    state[move] = 0
                    agent.won(state, move, 1)
                    # agent.won(np.negative(state), move, -1)
                else:
                    agent.won(state, move, 0)

            # if goingSecond:
            #     move = emptyIndices.pop(np.random.randint(numEmpty))
            #     state[move] = -1
            #     numEmpty = np.subtract(numEmpty, 1)

            # for turn in xrange(4):
            #     move = emptyIndices.pop(np.random.randint(numEmpty))
            #     oldState = np.negative(state)
            #     state[move] = 1
            #     if self.checkWinSpecific(state, move):
            #         winner = 1
            #         break
            #     agent.train(state, oldState, move, emptyIndices)
            #     numEmpty = np.subtract(numEmpty, 1)
            #     oldState[move] = 1

            #     move = emptyIndices.pop(np.random.randint(numEmpty))
            #     state[move] = -1
            #     # oldState[move] = 1 train on opponent's rand move. Maybe even just run one move (not 2) until end
            #     if self.checkWinSpecific(state, move):
            #         winner = -1
            #         break
            #     numEmpty = np.subtract(numEmpty, 1)
            # else:
            #     if not goingSecond:
            #         move = emptyIndices[0]
            #         state[move] = 1
            #         if self.checkWinSpecific(state, move):
            #             winner = 1

            # state[move] = 0
            # agent.won(state, move, winner)
