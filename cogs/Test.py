import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import os


class TestCog(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    test = SlashCommandGroup("testing", "various tests")

    @test.command()
    async def testing(self, ctx: discord.ApplicationContext):
        await ctx.respond('Testing!')

    # @test.command()
    # async def mgmt(self, ctx):
    #     await ctx.send('Subcommand not found')



def setup(bot):
    bot.add_cog(TestCog(bot))
