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

@bot.command()
async def
