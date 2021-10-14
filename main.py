from imports import commands, os, sys, traceback

bot = commands.Bot(
    command_prefix="s!", owner_ids=["AnbjoWYA", "dxDY9JEd"], help_command=None
)


@bot.event
async def on_command_error(ctx, error):
    print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, None, file=sys.stderr)


@bot.event
async def on_message(msg):
    pass


@bot.event
async def on_ready():
    print("all cogs have been loaded")
    print(str(bot.all_commands))


bot.load_extension("gishaku")
bot.load_extension("modules.economy")
bot.load_extension("modules.errhdl")
bot.load_extension("modules.events")
bot.load_extension("modules.general")
bot.load_extension("modules.hidden_cog")
bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
