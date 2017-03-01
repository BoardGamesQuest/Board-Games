from AbstractPlayer import Abstract
import shelve

class Learner(Abstract):

    def __init__(self, playerNum, numPlayers):
        super(Sample, self).__init__(playerNum, numPlayers)
        self.currentRound = self.round
        
    def move():
        self.pastMatchData = shelve.open('PastMatchData') #this algorithm will try to match the Ideal composition of cards based on passed match data.
        # it will take the percantage of each type of card of every game and scale it by the end score, and then take the average? and make that a set point it is trying to reach throught the game
        # it should do this individually or each round and then scale the percentatege of the board at the round end by the total score bc of pudding and stuff.
        # step 1: storring data from previous rounds
            # SubStep 1: dettecting a new round
        weights = weigh(self.hand)
        best = (0, 0)
        for item in weights.items():
            if item[1] > best[1]:
                best = item
        card = self.hand.pop(best[0])
        self.board.append(card)
        self.pastMatchData.close()
        return card

    def weigh(hand): # this should be a function that gives different wieghts to each card and then returns a dictionary with the keys as the card index and the weights as the value
        weights = {}
        for i in range(len(self.hand)):
            weights[i] = 
        return 


