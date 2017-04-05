from AbstractPlayer import Abstract
import copy

class CardEvaluator(Abstract):
    def __init__(self, playerNum, numPlayers, game):
        super(CardEvaluator, self).__init__(playerNum, numPlayers, game)
        self.pastScore = 0
        for i in range(numPlayers):
            self.prevHands[i] = self.game.normalDistribution()
        self.handTracker = 0

    # def takeHand(self, hand):
    #     super(CardEvaluatior, self).takeHand(self, hand)
    #     # self.prevHands[self.handTracker] = hand

    def move(self):
        self.prevHands[self.handTracker] = copy.deepcopy(self.hand)
        temp = (self.hand[0], 0)
        for cards in self.hand:
            if self.ScoreCard(game, cards) > temp[1]:
                temp = (cards, self.ScoreCard(game, cards))

        self.hand.remove(temp[0])
        self.board.append(temp[0])
        self.prevHands[self.handTracker] = copy.deepcopy(self.hand)
        self.handTracker = (self.handTracker + 1) % self.numPlayers
        return temp[0]

    def ScoreCard(self, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        if self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)>0:
            return self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)
        elif (card.cardType == "Tempura"):
            tempPrevHands = copy.deepcopy(self.prevHands)
            tempPrevHands[self.handTracker].remove(card)
            totalScore = 0
            for hand in self.prevHands:
                tempuraTracker = 0
                for card in hand:
                    if (card.cardType == "Tempura"):
                        tempuraTracker++
                score = 2.5*tempuraTracker/(2*self.numPlayers-tempuraTracker)
                if (score > 2.5):
                    score = 2.5
                totalScore = (totalScore+score)/(1+totalScore*score/2.5^2)
            return totalScore
