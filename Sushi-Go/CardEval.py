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
            if self.ScoreCard(game, cards) > temp[1]:
                temp = (cards, self.ScoreCard(game, cards))

        self.hand.remove(temp[0])
        self.board.append(temp[0])
        return temp[0]

    def ScoreCard(self, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        if self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)>0:
            return self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)
        # elif (card.type == "Tempura"):
            
