from AbstractPlayer import Abstract

class Sample(Abstract):
    def __init__(self, playerNum, numPlayers):
        super(Sample, self).__init__(playerNum, numPlayers)

    def move(self):
        card = self.hand.pop(0)
        self.board.append(card) #adds the card to the board
        return card # returns card if the game needs it
