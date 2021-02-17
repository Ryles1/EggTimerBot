# EggTimerBot.py
import discord
import os
from dotenv import load_dotenv
import logging
from asyncio import sleep

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('hello'):
        await message.channel.send('Hello!')

    if 'hurry' in message.content.lower():
        await message.channel.send(f'{str(message.author).upper()} SAYS IT IS TAKING TOO LONG')
        await sleep(2)
        await message.channel.send('GETTING THE EGG TIMER')
        await sleep(2)
        await message.channel.send('STARTING THE EGG TIMER')
        await sleep(2)
        await message.channel.send('HURRY IT UP')

client.run(TOKEN)
