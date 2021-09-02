from imports import commands, guilded, asyncio
from traceback import format_exception

class Hidden(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owners = ["AnbjoWYA", "dxDY9JEd", "4WPbEZwd"]
		
    @commands.command(name="eval", hidden=True)
    async def _eval(self, ctx, *, code='"bruh wat to eval"'):
        if ctx.author.id not in self.owners:
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

    @commands.command(name="exec", hidden=True)
    async def _exec(self, ctx, *, code='await ctx.send("????")'):
        if ctx.author.id not in self.owners:
            return
        try:
            realcode = (
                "ctx,bot,loop=ctx,bot,loop\n"
                + "async def _e():\n"
                + "  global ctx,bot,loop\n"
            )
            realcode += "".join([f"  {line}\n" for line in code.split("\n")])
            realcode += "\nlocals()['loop'].create_task(_e(), name='_exec')"
            ctx = ctx
            bot = ctx.bot
            loop = bot.loop
            scopes = globals()
            scopes.update(locals())
            exec(realcode, scopes, scopes)
            for task in asyncio.all_tasks(loop):
                if task.get_name() == "_exec":
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
			
	@commands.command(hidden=True)
	async def myid(ctx):
		await ctx.send(ctx.message.author.id)

	@commands.command(name="id", hidden=True)
	async def _id(ctx, thing: Union[guilded.ChatChannel, guilded.User, Any]):
		try:
			await ctx.send(thing.id)
		except Exception:
			pass

	@commands.command(hidden=True)
	async def test(ctx, *, s):
		await ctx.send(s)

	@commands.command(hidden=True)
	async def allcmds(ctx):
		await ctx.send(str(self.bot.all_commands))

	@commands.command(hidden=True)
	async def allcogs(ctx):
		await ctx.send(str(self.bot.cogs))

def setup(bot):
    bot.add_cog(Hidden(bot))
