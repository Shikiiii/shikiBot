from imports import commands, os, sys, traceback
from db import Database


class ShikiBot(
	commands.Bot,
	command_prefix="s!",
	owner_ids=["AnbjoWYA", "dxDY9JEd"],
	help_command=None,
):
	db: Database


bot = ShikiBot()


@bot.event
async def on_command_error(ctx, error):
	print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
	traceback.print_exception(type(error), error, None, file=sys.stderr)


@bot.event
async def on_message(msg):
	pass


@bot.event
async def on_ready():
	print("all cogs have been loaded")
	print(str(bot.all_commands))


bot.load_extension("gishaku")
bot.load_extension("modules.events")
bot.load_extension("modules.general")
bot.load_extension("modules.economy")
bot.load_extension("modules.botowner")
bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
