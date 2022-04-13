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


# parses and logs participation, can only be invoked by Mysterium members
# takes input in the form of 'name [optional value]\n' for any number of lines
@bot.command(name='participation', help='Logs participation')
@commands.has_role('Mysterium')
async def log_participation(ctx, *, args):
    parsed_input = parse_participation(args)
    message = ''
    for line in parsed_input:
        message += f'{line[0]} gains {line[1]} point(s)\n'
    await ctx.send(message)


# parses input into a list of lists in the form [[member, leads, events]], if no point value is indicated,
# defaults to 1 point
def parse_participation(args):
    args = args.splitlines()
    parsed = []
    for line in args:
        temp = ['name', 1]
        if line.split()[-1].isnumeric():
            temp[1] = line.split()[-1]
            temp[0] = ''.join(line.split()[:-1])
        else:
            temp[0] = ''.join(line)
        parsed.append(temp)
    print(parsed)
    return parsed


def add_participation(playername, leads=0, events=0):
    playerfound = False
    row = 1
    for row in range(1, len(sheetData)+1):
        if sheetData[row-1][0] == playername:
            playerfound = True
            active_sheet.update_cell(row, 3, int(sheetData[row-1][2]) + leads)
            active_sheet.update_cell(row, 4, int(sheetData[row-1][3]) + events)
            break

    if playerfound:
        message = f'{playername} gained {leads} point(s) for leading and {events} point(s) for participating.'
    else:
        message = f'{playername} not found.  Failed to add {leads} point(s) for leading and {events} ' \
                  f'point(s) for participating.'

    return message


# advises of lacking role on command usage check
# raises any other error to the console
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        raise

bot.run(TOKEN)
