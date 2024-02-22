#!/usr/bin/env python3
import colors as c
import random
import time

def createcards():
    suits = ['diamonds','clubs','hearts','spades']
    values = [['ace',11],['jack',10],['queen',10],['king',10],['2',2],['3',3],['4',4],['5',5],['6',6],['7',7],['8',8],['9',9],['10',10]]
    standardDeck=[]
    for cardList in values:
        for suit in suits:
            word = cardList[0] + " of " + suit
            value = cardList[1]
            minilist = [word, value]
            standardDeck.append(minilist)
    return standardDeck

def printrules():
    print('''
objective:Get as close to 21 points without going over.
How to win:Be the closest to 21 points. If you go over, you lose.
Point values:All cards are worth the value on the card, and face cards are worth 10.
Aces:Aces can be used as 1 or 11 points.
''')
    input('press enter to continue\n')

def knowsHowToPlay():
    answered = False
    while answered == False:
        answer = input(c.cl + "Does everyone know how to play blackjack? (Y/n) > ").lower().strip()
        if 'y' in answer:
            answered = True
        elif 'n' in answer:
            answered = True
            printrules()
        else:
            print('Invalid. Please say yes or no.')

def isAce(card):
    if 'ace' in card:
        return True
    return False

def hasAce(aces):
    hasAce = False
    for ace in aces:
        if ace == 11: 
            aces.remove(11)
            aces.append(1)
            hasAce = True
            break

    return hasAce, aces


def getTwoCards(deck):
    card =deck.pop()
    card2 = deck.pop()
    if isAce(card[0]) and isAce(card2[0]):
        total = 12
    else:
        total = card[1] + card2[1]
    titleOne = card[0]
    titleTwo = card2[0]
    return titleOne, titleTwo, total, deck

def getPlayers():
    try:
        while True:
            players = input('How many players? > ')
            if players.isdigit():
                return int(players)
            else:
                print('Please type a number.')
    except KeyboardInterrupt:
        print(c.cl)
        exit()
def printHand(titleOne, titleTwo, total):
    print("Your hand contains the " + titleOne + " and the " + titleTwo + " for a total of",total,"points.")
def getOneMoreCard(deck,total):
    card = deck.pop()
    title = card[0]

    total += card[1]
    print("Your new card is the "+title+". You now have",total,'Points')
    return total, deck, title
def askToHit(hand, firstTime):
    try:
        while True:
            itemstring = "Your hand contains:"
            for item in hand:
                itemstring += item + " "
            if firstTime == False:
                print(itemstring)
            wantToHit = input('would you like to hit? > ')
            if 'y' in wantToHit:
                return True
                break
            elif 'n' in wantToHit:
                return False
                break
            else:
                print('Please type yes or no.')
    except KeyboardInterrupt:
        print(c.cl)
        exit()
def getroundvalues(players):
    firstTime = []
    hands = []
    totals = []
    aces = []
    for x in range(players):
        firstTime.append(True)
        totals.append(0)
        hands.append([])
        aces.append([])
    return firstTime, hands, totals, aces
def getpermvalues(players):
    playerNames = []
    losses = []
    wins = []
    ties = []
    for x in range(players):
        playerNames.append("Player "+str(x + 1))
        wins.append(0)
        ties.append(0)
        losses.append(0)
    return playerNames, wins, ties, losses
def findBest(totals,hands):
    highest = 0
    shortest = 999
    for total in totals:
        if total < 22:
            if total > highest:
                highest = total
    for x in range(len(totals)):
        if totals[x] == highest and len(hands[x]) < shortest:
            shortest  = len(hands[x])

    return highest, shortest
def findWinners(totals, hands, losses):
    highest, shortest = findBest(totals,hands)
    winners = []
    for x in range(len(totals)):
        if totals[x] == highest and len(hands[x]) == shortest:
            winners.append(x)
        else:
            losses[x] += 1
    return winners, losses
def addAces(card1,card2,aces):
    if isAce(card1):
        aces.append(11)
    elif isAce(card2):
        aces.append(11)
    return aces
def printWinners(winners,wins,ties):
    if len(winners) > 1:
        names = ""
        string = "The winners are:"
        for name in winners:
            ties[name] += 1
            names += playerNames[name] + " " 
        print(string + names)
    elif len(winners) == 0:
        print('everyone lost.')
    else:
        print('The winner is',playerNames[winners[0]],"!")
        wins[winners[0]] += 1
    return wins, ties
def printData(playerNames, wins, ties, losses, stage,hands,totals):
    for i in range(len(playerNames)):
        hand = ""
        for card in hands[i]:
            hand += (card + ",")
        hand = hand[:-1]
        print(playerNames[i]+" card's include: "+hand+" for a total of:",totals[i],"points.")
    print('\nplayer  |wins|ties|losses|%win/tie|%lose')
    for x in range(len(playerNames)):
        losspercent = round(losses[x]/(stage+1)*100,2)
        winpercent = 100 - losspercent
        print('{}|{}   |{}   |{}     |{}    |{}    '.format(playerNames[x],wins[x],ties[x],losses[x],winpercent,losspercent))
    print('\n\n')


if __name__ == '__main__':
    players = getPlayers()
    deck = createcards() * 8
    rounds = round((52 * 8) / (4 * players))
    random.shuffle(deck)
    playerNames, wins, ties, losses = getpermvalues(players)
    print('max rounds:'+c.y,rounds-1,c.x)
    print('''decks used: 8
note: earlier players are at a disadvantage
if you let other people look at your screen.\n''')
    try:
        input('press enter to continue\n')
        knowsHowToPlay()

        print(c.cl)
        for stage in range(rounds-1):
            firstTime, hands, totals, aces = getroundvalues(players)
            print('round' + c.b,(stage+1),c.x)
            start = input('press enter to start the round, otherwise type anything\n')
            if len(start) != 0:
                exit()
            for z in range(players):
                print(c.cl + c.v+ playerNames[z] + c.x)
                title1, title2, totals[z],deck = getTwoCards(deck)
                hands[z].append(title1)
                hands[z].append(title2)
                aces[z] = addAces(title1,title2,aces[z])
                printHand(title1,title2,totals[z])
                while True:
                    wantsToHit = askToHit(hands[z], firstTime)
                    if wantsToHit == True:
                        firstTime[z] = False
                        totals[z], deck, title = getOneMoreCard(deck,totals[z])
                        if 'ace' in title:
                            aces[z].append(11)
                        hands[z].append(title)
                        if totals[z] > 21:
                            hasAnAce,aces[z] = hasAce(aces[z])
                            if hasAnAce == False:
                                print('Oh No! You busted.')
                                time.sleep(3)
                                if z != players-1:
                                    print(c.cl + c.r+ 'Pass to Next Player within 5 seconds' +c.x)
                                    time.sleep(5)
                                    print(c.cl)
                                    break
                            else:
                                totals[z] -= 10
                                print('You went over, so your ace valued 11 was changed into a 1')
                                print('You now have',totals[z],'points')
                    else:
                        if z != players-1:
                            print(c.cl + c.r + 'Pass to Next Player within 5 seconds' + c.x)
                            time.sleep(5)
                            print(c.cl)
                            break
            winners, losses = findWinners(totals, hands,losses)
            wins, ties = printWinners(winners,wins,ties)
            printData(playerNames, wins, ties, losses, stage,hands,totals)
    except KeyboardInterrupt:
        print(c.cl)
        exit()