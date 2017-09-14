import discord
import wikia
from discord.ext import commands

class WikiaReader:
    
    def __init__(self, bot):
        self.bot = bot
        self.__wiki = "Zelda"
        self.__log = open("test.txt", 'w')
        self.__query = list()
        
     
    def __say(self, message):
       message = str(message)
       await self.bot.say(message)
       #print()
       self.__log.write(message + "\n")
        
    @commands.command()   
    async def WikiQuery(self, message):
        '''This will help you do a query Search of the wiki'''
        query = wikia.search(self.__wiki, message, results=50)
        #log = open("test.txt", 'w')
        queryResults = "We found " + str(len(query)) + " results. Here are the top 10 results!\n"
        self.__say(queryResults)
        
        for i in range(0,10):
            i = i + 1
            await self.bot.say(str(i) + " " +query[i])
    
    
    
def setup(bot):
   n = WikiaReader(bot)
   bot.add_cog(n)