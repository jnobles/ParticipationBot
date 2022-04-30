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


bot.load_extension('cogs.Participation')


# advises of lacking role on command usage check
# raises any other error to the console
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        raise

bot.run(TOKEN)
