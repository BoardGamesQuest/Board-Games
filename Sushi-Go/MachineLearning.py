from AbstractPlayer import Abstract
import shelve

class Learner(Abstract):

    def __init__(self, playerNum, numPlayers):
        super(Learner, self).__init__(playerNum, numPlayers)
        self.currentRound = self.round
        
    def move(self):
        self.pastMatchData = shelve.open('PastMatchData') #this algorithm will try to match the Ideal composition of cards based on passed match data.
        # it will take the percantage of each type of card of every game and scale it by the end score, and then take the average? and make that a set point it is trying to reach throught the game
        # it should do this individually or each round and then scale the percentatege of the board at the round end by the total score bc of pudding and stuff.
        # step 1: storring data from previous rounds
            # SubStep 1: dettecting a new round
        card = self.hand.pop(0)
        self.board.append(card)
        self.pastMatchData.close()
        return card

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
        localPastMatchData['Score'] = self.score
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
        print(roundName + " " + str(self.pastMatchData[roundName]))

            
        self.pastMatchData.close()

    def calculateTarget(self, rnd):
        self.pastMatchData = shelve.open('PastMatchData')
        target = {}
        totalScore = 0.0
        totalRounds = 0.0
        Scores = []
        for key in self.pastMatchData.keys():
            if key == 'TotalRounds':
                pass
            elif self.pastMatchData[key]["Round"] == rnd:
                totalScore += self.pastMatchData[key]["Score"]
                Scores.append(self.pastMatchData[key]["Score"])
                totalRounds += 1
        averageScore = totalScore/totalRounds
        topScores = []
        topScoresTotal = 0.0
        for key in self.pastMatchData.keys():
            if key == 'TotalRounds':
                pass
            elif self.pastMatchData[key]["Round"] == rnd:
                if self.pastMatchData[key]["Score"] >= averageScore:
                    topScoresTotal += self.pastMatchData[key]["Score"]
                    topScores.append(self.pastMatchData[key]["Score"])
        for key in self.pastMatchData.keys():
            if key == 'TotalRounds':
                pass
            elif self.pastMatchData[key]["Round"]  == rnd:
                if self.pastMatchData[key]["Score"] >= averageScore:
                    for cardPercentageKey in self.pastMatchData[key]['Percentages']:
                        if not(target.has_key(cardPercentageKey)):
                            target[cardPercentageKey] = self.pastMatchData[key]['Percentages'][cardPercentageKey]*(self.pastMatchData[key]["Score"]/topScoresTotal)
                        else:
                            target[cardPercentageKey] += self.pastMatchData[key]['Percentages'][cardPercentageKey]*(self.pastMatchData[key]["Score"]/topScoresTotal)
        self.pastMatchData.close()
        return target # It Works!!! (Very inifeciently though. To many for loops)




                # need to find a way to scale the percentages such that afterwards, the avarage or so still adds up to 100
                
                

    def reset(self):
        self.pastMatchData = shelve.open('PastMatchData')
        for key in self.pastMatchData.keys():
            del self.pastMatchData[key]
        self.pastMatchData.close()

