from common_vars import *
import imports

# shiki - i'm not entirely sure if this should be here, but i think it should
from modules.events import *
from contextlib import suppress
from traceback import format_exception 
import asyncio


owners = ["AnbjoWYA", "dxDY9JEd"]


@bot.command(name="eval", hidden=True)
async def _eval(ctx, *, code='"bruh wat to eval"'):
    if ctx.author.id not in owners:
        return
    try:
        await ctx.send(eval(code))
    except Exception as err:
        print(err.__traceback__)
        await ctx.send(
            ":x: uh oh. there's an error in your code:\n```\n"
            + "".join(format_exception(err.__class__, err, err.__traceback__))
            + "\n```"
        )


@bot.command(name="exec", hidden=True)
async def _exec(ctx, *, code='await ctx.send("????")'):
    if ctx.author.id not in owners:
        return
    try:
        realcode = "async def exec_():\n  global ctx, bot, loop\n"
        realcode += "\n".join([f"  {line}" for line in code.splitlines()])
        realcode += "\nloop.create_task(exec_(), name='_exec')"
        ctx = ctx
        bot = ctx.bot
        loop = bot.loop
        exec(realcode)
        for task in asyncio.all_tasks(loop):
            if task.get_name() == '_exec':
                if not task.cancelled():
                    await asyncio.wait_for(task, timeout=None)
                res = task.result()
                if res:
                    await ctx.send(f"returned: {res}")
                return
        raise Exception("Can't find task... UwU")
    except Exception as err:
        print(err.__traceback__)
        await ctx.send(
            ":x: uh oh. there's an error in your code:\n```\n"
            + "".join(format_exception(err.__class__, err, err.__traceback__))
            + "\n```"
        )
