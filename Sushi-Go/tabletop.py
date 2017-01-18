import copy


class Sushi:
    def __init__(self, params, debugMode=False):
        if type(params) == list:
            self.numPlayers = params[0]
        self.debugMode = debugMode
        self.players = []
        for i in range(numPlayers):
            players.append(Player(i, numPlayers))

    # def reset():
    #     for player in players:
    #         player.hand = player.generateHand
    #         # someone write generateHand plz
    #         player.board = []

    def display():
        for player in self.players:
            print "This is player {}'s hand:".format(player.playerNum), player.hand
            print "This is player {}'s board:".format(player.playerNum), player.board

    def selectCards():
        # temporary
        move = Card("Squid Nigiri")

    def processMoves(player, move):
        player.hand.remove(move)
        player.board.append(move)

    def passHands():
        # this might be pretty inefficient, optimize plz
        tempPlayers = copy.deepcopy(self.players)
        for player in self.players:
            player.hand = tempPlayers[(player.playerNum+1)%numPlayers]



    def runGame():




# not sure if a card class helps
class Card:
    def __init__(self, cardType):


class Player:
    def __init__(self, playerNum, numPlayers):
        self.playerNum = playerNum
        self.hand = self.generateHand(numPlayers)
        self.board = []

    def generateHand():
