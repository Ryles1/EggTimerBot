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
VOICE_CHANNEL_NAME = os.getenv('VOICE_CHANNEL_NAME')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # get list of guilds that bot is a member
    guilds = client.guilds

    # get list of member objects from list of guilds
    member_obj_list = [member for guild in guilds for member in guild.members]

    # get voice channel for checking state and if anyone is in it
    voice_channels = [chan for guild in guilds for chan in guild.voice_channels]
    voice_chan_obj = discord.utils.get(voice_channels, name=VOICE_CHANNEL_NAME)

    # make VoiceState objects for checking status
    voice_state_none = discord.VoiceState(data=dict(channel=None))
    voice_state_in_channel = discord.VoiceState(data=dict(channel=voice_chan_obj))

    print(guilds)


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

async def on_voice_state_update(member, ):
    pass

client.run(TOKEN)

