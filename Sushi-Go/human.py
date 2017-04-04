from AbstractPlayer import Abstract

class Human(Abstract):
    def __init__(self, playerNum, numPlayers, SushiGo):
        super(Human, self).__init__(playerNum, numPlayers, SushiGo)

    def move(self):
        print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nNEW TURN"
        for i in self.SushiGo.players:
            if i.playerNum == self.playerNum:
                print "Player {} (you) has:".format(i.playerNum)
            else:
                print "Player {} has:".format(i.playerNum)
                for j in i.board:
                    print j.cardType+", ",
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
