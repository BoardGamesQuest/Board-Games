from AbstractPlayer import Abstract

class Human(Abstract):
    def __init__(self, playerNum, numPlayers):
        super(Human, self).__init__(playerNum, numPlayers)

    def move(self):
        print "my current board = "
        for i in self.board:
            print i.cardType
        print "my hand ="
        for i in self.hand:
            print i.cardType
        print "Please select your card."
        self.cardchoice = 0
        UserInput = raw_input()
        i = 0
        while i < len(self.hand):
            if self.hand[i].cardType == str(UserInput):
                self.cardchoice = i
                i+= 1
            else:
                i+= 1
#                for i in range(len(self.hand)):
#                                if self.hand[i] == str(UserInput):
#                                                    self.cardchoice = i
        card = self.hand.pop(self.cardchoice)
        self.board.append(card) #adds the card to the board
        return card # returns card if the game needs it
