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

        # get VoiceChannel object for checking state and if anyone is in it
        self.voice_channels = [chan for guild in self.guilds for chan in guild.voice_channels]
        self.current_voice_chan = discord.utils.get(self.voice_channels, name=VOICE_CHANNEL_NAME)

        # get VoiceState object for selected voice channel
        self.voice_state_in_channel = discord.VoiceState(data=dict(channel=self.current_voice_chan))

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')


    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower().startswith('hello'):
            await message.channel.send('Hello!')

        if 'hurry' in message.content.lower():
            await message.channel.send(f'{str(message.author).split("#")[0].upper()} SAYS IT IS TAKING TOO LONG')
            await sleep(2)
            await message.channel.send('GETTING THE EGG TIMER')
            await sleep(2)
            await message.channel.send('STARTING THE EGG TIMER')
            await sleep(2)
            await message.channel.send('HURRY IT UP')

client = EggTimer()

client.run(TOKEN)

