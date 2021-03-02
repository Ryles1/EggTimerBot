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


async def on_message(self, message):
    if message.author == self.user:
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
        if message.author.voice:
            await self.play_bomb(message.author.voice.channel)


async def on_member_update(before, after):
    if after.status == 'online' and before.status != 'online':
        if before.name == 'Dr.Phil':
            await message_drphil(after)
        if before.name == 'Conn':
            await message_conn(after)


async def message_conn(member):
    conn = discord.utils.get(member.guilds, name='Conn')   # member object for conn
    guild = discord.utils.get(member.guilds, name=GUILD_NAME)  # guild object
    channel = discord.utils.get(guild.text_channels, name='general')  # general channel in guild
    if conn:
        await channel.send(f'Hey {conn.mention}, fuck you!')


async def message_drphil(member):
    dr_phil = discord.utils.find(lambda m: m.name == 'Dr.Phil', member.guilds)   # member object for Dr.Phil
    guild = discord.utils.get(member.guilds, name=GUILD_NAME)  # guild object
    channel = discord.utils.get(guild.text_channels, name='general')  # general channel in guild
    if dr_phil:
        await channel.send(f'Hey {dr_phil.mention}, I am at your service!')


@bot.command()
async def time_bomb(ctx):
    #get voice channel, play bomb noise
    if self.current_voice_chan is not None:
        vc = await self.current_voice_chan.connect()
        print(f'{self.user} has connected to {self.current_voice_chan}')
        timebomb = discord.FFmpegPCMAudio('TimeBombShort.mp3')
        vc.play(timebomb)

bot.run(TOKEN)
