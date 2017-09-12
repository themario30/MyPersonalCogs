''' Luigi Poker - Python Version
    This version of Luigi Poker should be used
    to be used in Discord Red.


'''

import discord
from random import randint
from discord.ext import commands

class Card:
    def __init__(self):
        self.__number = randint(1,6)
        self.__suit = self.__suit()

    def __suit(self): #Names the suit based on the number
        if (self.__number == 1):
            suit = ":one:" #suit = "Cloud"
        elif (self.__number == 2):
            suit = ":two:" #suit = "Mushroom"
        elif (self.__number == 3):
            suit = ":three:" #suit = "Fireflower"
        elif (self.__number == 4):
            suit = ":four:" #suit = "Luigi"
        elif (self.__number == 5):
            suit = ":five:"#suit = "Mario"
        elif (self.__number == 6):
            suit = ":six:"#suit = "Starman"
        else:
            suit = "Error!"

        return suit

    def __repr__(self): #Used for the sort function
        return '{}: {}'.format(self.__suit,self.__number)

    def num(self):
        return self.__number
    def suit(self):
        return self.__suit

def getNum(card): #Used for the sort function
    return card.num()

class Deck:
    def __init__(self): #Deck Initiations
        self.__length = 5
        self.__deck = self.__createDeck()
        self.firstPair = 0  #First Pair and Second Pair Initiated incase
        self.secondPair = 0 #there are ties between dealer and player
        self.newDeck()

    def __createDeck(self): #Create a deck
        temp = [Card() for x in range(0,self.__length)]
        return temp

    def __newCard(self,i):
        self.__deck[i] = Card()

    def __sortDeck(self):   #Sorts the deck
        self.__deck.sort(key=lambda x: x.num(),reverse=True)
    def newDeck(self):      #This Function should be called every new deck
        self.__deck = self.__createDeck()
        self.__sortDeck()

    def deck(self): #
        return self.__deck

    def num(self,i):
        return self.__deck[i].num()

    def swap(self,i):
        l = eval(i)
        if i.isdigit():
            self.__deck[l-1] = Card()
        else:
            for x in l:
                self.__newCard(x-1)
        self.__sortDeck()

    def suit(self,i):
        return self.__deck[i].suit()

    def len(self):
        return self.__length

def onePair(deck):
    answer = False
    for x in range(0,deck.len() - 1):
        if (deck.num(x) == deck.num(x+1)):
            deck.firstPair = deck.num(x)
            answer = True

    return answer

def twoPair(deck):
    answer = False
    firstPair = 0
    secondPair = 0

    for x in range(0,deck.len() - 1):
        if (deck.num(x) == deck.num(x+1)):
            if (firstPair == 0):
                firstPair = deck.num(x)
            elif (firstPair != deck.num(x) and secondPair == 0):
                secondPair = deck.num(x)

    if (firstPair != 0 and secondPair != 0):
        deck.firstPair = firstPair
        deck.secondPair = secondPair
        answer = True

    return answer

def threeKind(deck):
    answer = False
    for x in range(0,deck.len() - 2):
        if (deck.num(x) == deck.num(x+1) and deck.num(x+1) == deck.num(x+2)):
            deck.firstPair = deck.num(x)
            answer = True

    return answer

def fullHouse(deck):
    answer = False
    firstPair = 0
    secondPair = 0
    for x in range(0,deck.len() - 2):
        if (deck.num(x) == deck.num(x+1) and deck.num(x+1) == deck.num(x+2)):
            if(firstPair == 0):
                firstPair = deck.num(x)
    for x in range(0,deck.len() - 1):
        if (deck.num(x) == deck.num(x+1)):
            if(firstPair != deck.num(x) and secondPair == 0):
                secondPair = deck.num(x)

    if (firstPair != 0 and secondPair != 0):
        deck.firstPair = firstPair
        deck.secondPair = secondPair
        answer = True


    return answer

