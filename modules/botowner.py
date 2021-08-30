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
        code = "async def exec_():\n"
        code += "\n".join([f"    {line}" for line in code.splitlines()])
        code += "ctx.bot.loop.create_task(exec_(), '_exec')"
        exec(code, globals(), locals())
        for task in asyncio.all_tasks(ctx.bot.loop):
            if task.get_name() == '_exec':
                asyncio.wait_for(task)
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
