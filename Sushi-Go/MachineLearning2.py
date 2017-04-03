from AbstractPlayer import Abstract
import shelve

class Learner2(Abstract):

    def __init__(self, playerNum, numPlayers, collectingData = False):
        super(Learner2, self).__init__(playerNum, numPlayers)
        self.currentRound = self.round
        self.pastScore = 0
        self.collectingData = collectingData
        
    def move(self):
        if self.collectingData:
            cardFinal = self.hand.pop(0)
            self.board.append(cardFinal)
            return cardFinal
        #print(self.hand)
        self.pastMatchData = shelve.open('PastMatchData') #this algorithm will try to match the Ideal composition of cards based on passed match data.
        # it will take the percantage of each type of card of every game and scale it by the end score, and then take the average? and make that a set point it is trying to reach throught the game
        # it should do this individually or each round and then scale the percentatege of the board at the round end by the total score bc of pudding and stuff.
        target = self.calculateTarget(self.round)
        cardsByType = {}
        total = 0.0
        for card in self.board:
            if not(cardsByType.has_key(card.cardType)):
                cardsByType[card.cardType] = 0.0
            cardsByType[card.cardType] += 1
            total += 1
        boardPercentage = {}
        for key in cardsByType.keys():
            boardPercentage[key] = round((cardsByType[key] * 100)/total, 2)
        diff = {}
        for key in target.keys():
            if boardPercentage.has_key(key):
                diff[key] = round(target[key] - boardPercentage[key], 2)
            else:
                diff[key] = round(target[key], 2) # this rounding behaves weirdly as well as in other places
        priorityList = []
        for key in diff.keys(): # needs debugging
            if len(priorityList) > 0:
                if diff[key] < diff[priorityList[-1]]:
                    priorityList.append(key)
                    #print("not in list, appending " + key)
                else:
                    for i in range(len(priorityList)):
                        if diff[key] > diff[priorityList[i]]:
                            priorityList.insert(i, key)
                            #print(key + " is bigger than " + priorityList[i + 1] + ", inserting at " + str(i))
                            break
                        else:
                            pass
            else:
                priorityList.append(key)
                #print("no list, appending " + key)
        cardFinal = 0
        tempList = priorityList
        for priority in priorityList:
            for card in self.hand:
                if card.cardType == priority:
                    cardFinal = card
            if not(cardFinal == 0):
                #print("hand: " + str(self.hand))
                #print("removing card: " + str(cardFinal))
                self.hand.remove(cardFinal)
                break
        if cardFinal == 0:
            cardFinal = self.hand[0]
            self.hand.remove(cardFinal)
            
            
        #print(target)
        #print(boardPercentage)
        #print(diff)
        #print(priorityList)
        if cardFinal.cardType[:-2] == 'Nigiri':
            #print("Nigiri")
            for card in self.board:
                if card.cardType == 'Wasabi':
                    #print('wasabi')
                    if not card.nigiri:
                        #print('empty')
                        card.addNigiri(cardFinal)
                        break
        self.board.append(cardFinal)
        self.pastMatchData.close()
        return cardFinal

    def setup(self):
        self.pastMatchData = shelve.open('PastMatchData')
        if not(self.pastMatchData.has_key('TotalRounds')): # this is there so that if the int with the key 'Games' was not created yet in the shelve, it then creates it, instead of trying to add to it which does not work with undefined ints. only needs to be run once ever.
            self.pastMatchData['TotalRounds'] = 1
        else:
            self.pastMatchData['TotalRounds'] += 1
        self.pastMatchData.close()

    def cleanup(self):
        self.pastMatchData = shelve.open('PastMatchData')
        roundName = 'Round ' + str(self.round) + ' ' + str(self.pastMatchData['TotalRounds'])
        localPastMatchData = {}
        localPastMatchData['Score'] = self.score - self.pastScore
        self.pastScore = self.score
        localPastMatchData['Round'] = self.round
        localPastMatchData['TotalRound'] = self.pastMatchData['TotalRounds']
        localPastMatchData['Board'] = self.board
        #print(localPastMatchData)
        cardsByType = {}
        total = 0.0
        for card in self.board:
            if not(cardsByType.has_key(card.cardType)):
                cardsByType[card.cardType] = 0.0
            cardsByType[card.cardType] += 1
            total += 1
        tempDict = {}
        for key in cardsByType.keys():
            tempDict[key] = round((cardsByType[key] * 100)/total, 2)
            #print(cardsByType[key])
            #print(total)
            #print(tempDict)
        localPastMatchData['Percentages'] = tempDict
        localPastMatchData['lengthOfBoard'] = total
        self.pastMatchData[roundName] = localPastMatchData
        #print(roundName + " " + str(self.pastMatchData[roundName]))

            
        self.pastMatchData.close()

    def calculateTarget(self, rnd):
        self.pastMatchData = shelve.open('PastMatchData')
        target = {}
        top10 = []
        topScoresTotal = 0.0
        for i in range(9):
            best = 0
            for key in self.pastMatchData.keys():
                if key == 'TotalRounds':
                    pass
                elif best == 0:
                    best = key
                elif self.pastMatchData[key]["Round"]  == rnd:
                    if (self.pastMatchData[key]["Score"] > self.pastMatchData[best]["Score"]) and not(key in top10):
                        best = key
            top10.append(best)
        print (top10)
        for key in top10:
            topScoresTotal += self.pastMatchData[key]["Score"]
        for key in top10:
            for cardPercentageKey in self.pastMatchData[key]['Percentages']:
                if not(target.has_key(cardPercentageKey)):
                    target[cardPercentageKey] = round(self.pastMatchData[key]['Percentages'][cardPercentageKey]*(self.pastMatchData[key]["Score"]/topScoresTotal), 2)
                else:
                    target[cardPercentageKey] += round(self.pastMatchData[key]['Percentages'][cardPercentageKey]*(self.pastMatchData[key]["Score"]/topScoresTotal), 2)
        self.pastMatchData.close()
        #print(target)
        return target # It Works!!! (Very inifeciently though. To many for loops)




                # need to find a way to scale the percentages such that afterwards, the avarage or so still adds up to 100
                
                

    def reset(self):
        self.pastMatchData = shelve.open('PastMatchData')
        for key in self.pastMatchData.keys():
            del self.pastMatchData[key]
        self.pastMatchData.close()

