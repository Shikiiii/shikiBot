import os
import sys
from traceback import format_exc

from guilded.ext.commands import Bot

from db import Database
from logcfg import gLogr, name

logger = gLogr("shiki")


class ShikiBot(Bot):
	db = Database()
	logf = name
	ver = "v0.0.1"

	async def on_message(msg):
		pass

	async def on_command_error(ctx, error):
		msg = f"Ignoring exception in command {ctx.command}:\n"
		msg += format_exc(type(error), error, None, file=sys.stderr)
		logger.error(msg)

	async def on_ready():
		logger.info("all cogs have been loaded")
		logger.debug(str(bot.all_commands))


bot = ShikiBot(command_prefix="s!", owner_ids=["AnbjoWYA", "dxDY9JEd"], help_command=None)

bot.load_extension("gishaku")
bot.load_extension("modules.economy")
bot.load_extension("modules.errhdl")
bot.load_extension("modules.events")
bot.load_extension("modules.general")
bot.load_extension("modules.hidden_cog")
bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
