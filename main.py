from common_vars import *
from imports import *

import modules.general
import modules.economy
import modules.events
import modules.eh
import modules.botowner
from typing import Union, Any

# temporary command
@bot.command(name='id')
async def _id(ctx, thing: Union[guilded.ChatChannel, guilded.User, Any]):
    try:
        await ctx.send(thing.id)
    except:
        pass
    
@bot.command()
async def test(ctx, *, s):
    await ctx.send(s)

bot.load_extension('jishaku')
bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
