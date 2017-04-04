from AbstractPlayer import Abstract
import copy

class CardEval(Abstract):
    def __init__(self, playerNum, numPlayers):
        super(CardEval, self).__init__(playerNum, numPlayers)
        self.pastScore = 0
        for i in range(numPlayer):

    def move(self, game):
        temp = (self.hand[0], 0)
        for cards in self.hand:
            if ScoreCard(game, cards) > temp[1]:
                temp = (cards, ScoreCard(game, cards))
        return temp[0]

    def ScoreCard(self, game, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        return game.scoreSingle(self.board+[card])-game.scoreSingle(self.board)
