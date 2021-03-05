# EggTimerBot
import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import logging
from asyncio import sleep
from sys import platform
from ctypes.util import find_library

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = getenv('BOT_TOKEN')
VOICE_CHANNEL_NAME = getenv('VOICE_CHANNEL_NAME')
EGG_TIMER_CHANNEL_NAME = 'Get the Egg Timer'
GUILD_NAME = getenv('GUILD_NAME')

if platform == "linux" and not discord.opus.is_loaded():
    discord.opus.load_opus(find_library('opus'))

description = 'A bot to deal with slow people.'
intents = discord.Intents.all()

bot = discord.ext.commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith('hello'):
        await message.channel.send('Hello!')

    if 'hurry' in message.content.lower():
        await message.channel.send(f'{message.author.mention} SAYS IT IS TAKING TOO LONG')
        await sleep(2)
        await message.channel.send('GETTING THE EGG TIMER')
        await sleep(2)
        await message.channel.send('STARTING THE EGG TIMER')
        await sleep(2)
        await message.channel.send('HURRY IT UP - TICK TOCK MOTHERFUCKER')


@bot.event
async def on_member_update(before, after):
    channel = discord.utils.get(after.guild.text_channels, name='general')  # general channel in guild
    messages = {'Dr.Phil': f'Hey {after.mention}, I am at your service!',
                'Conn': f'Hey {after.mention}, fuck you!',
                'Ryles': f'All hail {after.mention}, the Creator!'}
    if after.status.value == 'online' and before.status.value != 'online':
        try:
            await channel.send(messages[after.name])
        except KeyError:
            pass


@bot.command()
async def eggtimer(ctx):
    # get voice channel, play bomb noise
    author = ctx.author
    print(author)
    # get authors voice channel and connect
    vstate = author.voice
    print(vstate)
    vclient = await vstate.channel.connect()
    bot.voice_clients.append(vclient)
    print(f'{bot.user} has connected to {vclient}')
    timebomb = discord.FFmpegPCMAudio('TimeBombShort.mp3')
    # check bot method to play audio
    vclient.play(timebomb)

bot.run(TOKEN)
