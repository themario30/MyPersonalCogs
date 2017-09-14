from parse import *
import discord
import wikia
from discord.ext import commands

class WikiaReader:
    
    def __init__(self, bot):
        self.bot = bot
        self.__wiki = "Zelda"
        self.__log = open("test.txt", 'w')
        self.__query = list()
        
    def __query(self, term):
        query = wikia.search(self.__wiki, message, results=50)
        queryResults = "We found " + str(len(query)) + " results. Here are the top 10 results!\n"
        await self.bot.say(queryResults)
        
        queryMessage = "";
        
        for i in range(0,10):
            i = i + 1
            queryMessage += str(i) + " " +query[i] + "\n";
            
        await self.bot.say(queryMessage)
        await self.bot.say("Please select which one you'll like to choose using [p]Wikia select [#]")
        
    @commands.command()   
    async def Wikia(self, message):
        '''Base Command for everything Wikia!'''
        cmd,input = parse("{0} {1}", message)
        await self.bot.say("CMD: " + cmd + " input: " +  input)
        
    
    
def setup(bot):
   n = WikiaReader(bot)
   bot.add_cog(n)