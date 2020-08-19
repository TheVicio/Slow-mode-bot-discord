import discord
import config
import asyncio
from datetime import datetime, timedelta

class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        
        who_cant_say = dict()
        
        @self.event
        async def on_message(message: discord.Message):
            if isinstance(message.channel, discord.TextChannel):
                if not message.author.name in who_cant_say:
                    who_cant_say[message.author.name] = datetime.now() + timedelta(seconds = config.delay)
                else:
                    if datetime.now() < who_cant_say[message.author.name]:
                        await message.delete()
                        DMchannel = await message.author.create_dm()
                        await DMchannel.send(f'O canal está em modo slow mode, você precisa esperar {config.delay} segundos para digitar novamente')
                    else:
                        del who_cant_say[message.author.name]
        
        self.run(config.token)
    
Bot()