import numpy as np
import random, copy
from abstractAgent import Agent
# from sknn.mlp import Regressor, Layer

# nn = Regressor(
#     layers=[
#         Layer("Rectifier", units=100),
#         Layer("Linear")],
#     learning_rate=0.02,
#     n_iter=10)
# nn.fit(X_train, y_train)


from sklearn.neural_network import MLPRegressor

data, target = [], []
trainX, testX = data[n:], data[:n]
trainY, testY = target[n:], target[:n]
# TARGET: maximize personal score, maximize score relative to other highest player, equalize scores
network = MLPRegressor(hidden_layer_sizes=(100, ), activation='relu', solver='adam',
                    alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001,
                    power_t=0.5, max_iter=200, shuffle=True, random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

network.fit(trainX, trainY)
print("Training set score: %f" % mlp.score(trainX, trainY))
print("Test set score: %f" % mlp.score(testX, testY))


# Train:
# Make move based on Q with randomness
# Update Q. Train network on STATE -> Discount*MAX(nextState) + Reward
# Continue

# plt

# fig, axes = plt.subplots(4, 4)
# # use global min / max to ensure all weights are shown on the same scale
# vmin, vmax = network.coefs_[0].min(), network.coefs_[0].max()
# for coef, ax in zip(network.coefs_[0].T, axes.ravel()):
#     ax.matshow(coef.reshape(28, 28), cmap=plt.cm.gray, vmin=.5 * vmin,
#                vmax=.5 * vmax)
#     ax.set_xticks(())
#     ax.set_yticks(())

# plt.show()

deckTypes = [('wasabi', 0), ('wasabi', 1), 'nigiri']
# [0, [1,0], [1,1], 2]
def toArray(cards):
    cardTypes = [card.cardType for card in cards]
    array = np.array([cardTypes.count(Type) for Type in deckTypes])
    return array

class neural(Agent):
    def __init__(self, boardParams, learningRate=0.1, discountRate=1, randomness=0.2, debugMode=False):
        super(Q, self).__init__(boardParams, debugMode=debugMode)
        self.learningRate, self.discountRate, self.randomness = learningRate, discountRate, randomness
        self.Q, self.R = {}, {}
        self.debugMode = debugMode
        self. neuralNet = Regressor

    # def updateQ(state, move):
    #     Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
    #     currentVal = self.Q.get((str(state), move), 0)
    #     self.Q[(str(state), move)] = currentVal + self.learningRate * (val - currentVal)

    # Look further ahead


# train Qlearn on predicting total score (some scores are based on other players)
    def action(self, board, state, turn, playerNum, possibleMoves):
# Possible moves is hand


    def action(self):
        data = np.concatenate([toArray(self.hand), toArray(self.board)])
        vals = [self.runQ(data, card) fpr card in hand]
        sortedVals = np.argsort(vals)
        bestValIndex = sortedVals[-1] #use amax
        return possibleMoves[bestValIndex]

        strState = str(state)
        vals = [self.Q.get((strState, move), 0) for move in possibleMoves]
        sortedVals = np.argsort(vals)
        bestValIndex = sortedVals[-1] #use amax
        return possibleMoves[bestValIndex]

# Start by maximizing your own points given current hand and played cards.
# Use information of past hands and opponents played cards? (Hard)





# old
    # def boolState(self, State, player): # 2D
    #     state = copy.deepcopy(State)
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if state[i,j] == player:
    #                 state[i,j] = 1
    #             elif state[i,j] != 0:
    #                 state[i,j] = -1
    #     return state

    # def nextState(self, state, move, change=1):
    #     newState = copy.deepcopy(state)
    #     newState[move] = change
    #     return newState

    # def bestQ(self, state, possibleMoves, returnVal=False):
    #     strState = str(state)
    #     vals = [self.Q.get((strState, move), 0) for move in possibleMoves]
    #     sortedVals = np.argsort(vals)
    #     bestValIndex = sortedVals[-1] #use amax
    #     return possibleMoves[bestValIndex]

    # # def trainAction(self, state, possibleMoves, numEmpty):
    # #     move = possibleMoves.pop(random.randrange(numEmpty)) # make not always random? # possibly implement a random choice with weighted distribution?
    # #     if len(possibleMoves) <= 1:
    # #         return move
    # #     newState = np.negative(self.nextState(state, move))
    # #     newMoves = copy.deepcopy(possibleMoves)
    # #     newMoves.remove(move)

    # def train(self, state, oldState, move, possibleMoves):
    #     strState, strOldState = str(state), str(oldState)
    #     val = np.amax([self.Q.get((strState, possibleMove), 0) for possibleMove in possibleMoves])
    #     val = np.multiply(val, np.negative(self.discountRate))
    #     currentVal = self.Q.get((strOldState, move), 0)
    #     self.Q[(strOldState, move)] = np.add(currentVal, np.multiply(self.learningRate, np.subtract(val, currentVal)))
    #     # For symmetrical games the state should be identical to a different playerNum (with a respective state) as to reduce redundancy that could make training harder
    #     # Limited information, use neural net
    # def action(self, board, state, turn, playerNum, possibleMoves):
    #     state = self.boolState(state, playerNum)
    #     return self.bestQ(state, possibleMoves) 


    # # def end(self, reward, winner, playerNum, state, move):
    # #     state = self.boolState(state, playerNum)
    # #     oldState = np.negative(self.nextState(state, move, change=0))
    # #     self.R[(str(oldState), move)] = reward
    # #     self.updateQVal(oldState, move, reward)
    #     # if self.debugMode: print self.Q.values()

    # def won(self, state, move, winner):
    #     self.Q[(str(state), move)] = winner
