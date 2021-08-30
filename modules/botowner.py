from common_vars import *
import imports

# shiki - i'm not entirely sure if this should be here, but i think it should
from modules.events import *
from contextlib import suppress
from traceback import format_exception 


owners = ["AnbjoWYA", "dxDY9JEd"]


@bot.command(name="eval", hidden=True)
async def _eval(ctx, *, code='"bruh wat to eval"'):
    if ctx.author.id not in owners:
        return
    try:
        await ctx.send(eval(code))
        return await ctx.message.add_reaction("✅")
    except Exception:
        await ctx.send(
            ":x: uh oh. there's an error in your code:\n```\n"
            + format_exception()
            + "\n```"
        )


@bot.command(name="exec", hidden=True)
async def _exec(ctx, *, code='return "???????"'):
    if ctx.author.id not in owners:
        return
    try:
        exec(code, globals(), locals())
        return await ctx.message.add_reaction("✅")
    except Exception:
        await ctx.send(
            ":x: uh oh. there's an error in your code:\n```\n"
            + format_exception()
            + "\n```"
        )
