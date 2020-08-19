import discord
import config

class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        
        @self.event
        def on_ready():
            print('Bot inicializado')
            
        @self.event
        def on_message(message):
            pass
        
        self.run(config.token)
    