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
        for file in [file for file in os.listdir('./cogs') if file.endswith('.py')]:
            cog_list += f'{file[:-3]}: '
            try:
                self.bot.load_extension(f'cogs.{file[:-3]}')
            except commands.ExtensionAlreadyLoaded:
                cog_list += 'Loaded\n'
            else:
                self.bot.unload_extension(f'cogs.{file[:-3]}')
                cog_list += 'Unloaded'
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

    @cog.command(name='reload_all',
                 description='Reloads all currently loaded cogs.',
                 hidden=True)
    async def reload_all(self, ctx):
        reloaded_cogs_list = 'Reloaded the following cogs:\n```\n'
        for file in [file for file in os.listdir('./cogs') if file.endswith('.py')]:
            try:
                self.bot.load_extension(f'cogs.{file[:-3]}')
            except commands.ExtensionAlreadyLoaded:
                self.bot.reload_extension(f'cogs.{file[:-3]}')
                reloaded_cogs_list += f'{file[:-3]}\n'
        reloaded_cogs_list += '```'
        await ctx.send(reloaded_cogs_list)


def setup(bot):
    bot.add_cog(BotManagementCog(bot))
