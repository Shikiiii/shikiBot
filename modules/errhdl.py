import contextlib
import sys
from traceback import format_exc

import guilded
import lib
from guilded.ext import commands


class HaltInvoke(Exception):
	"""Halt command invoke instantly."""
	pass


class ToGlobalErrhdl(Exception):
	"""Pass errhdl to global error handler."""
	def __init__(self, err):
		self.original = err


class Errhdl(lib.Cog, hidden=True):
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		"""General global error handler."""
		bot = self.bot
		if isinstance(error, ToGlobalErrhdl):
			error = error.original
		else:
			# prevents any cmds with local hdl being hdl'd here
			if hasattr(ctx.command, "on_error"):
				return

			# prevents any cogs with cog_command_error
			if ctx.cog and ctx.cog._get_overridden_method(ctx.cog.cog_command_error):
				return

		if isinstance(error, commands.errors.CommandInvokeError) and isinstance(
			error.original, HaltInvoke
		):
			if error.original.msg:
				await ctx.send(error.original.msg)
			return 0  # well it is totally fine after all

		# This tells the issuer that the command cannot be used in DM
		if isinstance(error, commands.errors.NoPrivateMessage):
			with contextlib.suppress(Exception):
				await ctx.author.send(
					f":x::lock: {ctx.command} cannot be used in Private Messages."
				)
			return 3

		# Anything in ignored will return and prevent anything happening.
		if isinstance(error, commands.errors.CommandNotFound):
			await ctx.send(":interrobang: Welp, I've no idea. Command not found!")
			return 2
		if isinstance(
			error,
			(
				commands.BadArgument,
				commands.MissingRequiredArgument,
				commands.errors.ConversionError,
			),
		):
			return await ctx.invoke(bot.cmd_help, query=ctx.command.qualified_name)

		if isinstance(error, commands.errors.DisabledCommand):
			return await ctx.send(
				embed=guilded.Embed(
					title=f":no_entry: {ctx.command} has been disabled.",
					description=f":x: `{ctx.command.qualified_name}`",
					color=0xFF0000,
				)
			)

		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("Something went wrong :(\nContact bot maintainers.")

		if isinstance(error, commands.errors.NotOwner):
			await ctx.send("No you are not owner bai. UwU")
			return 6

		# All other Errors not returned come here. And we can just print the default TraceBack.
		print(
			f"Ignoring exception in command `{ctx.command.qualified_name}`:\n"
			f"\n```{format_exc(type(error), error, None)}\n```",
			ctx.guild,
		)
		return 1


def setup(bot):
	"""Ext setup."""
	bot.add_cog(Errhdl(bot))
