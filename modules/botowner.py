from common_vars import *
import imports

# shiki - i'm not entirely sure if this should be here, but i think it should
from modules.events import *
from contextlib import suppress
from traceback import format_exc


owners = ["AnbjoWYA", "dxDY9JEd"]


@bot.command(name="eval", hidden=True)
async def _eval(self, ctx, *, code='"bruh wat to eval"'):
    if ctx.author.id not in owners:
        return
    with suppress(Exception):
        await ctx.send(eval(code))
        return await ctx.message.add_reaction("✅")
    await ctx.send(
        ":x: uh oh. there's an error in your code:\n```\n"
        + format_exc()
        + "\n```"
    )


@bot.command(name="exec", hidden=True)
async def _exec(self, ctx, *, code='return "???????"'):
    if ctx.author.id not in owners:
        return
    with suppress(Exception):
        exec(code, globals(), locals())
        return await ctx.message.add_reaction("✅")
    await ctx.send(
        ":x: uh oh. there's an error in your code:\n```\n"
        + format_exc()
        + "\n```"
    )
