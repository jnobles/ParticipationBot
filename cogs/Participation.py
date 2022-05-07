import discord
import gspread.exceptions
from discord.ext import commands
import os
from dotenv import load_dotenv
import WorksheetConnection as WSConnection

load_dotenv()
GSHEET_CRED = os.getenv('GOOGLE_SHEET_CREDENTIAL_FILE_PATH')
file = None


class ParticipationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set_sheet',
                      description='Selects a Google Sheet as the target for commands.')
    async def select_sheet(self, ctx, workbook_name, sheet_name=None):
        try:
            global file
            file = WSConnection.WorksheetConnection(GSHEET_CRED)
        except gspread.exceptions.GSpreadException:
            await ctx.send('Failed to authenticate with Google Sheets.  Check that your key file is correctly defined.')
        else:
            await ctx.send(f'{file.open_sheet(workbook_name, sheet_name)}')
            print(file.active_sheet_name)

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
    async def bonus(self, ctx, *, args):
        args = args.splitlines()
        parsed = []
        for line in args:
            temp = ['name', 1]
            input_string = line.split()
            if len(input_string) == 1:
                temp[0] = ''.join(input_string)
                parsed.append(temp)
                continue
            if input_string[-1].isnumeric():
                temp[0] = ' '.join(input_string[:-1])
                temp[1] = int(input_string[-1])
            else:
                temp[0] = ' '.join(input_string)
            parsed.append(temp)

        global file
        message = '```\n'
        # todo: more magic numbers
        for player in parsed:
            try:
                player_row = file.get_player_row_index(player[0])
                previous_points = file.get_cell_value(player_row, 13)
                new_points = int(previous_points) + player[1] if previous_points is not None else player[1]
                file.update_cell_value(player_row, 13, new_points)
                message += f'{player[0]} gains {player[1]} bonus point(s).\n'
            except WSConnection.PlayerNotFound:
                message += f'**{player[0]} not found, {player[1]} point(s) not logged**'
        message += '```'
        await ctx.send(message)

    @log.command(name='poobadoo',
                 description='Awards poobadoo points.')
    async def poobadoo_points(self, ctx, *, args):
        args = args.splitlines()
        parsed = []
        for line in args:
            temp = ['name', 1]
            input_string = line.split()
            temp[1] = input_string[-1]
            temp[0] = ''.join(input_string[:-1])
            parsed.append(temp)

        message = ''
        try:
            # todo: attempt to write to spreadsheet
            message = '```\n'
            message += ''.join([f'{item[0]} gains {item[1]} poobadoo point(s).\n' for item in parsed])
            message += '```'
        except Exception as e:
            message = f'Error parsing: {e}'
        await ctx.send(message)

    @log.command(name='event',
                 description='Awards event participation.')
    async def event_participation(self, ctx, *, args):
        args = args.splitlines()
        parsed = []
        for line in args:
            temp = ['name', False, 1]
            input_string = line.split()
            if len(input_string) == 1:
                temp[0] = ''.join(input_string)
                parsed.append(temp)
                continue
            if '--leader' in input_string:
                temp[1] = True
            if input_string[-1].isnumeric():
                temp[2] = input_string[-1]
            temp[0] = ''.join(input_string[:-1])
            parsed.append(temp)

        message = '```\n'
        try:
            for item in parsed:
                # todo: attempt to write to spreadsheet
                message += ''.join(f'{item[0]}{"(Leader)" if item[1] else ""} gains {item[2]} event point(s).\n')
            message += '```'
        except Exception as e:
            message = f'Error parsing: {e}'
        await ctx.send(message)


def setup(bot):
    bot.add_cog(ParticipationCog(bot))
