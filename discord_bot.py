# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# loads bot token from local .env file
load_dotenv()

# initialize bot to respond to '!' commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# prints connection confirmation to console
@bot.event
async def on_ready():
    print('Connected to Discord.')



bot.load_extension('cogs.BotManagement')
bot.load_extension('cogs.Participation')

bot.run(os.getenv('DISCORD_TOKEN'))
