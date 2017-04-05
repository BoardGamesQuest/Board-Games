from AbstractPlayer import Abstract
import copy

class CardEvaluator(Abstract):
    def __init__(self, playerNum, numPlayers):
        super(CardEvaluator, self).__init__(playerNum, numPlayers)
        self.pastScore = 0
        

    def move(self, game):
        temp = (self.hand[0], 0)
        for cards in self.hand:
            if self.ScoreCard(game, cards) > temp[1]:
                temp = (cards, self.ScoreCard(game, cards))

        self.hand.remove(temp[0])
        self.board.append(temp[0])
        return temp[0]

    def ScoreCard(self, game, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        return game.scoreSingle(self.board+[card])-game.scoreSingle(self.board)
