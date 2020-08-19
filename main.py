import discord
import config
import asyncio
import commands
from datetime import datetime, timedelta
import re
import functions

class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        
        who_cant_say = dict()
        
        @self.event
        async def on_message(message: discord.Message):
            setdelay = re.findall(r'^\!slowmode set ([0-9]+)', message.content)
            
            if isinstance(message.channel, discord.TextChannel) and config.slowmode and not message.author.id in functions.load_json('whitelist.json')['whitelist']:
                if not message.author.id in who_cant_say:
                    who_cant_say[message.author.id] = datetime.now() + timedelta(seconds = config.delay)
                else:
                    if datetime.now() < who_cant_say[message.author.id]:
                        await message.delete()
                        await self.send_dm(f'O canal está em modo slow mode, você precisa esperar {config.delay} segundos para digitar novamente.', message)
                    else:
                        del who_cant_say[message.author.id]
                        
            if message.content.lower().startswith(commands.APPEND_TO_WHITELIST):
                if len(message.mentions) == 1:
                    base = functions.load_json('whitelist.json')
                    if not message.mentions[0].id in base['whitelist']:
                        base['whitelist'].append(message.mentions[0].id)
                        functions.save_json('whitelist.json', base)
            elif message.content.lower().startswith(commands.REMOVE_FROM_WHITELIST):
                if len(message.mentions) == 1:
                    base = functions.load_json('whitelist.json')
                    if message.mentions[0].id in base['whitelist']:
                        base['whitelist'].remove(message.mentions[0].id)
                        functions.save_json('whitelist.json', base)
            
            elif setdelay:
                if message.author.id == message.guild.owner_id:
                    config.delay = int(setdelay[0])
                    await self.send_dm(f'O slowmode foi definido para {config.delay} segundos.', message)
                else:
                    await self.send_dm('Apenas o dono do servidor pode modificar o slow mode.', message)
                    
            elif message.content.lower() == commands.TO_ACTIVE:
                if message.author.id == message.guild.owner_id:
                    config.slowmode = True
                    await self.send_dm('O slowmode foi ativado.', message)
                else:
                    await self.send_dm('Apenas o dono do servidor pode ativar ou desativar o slow mode.', message)
                
            elif message.content.lower() == commands.TO_DESACTIVE:
                if message.author.id == message.guild.owner_id:
                    config.slowmode = False
                    await self.send_dm('O slowmode foi desativado.', message)
                else:
                    await self.send_dm('Apenas o dono do servidor pode ativar ou desativar o slow mode.', message)
            
        self.run(config.TOKEN)
                    
    async def send_dm(self, content: str, message:discord.Message):
        DMchannel = await message.author.create_dm() if not message.author.dm_channel else message.author.dm_channel
        await DMchannel.send(content)
    
Bot()