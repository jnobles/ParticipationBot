# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv

# loads bot token from local .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# initialized bot to respond to '!' commands
bot = commands.Bot(command_prefix='!')


# prints connection confirmation to console
@bot.event
async def on_ready():
    print("connected")


# parses and logs participation, can only be invoked by Mysterium members
# takes input in the form of 'name [optional value]\n' for any number of lines
@bot.command(name='participation', help='Logs participation')
@commands.has_role('Mysterium')
async def log_participation(ctx):
    args = str(ctx.message.content).splitlines()[1:]
    parsedInput = parse_participation(args)
    message = ''
    for line in parsedInput:
        message += f'{line[0]} gains {line[1]} point(s)\n'
    await ctx.send(message)


# parses input into a list of the form [[member, points]], if no point value is indicated, defaults to 1 point
def parse_participation(args):
    parsed = []
    for line in args:
        temp = ['name', 1]
        if line.split()[-1].isnumeric():
            temp[1] = line.split()[-1]
            temp[0] = ''.join(line.split()[:-1])
        else:
            temp[0] = ''.join(line)
        parsed.append(temp)
    return parsed


# advises of lacking role on command usage check
# raises any other error to the console
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        raise

bot.run(TOKEN)
