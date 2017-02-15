from AbstractPlayer import Abstract

class Sample2(Abstract):
    def __init__(self, playerNum, numPlayers):
        super(Sample2, self).__init__(playerNum, numPlayers)

    def move(self):
        card = self.hand.pop(0)
        print('move')
        if card.cardType == 'Nigiri 1' or card.cardType == 'Nigiri 2' or card.cardType == 'Nigiri 3':
            for card2 in self.board:
                if card2.cardType == 'Wasabi':
                    if not card2.nigiri:
                        card2.addNigiri(card)
                        break
        self.board.append(card) #adds the card to the board
        return card # returns card if the game needs it
