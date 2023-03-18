# bot.py
import os
import random
from parse_message import parse_message

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_error(event, *args, **kwargs):
    return

@client.event
async def on_message(message):

    if message.author == client.user or message.channel.name != 'rolls':
        return
    
    result = '"'+message.content+'" for '+str(message.author.mention)+':\n'+parse_message(message.content)

    await message.channel.send(result)

client.run(TOKEN)