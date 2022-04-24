# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
import WorksheetConnection as WSConnection

# loads bot token from local .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GSHEET_CRED = os.getenv('GOOGLE_SHEET_CREDENTIAL_FILE_PATH')
active_file = active_sheet = None

# initialize bot to respond to '!' commands
bot = commands.Bot(command_prefix='!')


# prints connection confirmation to console
@bot.event
async def on_ready():
    print("Connected to Discord.")


@bot.command(name='set_sheet', help='Selects a Google Sheet as the target for commands.')
async def select_google_sheet(ctx, workbook_name, sheet_name=None):
    try:
        global active_file
        active_file = WSConnection.WorksheetConnection(GSHEET_CRED)
    except WSConnection.AuthenticationFailed:
        await ctx.send('Failed to authenticate with Google Sheets.  Check that your key file is correctly defined.')
    else:
        global active_sheet
        active_sheet = active_file.open_sheet(workbook_name, sheet_name)
        print(f'{active_sheet.file_name} is open for editing.')


# parses and logs participation, can only be invoked by Mysterium members
# takes input in the form of 'name [optional value]\n' for any number of lines
@bot.command(name='participation', help='Logs participation')
async def log_participation(ctx, *, args):
    if len(args) == 0 or "\n" not in args:
        await ctx.send(
            "Press Shift+Enter to enter multiple lines in one message.\n"
            "Your command should be in the form of:\n"
            "!participation\n"
            "Player Name [leader] [participation points]\n"
            "with each new player on a new line.  If the player lead the event, type \"leader\" after their name.  "
            "You may manually specify the number of participation points granted.  If no number is specified, 1 point "
            "is given.")
    parsed_input = event_participation(args)
    message = ''
    for line in parsed_input:
        print(f"Name: {parsed_input[0]}, Leader: {parsed_input[1]}, Participation Points: {parsed_input[2]}")
    await ctx.send(message)


# todo: bonus points (player and points)
# todo: poobadoo participation (player and points)
def poobadoo_points(args):
    args = args.splitlines()
    parsed = []
    for line in args:
        temp = ['name', 1]
        input_string = args.split()
        temp[1] = input_string[-1]
        temp[0] = input_string[:-1]
        parsed.append(temp)


# todo: event participation (leader and players)
def event_participation(args):
    args = args.splitlines()
    parsed = []
    for line in args:
        temp = ['name', False, 1]
        input_string = line.split()
        if len(input_string) == 1:
            temp[0] = ''.join(input_string)
            break
        if 'leader' in input_string.tolower():
            # todo: this check will not work correctly if someone has a name containing a space and any part of their
            #   name that isn't the first word contains the word 'leader'
            temp[1] = True
        if input_string[-1].isnumeric():
            temp[2] = input_string[-1]
        temp[0] = ''.join(input_string[:-1])
        parsed.append(temp)
    return parsed


# todo: rewrite call to WorksheetConnection.py for writing to sheet; parsing of bot commands has changed


# advises of lacking role on command usage check
# raises any other error to the console
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        raise

bot.run(TOKEN)
