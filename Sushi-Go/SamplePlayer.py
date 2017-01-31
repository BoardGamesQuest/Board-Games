import AbstractPlayer

class SamplePlayer(AbstractPlayer):
    def __init__(self, playerNum, numPlayers):
        super(SamplePlayer, self).__init__(playerNum, numPlayers)

    def move(self):
        card = self.hand.pop(0)
        self.board.append(card) #adds the card to the board
        return card # returns card if the game needs it 
