import copy
import random


class SushiGo:
    def __init__(self, params, debugMode=False):
        if type(params) == list:
            self.numPlayers = params[0]
        if type(params) == list && len(self.params) > 1
            self.maxRounds = params[1] #default should be 3
        self.debugMode = debugMode
        self.players = []
        self.numRound = 0
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



    def processMoves(player, move):
        player.hand.remove(move)
        player.board.append(move)

    def passHands():
        # this might be pretty inefficient, optimize plz
        tempPlayers = copy.deepcopy(self.players)
        for player in self.players:
            player.hand = tempPlayers[(player.playerNum+1)%numPlayers]




    def runGame():
        for player in self.players:
            player.generateHand()
        self.display()
#        while True: #hopefully theres a better way to repeatedly check
        for player in self.players:
            self.processMoves(player, player.selectCards())
        if len(self.players[len(self.players)-1].hand) == 0:
            for player in self.players:
                player.scoreBoard()
                self.numRound += 1
                player.generateHand()
        else:
            self.passHands()
