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
        if not(pastMatchData['TotalRounds'] > 0): # this is there so that if the int with the key 'Games' was not created yet in the shelve, it then creates it, instead of trying to add to it which does not work with undefined ints. only needs to be run once ever.
            pastMatchData['TotalRounds'] = 1
        else:
            pastMatchData['TotalRounds'] += 1

    def cleanup(self):
        roundName = 'Round ' + str(self.round) + ' ' + str(pastMatchData['TotalRounds'])
        pastMatchData[roundName] = {}
        pastMatchData[roundName]['Round'] = self.round
        pastMatchData[roundName]['TotalRound'] = pastMatchData['TotalRounds']
        pastMatchData[roundName]['Board'] = self.board
        pastMatchData[roundName]['Percentages'] = {}
        cardsByType = {}
        total = 0
        for card in self.board:
            if not(cardsByType.has_key(card.type)):
                cardsByType[card.type] = 0
            cardsByType[card.type] += 0
            total += 1
        for key in cardsByType.key():
            pastMatchData[roundName]['Percentages'][key] = cardsByType[key]/total
        print(roundName + " " + str(pastMatchData[roundName]))
        self.pastMatchData.close()


