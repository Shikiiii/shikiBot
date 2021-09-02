from traceback import format_exception

from imports import asyncio, commands


class BotOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owners = ["AnbjoWYA", "dxDY9JEd", "4WPbEZwd"]

def setup(bot):
    bot.add_cog(BotOwner(bot))
