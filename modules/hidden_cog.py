import asyncio
from traceback import format_exception
from typing import Any, Union

from guilded import ChatChannel, User
from guilded.ext import commands

import lib


class Hidden(lib.Cog, hidden=True):
	def __init__(self, bot):
		self.bot = bot
		self.owners = ["AnbjoWYA", "dxDY9JEd", "4WPbEZwd"]

	@commands.command(name="eval")
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

	@commands.command(name="exec")
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

	@commands.command()
	async def myid(self, ctx):
		await ctx.send(ctx.message.author.id)

	@commands.command(name="id")
	async def _id(self, ctx, thing: Union[ChatChannel, User, Any]):
		try:
			await ctx.send(thing.id)
		except Exception:
			pass

	@commands.command()
	async def test(self, ctx, *, s):
		await ctx.send(s)

	@commands.command()
	async def allcmds(self, ctx):
		await ctx.send(str(self.bot.all_commands))

	@commands.command()
	async def allcogs(self, ctx):
		await ctx.send(str(self.bot.cogs))

	@commands.command()
	async def logs(self, ctx):
		with open(ctx.bot.logf, 'r') as f:
			await ctx.send(f"```\n{f.read()}```")

def setup(bot):
	bot.add_cog(Hidden(bot))
