from AbstractPlayer import Abstract
import copy

class CardEvaluator(Abstract):
    def __init__(self, playerNum, numPlayers, game):
        super(CardEvaluator, self).__init__(playerNum, numPlayers)
        self.pastScore = 0
        self.game = game
        self.prevHands = []
        for i in range(numPlayers):
            self.prevHands.append(self.game.normalDistribution())
        self.handTracker = 0

    # def takeHand(self, hand):
    #     super(CardEvaluatior, self).takeHand(self, hand)
    #     # self.prevHands[self.handTracker] = hand

    def move(self, game):
        print self.hand
        print len(self.hand)
        self.prevHands[self.handTracker] = copy.deepcopy(self.hand)
        temp = (self.hand[0], 0)
        for cards in self.prevHands[self.handTracker]:
            if self.ScoreCard(cards) > temp[1]:
                temp = (cards, self.ScoreCard(cards))

        for i in self.hand:
            if (i.cardType == temp[0].cardType):
                self.hand.remove(i)
                self.board.append(temp[0])
                break
        self.prevHands[self.handTracker] = copy.deepcopy(self.hand)
        self.handTracker = (self.handTracker + 1) % self.numPlayers
        print self.hand
        print len(self.hand)
        return temp[0]

    def ScoreCard(self, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        if self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)>0:
            return self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)
        elif (card.cardType == "Tempura"):
            tempPrevHands = copy.deepcopy(self.prevHands)
            # print tempPrevHands[self.handTracker]
            # print card
            for i in range(len(tempPrevHands[self.handTracker])):
                if (tempPrevHands[self.handTracker][i].cardType == "Tempura"):
                    tempPrevHands[self.handTracker].pop(i)
                    break
            # tempPrevHands[self.handTracker].remove(card)
            totalScore = 0
            for hand in tempPrevHands:
                tempuraTracker = 0
                for card in hand:
                    if (card.cardType == "Tempura"):
                        tempuraTracker += 1
                score = 2.5*tempuraTracker/(2*self.numPlayers-tempuraTracker)
                if (score > 2.5):
                    score = 2.5
                totalScore = (totalScore+score)/(1+totalScore*score/2.5**2)
            return totalScore
        elif (card.cardType == "Sashimi"):
            counter = 0
            for card in self.board:
                if (card.cardType == "Sashimi"):
                    counter++
            if (counter%3 == 0):
                tempPrevHands = copy.deepcopy(self.prevHands)
                # print tempPrevHands[self.handTracker]
                # print card
                for i in range(len(tempPrevHands[self.handTracker])):
                    if (tempPrevHands[self.handTracker][i].cardType == "Sashimi"):
                        tempPrevHands[self.handTracker].pop(i)
                        break
                # tempPrevHands[self.handTracker].remove(card)
                totalScore = 0
                for hand in tempPrevHands:
                    sashimiTracker = 0
                    for card in hand:
                        if (card.cardType == "Sashimi"):
                            sashimiTracker += 1
                    score = (3+1/3)*sashimiTracker/(2*(3*self.numPlayers-sashimiTracker))
                    if (score > (3+1/3)):
                        score = (3+1/3)
                    totalScore = (totalScore+score)/(1+totalScore*score/(3+1/3)**2)
                return totalScore
            elif (counter%3 == 1):
                tempPrevHands = copy.deepcopy(self.prevHands)
                # print tempPrevHands[self.handTracker]
                # print card
                for i in range(len(tempPrevHands[self.handTracker])):
                    if (tempPrevHands[self.handTracker][i].cardType == "Sashimi"):
                        tempPrevHands[self.handTracker].pop(i)
                        break
                # tempPrevHands[self.handTracker].remove(card)
                totalScore = 0
                for hand in tempPrevHands:
                    sashimiTracker = 0
                    for card in hand:
                        if (card.cardType == "Sashimi"):
                            sashimiTracker += 1
                    score = (5)*sashimiTracker/(2*self.numPlayers-sashimiTracker)
                    if (score > 5):
                        score = 5
                    totalScore = (totalScore+score)/(1+totalScore*score/5**2)
                return totalScore