def fourKind(deck):
    answer = False
    for x in range(0,deck.len() - 3):
        if (deck.num(x) == deck.num(x+1) and deck.num(x+1) == deck.num(x+2)
            and deck.num(x+2) == deck.num(x+3)):
            deck.firstPair = deck.num(x)
            answer = True

    return answer

def flush(deck):
    answer = False
    x = 0
    if (deck.num(x) == deck.num(x+1) and deck.num(x+1) == deck.num(x+2)
        and deck.num(x+2) == deck.num(x+3) and deck.num(x+3) == deck.num(x+4)):
        deck.firstPair = deck.num(x)
        answer = True

    return answer

''' Below This Line is Discord Bot Time '''

class LuigiPoker:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.user = ""
        self.__inGame = False
        self.__hit = False
        self.pDeck = Deck()
        self.dDeck = Deck()

    @commands.command()
    async def LuigiHelpMe(self):
        await self.bot.say("``Luigi``\nI am Luigi, Number #1! This game runs the same as Luigi's Poker in Super Mario 64 DS Minigames.")
        await self.bot.say("The Card's worth is dependant from their number. \nFor example, a 6 has greater worth than a 5, a 5 has greater worth than a 4, etc, etc. ")
        await self.bot.say("The following table represents the winning matches. How close from the top represents their worth.\nFor example, A Full House is greater than Three of a Kind, but less than a Four of a Kind.")
        flush =     "Flush:           {}{}{}{}{}".format(":six:",":six:",":six:",":six:",":six:")
        fourKind =  "Four of a Kind:  {}{}{}{}".format(":six:",":six:",":six:",":six:")
        fullHouse = "Full House:      {}{}{}{}{}".format(":six:",":six:",":six:",":three:",":three:")
        threeKind = "Three of a Kind: {}{}{}".format(":six:",":six:",":six:")
        twoP =      "Two Pairs:       {}{}{}{}".format(":six:",":six:",":one:",":one:")
        oneP =      "Pair:            {}{}".format(":six:",":six:")
        await self.bot.say("{}\n{}\n{}\n{}\n{}\n{}".format(flush,fourKind,fullHouse,threeKind,twoP,oneP))

    @commands.command()
    async def deck(self):
        """Starts the Game! Use !deckHelp for game help"""
        if (self.__inGame == False):
            await self.bot.say("Starting Deck...")
            self.__inGame = True
            self.pDeck.newDeck()
            self.dDeck.newDeck()
        else:
            await self.bot.say("You're already in a game...")

        await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(":white_medium_small_square:",":white_medium_small_square:",":white_medium_small_square:",
            ":white_medium_small_square:",":white_medium_small_square:"))
        await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
        if (self.__hit):
            await self.bot.say("Stay or Fold?")
        else:
            await self.bot.say("Stay, Hit, or Fold?")

    @commands.command()
    async def hit(self, i):
        '''To indicate which card/s to trade, the first card is 1, second card is 2, etc Ex: [p]hit 2,4,5'''
        if(self.__inGame):
            if(self.__hit == False):
                await self.bot.say("Swaping Cards...")
                self.pDeck.swap(i)
                await self.bot.say("Cards have been swapped.")
                await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(":white_medium_small_square:",":white_medium_small_square:",":white_medium_small_square:",
                    ":white_medium_small_square:",":white_medium_small_square:"))
                await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
                await self.bot.say("Stay or Fold?")
                self.__hit = True
            else:
                await self.bot.say("You've already hit this round. You must Stay or Fold.")
        else:
            await self.bot.say("There isn't a game going on. Use {}deck to start a game.".format('!'))

    @commands.command()
    async def fold(self):
        if(self.__inGame):
            await self.bot.say("You have Folded.")
            await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(self.dDeck.suit(0),self.dDeck.suit(1),self.dDeck.suit(2),self.dDeck.suit(3),self.dDeck.suit(4)))
            await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
            self.__inGame = False
            self.__hit = False
        else:
            await self.bot.say("There isn't a game going on. Use {}deck to start a game.".format('!'))

    @commands.command()
    async def stay(self):
        say = ""
        win = False
        sameMove = False
        tied = False
        if(self.__inGame == True):
            await self.bot.say("You've stayed.")
            if (flush(self.pDeck) != flush(self.dDeck)):
                say = "a Flush"
                if(flush(self.pDeck)):
                    win = True
            elif (flush(self.pDeck) and flush(self.dDeck)):
                say = "Flush"
                sameMove = True
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    win = True
                elif(self.pDeck.firstPair == self.dDeck.firstPair):
                    tied = True
            elif(fourKind(self.pDeck) != fourKind(self.dDeck)):
                say = "a Four of a Kind"
                if(fourKind(self.pDeck)):
                    win = True
            elif (fourKind(self.pDeck) and fourKind(self.dDeck)):
                say = "Four of a Kind"
                sameMove = True
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    win = True
                elif(self.pDeck.firstPair == self.dDeck.firstPair):
                    tied = True
            elif(fullHouse(self.pDeck) != fullHouse(self.dDeck)):
                say = "a Full House"
                if(fullHouse(self.pDeck)):
                    win = True
            elif (fullHouse(self.pDeck) and fullHouse(self.dDeck)):
                say = "Full House"
                sameMove = True
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    win = True
                elif (self.pDeck.secondPair > self.dDeck.secondPair):
                    win = True
                elif(self.pDeck.firstPair == self.dDeck.firstPair and self.pDeck.secondPair == self.dDeck.secondPair):
                    tied = True
            elif(threeKind(self.pDeck) != threeKind(self.dDeck)):
                say = "a Three of a Kind"
                if(threeKind(self.pDeck)):
                    win = True
            elif (threeKind(self.pDeck) and threeKind(self.dDeck)):
                say = "Three of a Kind"
                sameMove = True
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    win = True
                elif(self.pDeck.firstPair == self.dDeck.firstPair):
                    tied = True
            elif(twoPair(self.pDeck) != twoPair(self.dDeck)):
                say = "Two Pairs"
                if(twoPair(self.pDeck)):
                    win = True
            elif (twoPair(self.pDeck) and twoPair(self.dDeck)):
                say = "Two Pairs"
                sameMove = True
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    win = True
                elif (self.pDeck.secondPair > self.dDeck.secondPair):
                    win = True
                elif(self.pDeck.firstPair == self.dDeck.firstPair and self.pDeck.secondPair == self.dDeck.secondPair):
                    tied = True
            elif(onePair(self.pDeck) != onePair(self.dDeck)):
                say = "a Pair"
                if(onePair(self.pDeck)):
                    win = True
            elif (onePair(self.pDeck) and onePair(self.dDeck)):
                say = "Pair"
                sameMove = True
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    win = True
                elif(self.pDeck.firstPair == self.dDeck.firstPair):
                    tied = True
            else:
                tied = True

            if(sameMove):
                if(win):
                    await self.bot.say("You won! Your {} is greater than Dealer's {}!".format(say,say))
                else:
                    await self.bot.say("You lost! The Dealer's {} is greater than your {}!".format(say,say))
            elif(win):
                await self.bot.say("You won! You got {}!".format(say))
            elif(tied):
                await self.bot.say("Both the Dealer and the Player have Tied")
            else:
                await self.bot.say("You lost! The Dealer got {}".format(say))

            await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(self.dDeck.suit(0),self.dDeck.suit(1),self.dDeck.suit(2),self.dDeck.suit(3),self.dDeck.suit(4)))
            await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
            self.__inGame = False
            self.__hit = False
        else:
            await self.bot.say("There isn't a game going on. Use {}deck to start a game.".format('!'))


def setup(bot):
	n = LuigiPoker(bot)
    bot.add_cog(n)
