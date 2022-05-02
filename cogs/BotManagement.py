import discord
from discord.ext import commands
import os


class BotManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=False)
    async def cog(self, ctx):
        pass

    @cog.command(name='list',
                 description='Lists available cogs and their load status',
                 hidden=True)
    async def list(self, ctx):
        cog_list = '```\n'
        for file in [f for f in os.listdir('./cogs') if f.endswith('.py')]:
            cog_list += f'{file[:-3]}\n'
        cog_list += '```'
        await ctx.send(cog_list)

    @cog.command(name='load',
                 description='Loads specified cog',
                 hidden=True)
    async def load(self, ctx, cog_name):
        try:
            self.bot.load_extension(f'cogs.{cog_name}')
        except commands.ExtensionError as e:
            await ctx.send(f'There was a problem loading \'{cog_name}\'.\nNote: Cog names are case sensitive.')
        else:
            await ctx.send(f'Cog \'{cog_name}\' has been loaded.')

    @cog.command(name='unload',
                 description='Unloads specified cog',
                 hidden=True)
    async def unload(self, ctx, cog_name):
        try:
            self.bot.unload_extension(f'cogs.{cog_name}')
        except commands.ExtensionError as e:
            await ctx.send(f'There was a problem unloading \'{cog_name}\'.\nNote: Cog names are case sensitive.')
        else:
            await ctx.send(f'Cog \'{cog_name}\' has been unloaded.')

    @cog.command(name='reload',
                 description='Reloads specified cog',
                 hidden=True)
    async def reload(self, ctx, cog_name):
        try:
            self.bot.reload_extension(f'cogs.{cog_name}')
        except commands.ExtensionError as e:
            await ctx.send(f'There was a problem reloading \'{cog_name}\'.\nNote: Cog names are case sensitive.')
        else:
            await ctx.send(f'Cog \'{cog_name}\' has been reloaded.')


def setup(bot):
    bot.add_cog(BotManagementCog(bot))
