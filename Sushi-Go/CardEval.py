from AbstractPlayer import Abstract
import copy

class CardEvaluator(Abstract):
    def __init__(self, playerNum, numPlayers, game):
        super(CardEvaluator, self).__init__(playerNum, numPlayers, game)
        self.pastScore = 0
        for i in range(numPlayers):
            self.prevHands[i] = self.game.normalDist()

    def move(self):
        temp = (self.hand[0], 0)
        for cards in self.hand:
            if ScoreCard(self.game, cards) > temp[1]:
                temp = (cards, ScoreCard(self.game, cards))
        return temp[0]

    def ScoreCard(self, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        if self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)>0:
            return self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)
        elif (card.type = "Tempura"):
            
