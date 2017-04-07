import numpy as np

def scoreNigiri(boards):
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType[0:6] == 'Nigiri' :
                boardScores[-1] += card.pointValue
                #print card.pointValue

    #print("Nigiri: " + str(boardScores))

    return boardScores

def scoreSashimi(boards):
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType == 'Sashimi':
                boardScores[-1] += 1
        boardScores[-1] =  np.floor(boardScores[-1]/3) * 10

    #print("Sashimi: " + str(boardScores))

    return boardScores

def scoreDumpling(boards):
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType == 'Dumpling':
                boardScores[-1] += 1
        score = 0
        print boardScores[-1]
        if (boardScores[-1] < 5):
            for i in range(boardScores[-1]+1): # there might be something more efficient
                score += i
                print ("I: " + str(i) + " score: " + str(score))
            boardScores[-1] = score
        else:
            boardScores[-1] = 15

    #print("Dumpling: " + str(boardScores))

    return boardScores

def scoreWasabi(boards):
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType == 'Wasabi':
                if card.nigiri:
                    boardScores[-1] += (2*card.nigiriCard.pointValue) # only * 2 becuase we already evaluate the point value once when scoring nigiri

    #print("Wasabi: " + str(boardScores))

    return boardScores

def scoreTempura(boards):
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType == 'Tempura':
                boardScores[-1] += 1
        boardScores[-1] =  np.floor(boardScores[-1]/2) * 5
    #print("Tempura: " + str(boardScores))
# use IsInstance function
    return boardScores

def scoreMaki(boards): # is there anything more eficient?
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType[0:4] == 'Maki':
                boardScores[-1] += card.size
    sortScores = sorted(boardScores)
    firsts = []
    seconds = []
    for i in range(len(boardScores)):
        if boardScores[i] == sortScores[-1]:
            firsts.append(i)
        elif boardScores[i] == sortScores[- (1+sortScores.count(sortScores[-1]))]:
            seconds.append(i)
    for i in range(len(boardScores)):
        if i in firsts:
            boardScores[i] = np.floor(6/(len(firsts)))
        elif i in seconds:
            boardScores[i] = np.floor(3/(len(seconds)))
        else:
            boardScores[i] = 0

    #print("Maki: " + str(boardScores))

    return boardScores

def scorePudding(boards):
    boardScores = []
    for board in boards:
        boardScores.append(0)
        for card in board:
            if card.cardType == 'Pudding':
                boardScores[-1] += 1
    sortScores = sorted(boardScores)
    firsts = []
    lasts = []
    for i in range(len(boardScores)):
        if boardScores[i] == sortScores[-1]:
            firsts.append(i)
        elif boardScores[i] == sortScores[1]:
            lasts.append(i)
    for i in range(len(boardScores)):
        if i in firsts:
            boardScores[i] = np.floor(6/(len(firsts)))
        elif i in lasts:
            boardScores[i] = np.floor(-6/(len(lasts)))
        else:
            boardScores[i] = 0

    #print("Pudding: " + str(boardScores))

    return boardScores
