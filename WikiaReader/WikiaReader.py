import wikia

class WarframeReader:
    
    
    def __init__(self, bot):
        self.bot = bot
        self.__wiki = "Zelda"
        self.__log = open("test.txt", 'w')
        self.__query = list()
     
    def __say(self, message):
       self.bot.say
       #print()
       self.__log.write(message + "\n")
        
    @commands.command    
    async def search(self, term):
        query = wikia.search(self.__wiki, term, results=50)
        #log = open("test.txt", 'w')
        queryResults = "We found " + str(len(query)) + " results. Here are the top 10 results!\n"
        self.__say(queryResults)
        
        for i in range(0,10):
            i = i + 1
            self.__say(str(i) + " " +query[i])
    
    
    
def setup(bot):
   n = WarframeReader(bot)
   n.search("Gourmet Meat")
    
main()
    