# bot.py
import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# loads bot token from local .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# initialize bot to respond to '!' commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# prints connection confirmation to console
@bot.event
async def on_ready():
    print('Connected to Discord.')


async def main():
    async with bot:
        await bot.load_extension('cogs.BotManagement')
        await bot.load_extension('cogs.Participation')
        await bot.start(TOKEN)


asyncio.run(main())
