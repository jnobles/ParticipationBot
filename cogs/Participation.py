import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import WorksheetConnection as WSConnection

load_dotenv()
GSHEET_CRED = os.getenv('GOOGLE_SHEET_CREDENTIAL_FILE_PATH')
active_file = active_sheet = None


class ParticipationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set_sheet',
                      description='Selects a Google Sheet as the target for commands.')
    async def select_google_sheet(self, ctx, workbook_name, sheet_name=None):
        try:
            global active_file
            active_file = WSConnection.WorksheetConnection(GSHEET_CRED)
        except WSConnection.AuthenticationFailed:
            await ctx.send('Failed to authenticate with Google Sheets.  Check that your key file is correctly defined.')
        else:
            global active_sheet
            active_sheet = active_file.open_sheet(workbook_name, sheet_name)
            print(f'{active_sheet.file_name} is open for editing.')

    @commands.group(invoke_without_command=True)
    async def log(self, ctx):
        message = 'Available subcommands are:\n```'
        for command in commands.Cog.walk_commands(self):
            try:
                if command.parent.name == 'log':
                    message += f'{command.parent.name} {command.name}: {command.description}\n'
            except AttributeError:
                continue
        message += '```'
        await ctx.send(message)

    @log.command(name='bonus',
                 description='Awards bonus points.')
    async def bonus(self, ctx, *, args: str):
        # todo: write parsing function
        await ctx.send(f'{args}')

    @log.command(name='poobadoo',
                 description='Awards poobadoo points.')
    async def poobadoo_points(self, ctx, *, args: str):
        args = args.splitlines()
        parsed = []
        for line in args:
            temp = ['name', 1]
            input_string = args.split()
            temp[1] = input_string[-1]
            temp[0] = input_string[:-1]
            parsed.append(temp)

    @log.command(name='event',
                 description='Awards event participation.')
    async def event_participation(self, ctx, *, args: str):
        args = args.splitlines()
        parsed = []
        for line in args:
            temp = ['name', False, 1]
            input_string = line.split()
            if len(input_string) == 1:
                temp[0] = ''.join(input_string)
                break
            if 'leader' in input_string.tolower():
                # todo: this check will not work correctly if someone has a name containing a space and any part of
                #  their name that isn't the first word contains the word 'leader'
                temp[1] = True
            if input_string[-1].isnumeric():
                temp[2] = input_string[-1]
            temp[0] = ''.join(input_string[:-1])
            parsed.append(temp)
        return parsed

    # todo: rewrite call to WorksheetConnection.py for writing to sheet; parsing of bot commands has changed


def setup(bot):
    bot.add_cog(ParticipationCog(bot))
