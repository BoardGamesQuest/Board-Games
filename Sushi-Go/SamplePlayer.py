from AbstractPlayer import Abstract
import shelve

class Sample(Abstract):
    def __init__(self, playerNum, numPlayers):
        super(Sample, self).__init__(playerNum, numPlayers)
        self.pastScore = 0

    def move(self, game):
        card = self.hand[0]
        return card # returns card if the game needs it
