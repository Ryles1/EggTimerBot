# EggTimerClient.py
import discord
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

class EggTimer(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.member_obj_list = []
        self.voice_channels = []
        self.current_voice_chan = None
        # make VoiceState objects for checking status
        self.voice_state_none = discord.VoiceState(data=dict(channel=None))
        self.voice_state_in_channel = None

    async def on_connect(self):
        # get list of member objects from list of guilds
        self.member_obj_list = [member for guild in self.guilds for member in guild.members]
        # check for anyone in desired voice channels
        self.check_vcs()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

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

    async def on_member_update(self, member):
        if member.name == 'Dr.Phil':
            await self.message_drphil()
        if member.name == 'Conn':
            await self.message_conn()
        self.check_vcs()

    async def play_bomb(self, channel):
        if self.current_voice_chan is not None:
            vc = await self.current_voice_chan.connect()
            print(f'{self.user} has connected to {self.current_voice_chan}')
            timebomb = discord.FFmpegPCMAudio('TimeBombShort.mp3')
            vc.play(timebomb)

    def check_vcs(self):
        # get VoiceChannel object for checking state and if anyone is in it
        self.voice_channels = [chan for chan in self.get_all_channels() if isinstance(chan, discord.VoiceChannel)]
        self.current_voice_chan = discord.utils.get(self.voice_channels, name=VOICE_CHANNEL_NAME)
        if self.current_voice_chan is None:
            self.current_voice_chan = discord.utils.get(self.voice_channels, name="General")

        # get VoiceState object for selected voice channel
        self.voice_state_in_channel = discord.VoiceState(data=dict(channel=self.current_voice_chan))

    async def message_conn(self):
        conn = discord.utils.get(self.guilds.members, name='Conn')   # member object for conn
        guild = discord.utils.get(self.guilds, name=GUILD_NAME)
        channel = discord.utils.get(guild.text_channels, name='general')
        if conn:
            await channel.send(f'Hey {conn.mention}, fuck you!')

    async def message_drphil(self):
        dr_phil = discord.utils.find(lambda m: m.name == 'Dr.Phil', self.guilds.members)   # member object for Dr.Phil
        guild = discord.utils.get(self.guilds, name=GUILD_NAME)
        channel = discord.utils.get(guild.text_channels, name='general')
        if dr_phil:
            await channel.send(f'Hey {dr_phil.mention}, I am at your service!')



client = EggTimer()
client.run(TOKEN)