# bot.py
import os
from parse_message import parse_expression
import re
import json

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

named_roll_dict = {}
with open("named_rolls.json") as names_file:
    named_roll_dict = json.load(names_file)

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.casefold() == 'help'.casefold():
        await message.channel.send('helpmsg')
        return
    if message.channel.name != 'rolls':
        return
    
    global named_roll_dict

    processed_content = message.content

    roll_name_match = re.search(r'^".*"',processed_content)
    roll_name = None

    if str(message.author.id) in named_roll_dict and message.content in named_roll_dict[str(message.author.id)]:
        roll_name = message.content
        processed_content = named_roll_dict[str(message.author.id)][message.content]
    elif str(message.author.id) in named_roll_dict and len(message.content) >= 2 and message.content[0] == '"' and message.content[-1] == '"' and message.content[1:-1] in named_roll_dict[str(message.author.id)]:
        roll_name = message.content[1:-1]
        processed_content = named_roll_dict[str(message.author.id)][message.content[1:-1]]
    elif roll_name_match:
        roll_name = roll_name_match.group(0)[1:-1]
        processed_content = processed_content[:roll_name_match.start()]+processed_content[roll_name_match.end():]
        if str(message.author.id) not in named_roll_dict:
            named_roll_dict[str(message.author.id)] = {}
        named_roll_dict[str(message.author.id)][roll_name] = processed_content
        with open("named_rolls.json",'w') as names_file:
            json.dump(named_roll_dict,names_file,indent=4,sort_keys=True)
    
    processed_content = ''.join(processed_content.split())

    processed_content = processed_content.replace('\\','')
    valid_chars_match = re.search(r'^[-\d\.\^\+\*/s_\(\)d]*$',processed_content)
    if not valid_chars_match:
        return
    
    if roll_name == None:
        roll_name = message.content

    output_log = roll_name+' for '+str(message.author.mention)+':\n'
    output_log, expression = parse_expression(output_log, processed_content)

    output_log += expression
    output_log = re.sub(r'(?<!\\)\*','\*',output_log)
    output_log += ' = **'+str(eval(expression))+'**'

    await message.channel.send(output_log)
    return

client.run(TOKEN)