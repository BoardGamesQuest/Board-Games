import random
class Player:
    def __init__(self, playerNum, numPlayers):
        self.playerNum = playerNum
        self.hand = []
        self.board = []
        self.score = 0
    def scoreBoard():
        for i in self.board:
            if self.board[i].cardType == 'Nigiri':
                self.score += self.board[i].pointvalue

    def generateHand(self):
        while (len(self.hand) < 8):#formula for cards in hand given numPlayers)
            self.hand.append(random.choice([Card('nigiri'),Card('Sashimi'),Card('Dumpling'),Card('Wasabi'),Card('Maki'),Card('Tempura'),Card('Pudding')]))#may want to change if we want to incorporate the number of times a card appears in the deck
        for i in range(len(self.hand)):
            print self.hand[i].cardType

    def selectCards():
        # temporary
        move = Card("Squid Nigiri")
        # should make something that iterates through hand, and if card is not found ask for a different card

        
class Card:
    def __init__(self, cardType):
        self.cardType = cardType
# me = Player(1,1)
# me.generateHand()
