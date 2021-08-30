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

bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
