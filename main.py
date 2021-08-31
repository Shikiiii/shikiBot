from common_vars import *
from imports import *

@bot.event
async def on_command_error(ctx, error):
	print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
	traceback.print_exception(type(error), error, None, file=sys.stderr)

@bot.command()
async def myid(ctx):
	await ctx.send(ctx.message.author.id)
    
@bot.command()
async def test(ctx, *, s):
	await ctx.send(s)

bot.load_extension('modules.general')
bot.load_extension('modules.economy')
bot.load_extension('modules.botowner')
bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
