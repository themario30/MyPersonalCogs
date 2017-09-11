''' Luigi Poker - Python Version
    This version of Luigi Poker should be used
    to be used in Discord Red.


'''

from random import *
import discord
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
        for x in i:
            self.__deck[x - 1] = Card()
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

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.__inGame = False
        self.__hit = False
        self.pDeck = Deck()
        self.dDeck = Deck()

    @commands.command()
    async def deck(self):
        """This does stuff!"""
        if (self.__inGame == False):
            #Your code will go here
            await self.bot.say("Starting Deck...")
            self.__inGame = True
            self.pDeck.newDeck()
            self.dDeck.newDeck()
            await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(":white_medium_small_square:",":white_medium_small_square:",":white_medium_small_square:",
                ":white_medium_small_square:",":white_medium_small_square:"))
            await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
            await self.bot.say("fold or stay?")

    @commands.command()
    async def hit(self, i):
        '''To indicate which card/s to trade, the first card is 1, second card is 2, etc Ex: [p]hit 2,4,5'''
        if(self.__hit == False):
            l = eval(i)
            await self.bot.say("Swaping Cards...")
            self.pDeck.swap(l)
            await self.bot.say("Cards have been swapped.")
            await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(":white_medium_small_square:",":white_medium_small_square:",":white_medium_small_square:",
                ":white_medium_small_square:",":white_medium_small_square:"))
            await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
            await self.bot.say("fold or stay?")
            self.__hit = True
        else:
            await self.bot.say("You've already hit this round. You must fold or stay.")

    @commands.command()
    async def fold(self):
        if(self.__inGame):
            await self.bot.say("You have Folded.")
            await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(self.dDeck.suit(0),self.dDeck.suit(1),self.dDeck.suit(2),self.dDeck.suit(3),self.dDeck.suit(4)))
            await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
            self.__inGame = False
        else:
            await self.bot.say("There isn't a game going on. Use {}deck to start a game.".format('!'))

    @commands.command()
    async def stay(self):
        if(self.__inGame == True):
            await self.bot.say("You've Stayed.")
            if (flush(self.pDeck) != flush(self.dDeck)):
                if(flush(self.pDeck)):
                    await self.bot.say("You Won! You got a Flush!")
                elif (flush(self.dDeck)):
                    await self.bot.say("You lost! The Dealer got a Flush!")
            elif (flush(self.pDeck) and flush(self.dDeck)):
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    await self.bot.say("You Won! Your Flush is greater than Dealer.")
                elif(self.pDeck.firstPair < self.dDeck.firstPair):
                    await self.bot.say("You Lost! Dealer's Flush is greater than yours.")
                else:
                    await self.bot.say("The Dealer and Player has Tied")
            elif(fourKind(self.pDeck) != fourKind(self.dDeck)):
                if(fourKind(self.pDeck)):
                    await self.bot.say("You Won! You got a Four of a Kind!")
                elif (fourKind(self.dDeck)):
                    await self.bot.say("You lost! The Dealer got a Four of a Kind")
            elif (fourKind(self.pDeck) and fourKind(self.dDeck)):
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    await self.bot.say("You Won! Your Four of a Kind is greater than Dealer.")
                elif(self.pDeck.firstPair < self.dDeck.firstPair):
                    await self.bot.say("You Lost! Dealer's Four of a Kind is greater than yours.")
                else:
                    await self.bot.say("The Dealer and Player has Tied.")
            elif(fullHouse(self.pDeck) != fullHouse(self.dDeck)):
                if(fullHouse(self.pDeck)):
                    await self.bot.say("You Won! You got a Full House!")
                elif (fullHouse(self.dDeck)):
                    await self.bot.say("You lost! The Dealer got a Full House")
            elif (fullHouse(self.pDeck) and fullHouse(self.dDeck)):
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    await self.bot.say("You Won! Your Full House is greater than Dealer.")
                elif(self.pDeck.firstPair < self.dDeck.firstPair):
                    await self.bot.say("You Lost! Dealer's Full House is greater than yours.")
                elif (self.pDeck.secondPair > self.dDeck.secondPair):
                    await self.bot.say("You Won! Your Full House is greater than Dealer.")
                elif(self.pDeck.secondPair < self.dDeck.secondPair):
                    await self.bot.say("You Lost! Dealer's Full House is greater than yours.")
                else:
                    await self.bot.say("The Dealer and Player has Tied.")
            elif(threeKind(self.pDeck) != threeKind(self.dDeck)):
                if(threeKind(self.pDeck)):
                    await self.bot.say("You Won! You got a Three of a Kind!")
                elif (threeKind(self.dDeck)):
                    await self.bot.say("You lost! The Dealer got a Three of a Kind")
            elif (threeKind(self.pDeck) and threeKind(self.dDeck)):
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    await self.bot.say("You Won! Your Three of a Kind is greater than Dealer.")
                elif(self.pDeck.firstPair < self.dDeck.firstPair):
                    await self.bot.say("You Lost! Dealer's Three of a Kind is greater than yours.")
                else:
                    await self.bot.say("The Dealer and Player has Tied.")
            elif(twoPair(self.pDeck) != twoPair(self.dDeck)):
                if(twoPair(self.pDeck)):
                    await self.bot.say("You Won! You got Two Pairs!")
                elif (twoPair(self.dDeck)):
                    await self.bot.say("You lost! The Dealer got Two Pairs!")
            elif (twoPair(self.pDeck) and twoPair(self.dDeck)):
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    await self.bot.say("You Won! Your Two Pairs is greater than Dealer.")
                elif(self.pDeck.firstPair < self.dDeck.firstPair):
                    await self.bot.say("You Lost! Dealer's Two Pairs is greater than yours.")
                elif (self.pDeck.secondPair > self.dDeck.secondPair):
                    await self.bot.say("You Won! Your Two Pairs is greater than Dealer.")
                elif(self.pDeck.secondPair < self.dDeck.secondPair):
                    await self.bot.say("You Lost! Dealer's Two Pairs is greater than yours.")
                else:
                    await self.bot.say("The Dealer and Player has Tied.")
            elif(onePair(self.pDeck) != onePair(self.dDeck)):
                if(onePair(self.pDeck)):
                    await self.bot.say("You Won! You got a Pair!")
                elif (onePair(self.dDeck)):
                    await self.bot.say("You lost! The Dealer got a Pair!")
            elif (onePair(self.pDeck) and onePair(self.dDeck)):
                if (self.pDeck.firstPair > self.dDeck.firstPair):
                    await self.bot.say("You Won! Your Pair is greater than Dealer.")
                elif(self.pDeck.firstPair < self.dDeck.firstPair):
                    await self.bot.say("You Lost! Dealer's Pair is greater than yours.")
                else:
                    await self.bot.say("The Dealer and Player has Tied.")
            else:
                await self.bot.say("Tie! Both the Dealer and the Player has no Match.")

            await self.bot.say("Dealer's Deck: {}{}{}{}{}".format(self.dDeck.suit(0),self.dDeck.suit(1),self.dDeck.suit(2),self.dDeck.suit(3),self.dDeck.suit(4)))
            await self.bot.say("Your Deck: {}{}{}{}{}".format(self.pDeck.suit(0),self.pDeck.suit(1),self.pDeck.suit(2),self.pDeck.suit(3),self.pDeck.suit(4)))
            self.__inGame = False
            self.__hit = False
        else:
            await self.bot.say("There isn't a game going on. Use {}deck to start a game.".format('!'))


def setup(bot):
    bot.add_cog(Mycog(bot))
