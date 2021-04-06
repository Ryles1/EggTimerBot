# EggTimerBot
import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import logging
from asyncio import sleep
from sys import platform
from ctypes.util import find_library

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load env variables
load_dotenv()
TOKEN = getenv('BOT_TOKEN')
VOICE_CHANNEL_NAME = getenv('VOICE_CHANNEL_NAME')
EGG_TIMER_CHANNEL_NAME = 'Get the Egg Timer'
GUILD_NAME = getenv('GUILD_NAME')

# Below two lines are required to find the opus library on linux.
if platform == "linux" and not discord.opus.is_loaded():
    discord.opus.load_opus(find_library('opus'))

# Instantiate bot object
description = 'A bot to deal with slow people.'
intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', description=description, intents=intents)


@client.command(description="Gets the egg timer!")
async def eggtimer(ctx):
    # get voice channel, play bomb noise
    author = ctx.author
    try:
        vstate = author.voice   # get authors voice channel and connect
        vclient = await vstate.channel.connect()
        client.voice_clients.append(vclient)
        print(f'{client.user} has connected to {vclient}')
        timebomb = discord.FFmpegPCMAudio('TimeBombShort.mp3')
        vclient.play(timebomb)
    except AttributeError:
        await ctx.channel.send(f"Silly {author.mention}, you're not in a voice channel!")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    if 'hurry' in message.content.lower():
        await message.channel.send(f'{message.author.mention} SAYS IT IS TAKING TOO LONG')
        await sleep(2)
        await message.channel.send('GETTING THE EGG TIMER')
        await sleep(2)
        await message.channel.send('STARTING THE EGG TIMER')
        await sleep(2)
        await message.channel.send('HURRY IT UP - TICK TOCK MOTHERFUCKER')


@client.event
async def on_member_update(before, after):
    channel = discord.utils.get(after.guild.text_channels, name='general')  # general channel in guild
    messages = {'Dr.Phil': f'Hey {after.mention}, I am at your service!',
                'Conn': f'Hey {after.mention}, fuck you!',
                'Ryles': f'All hail {after.mention}, the Creator!',
                'zxKylexz': f'Hey everyone! {after.mention} is here, spreading coronavirus everywhere!'}
    if after.status.value == 'online' and before.status.value != 'online':
        try:
            await channel.send(messages[after.name])
        except KeyError:
            pass


client.run(TOKEN)
