# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv

# loads bot token from local .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# initialize bot to respond to '!' commands
bot = commands.Bot(command_prefix='!')


# prints connection confirmation to console
@bot.event
async def on_ready():
    print('Connected to Discord.')


bot.load_extension('cogs.BotManagement')
bot.load_extension('cogs.Participation')

bot.run(TOKEN)
