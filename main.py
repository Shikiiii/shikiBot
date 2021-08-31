from common_vars import *
from imports import *

import modules.general
import modules.economy
import modules.events
import modules.eh
import modules.botowner

# temporary command
@bot.command()
async def myid(ctx):
    await ctx.send(ctx.message.author.id)
    
@bot.command()
async def test(ctx, *, s):
    await ctx.send(s)

bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
