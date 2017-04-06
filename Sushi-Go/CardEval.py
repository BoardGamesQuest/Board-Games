from AbstractPlayer import Abstract
import copy

def replicate(inp): #copy doesn't really work for maintaining the same instance of objects, but this will (JANK)
    if type(inp) != list:
        new = [inp] + [0]
        new.pop()
        new = new[0]
    else:
        new = inp + [0]
        new.pop()
    return new

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
        # print self.hand
        # print len(self.hand)
        self.prevHands[self.handTracker] = replicate(self.hand)
        temp = (self.hand[0], 0)
        for cards in self.prevHands[self.handTracker]:
            if self.ScoreCard(cards) > temp[1]:
                temp = (cards, self.ScoreCard(cards))

        for i in self.prevHands[self.handTracker]:
            if (i.cardType == temp[0].cardType):
                self.prevHands[self.handTracker].remove(i)
                break
        self.handTracker = (self.handTracker + 1) % self.numPlayers
#        print self.hand
#        print len(self.hand)
#        return temp[0]
        for i in self.hand:
            if (i.cardType == temp[0].cardType):
                return i

    def ScoreCard(self, card):
        # tempGame = copy.deepcopy(game)
        # tempBoard = copy.deepcopy(self.board)
        # tempBoard2 = copy.deepcopy(self.board).append(card)
        if (card.cardType == "Dumpling"):
            return self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)+0.01
        elif self.game.scoreSingle(self.board+[card])-self.game.scoreSingle(self.board)>0:
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
                    counter += 1
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
        elif (card.cardType == "Pudding"):
            tempPrevHands = copy.deepcopy(self.prevHands)
            puddingCounter = -1
            for hand in tempPrevHands:
                for tempCard in hand:
                    if (tempCard.cardType == "Pudding"):
                        puddingCounter += 1
            puddVals = []
            for i in range(len(self.game.players)):
                pudd = 0
                for c in self.game.players[i].board:
                    if (c.cardType == "Pudding"):
                        pudd += 1
                puddVals.append(pudd)
            withoutSelf = copy.deepcopy(puddVals)
            withoutSelf.pop(self.playerNum)
            if ( puddVals[self.playerNum] > max(withoutSelf) ):
                return 0
            elif ( puddVals[self.playerNum] <= max(withoutSelf) and puddVals[self.playerNum] >= min(withoutSelf)):
                return ((4+puddingCounter)/(puddingCounter+1))/(max(withoutSelf)-puddVals[self.playerNum]+1)
            elif (puddVals[self.playerNum] < min(withoutSelf)):
                return ((4+puddingCounter)/(puddingCounter+1))/(min(withoutSelf)-puddVals[self.playerNum]+1)



        elif (card.cardType[:4] == "Maki"):
            tempPrevHands = copy.deepcopy(self.prevHands)
            puddingCounter = -1*int(card.cardType[-1])
            for hand in tempPrevHands:
                for tempCard in hand:
                    if (tempCard.cardType[:4] == "Maki"):
                        puddingCounter += int(tempCard.cardType[-1])
            puddVals = []
            for i in range(len(self.game.players)):
                pudd = 0
                for c in self.game.players[i].board:
                    if (c.cardType[:4] == "Maki"):
                        pudd += int(c.cardType[-1])
                puddVals.append(pudd)
            withoutSelf = copy.deepcopy(puddVals)
            withoutSelf.pop(self.playerNum)
            if ( puddVals[self.playerNum] > max(withoutSelf) ):
                return 0
            else:
                thing = 2+max(withoutSelf)-puddVals[self.playerNum]-int(card.cardType[-1])
                if (thing == 0):
                    thing = .9
                if (thing == -1):
                    thing = .8
                return ((6+puddingCounter)/(puddingCounter+1))/thing
