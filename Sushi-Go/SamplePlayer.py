import AbstractPlayer

class SamplePlayer(AbstractPlayer):
    def __init__(self, playerNum, numPlayers):
        super(self, playerNum, numPlayers).__init__()

    def move(self):
        card = self.hand[0]
        del.self.hand[0] # removes the card from the hand
        self.board.append(card) #adds the card to the board
        return card # returns card if the game needs it 
