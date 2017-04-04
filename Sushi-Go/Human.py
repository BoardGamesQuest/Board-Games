from AbstractPlayer import Abstract

class Interactive(Abstract):

    def __init__(self, playerNum, numPlayers):
        super(Interactive, self).__init__(playerNum, numPlayers)

    def move(self):
        print("This is your Hand:")
        for i in range(len(self.hand)):
            print (str(i) + ": " + self.hand[i].cardType)
        print("This is your Board:")
        for i in range(len(self.board)):
            print (str(i) + ": " + self.board[i].cardType)
        while True:
            inp = raw_input("Please Choose a card by submitting it's index ")
            try:
                cardIndex = int(inp)
            except:
                print("You did not enter a valid index")
                continue
            if cardIndex in range(len(self.hand)):
                print("You Chose " + self.hand[cardIndex].cardType)
                answer = str(raw_input("Please confirm your choice by entering y if you would like to choose again enter n "))
                if answer == "y":
                    print("Your choice has been confirmed")
                    break
            else:
                print("You did not enter a valid index")

        card = self.hand.pop(cardIndex)
        print(card.cardType)
        self.board.append(card)
        return card
        
