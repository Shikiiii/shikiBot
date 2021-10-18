from random import choice

from guilded import Embed, Member
from guilded.ext import commands


class General(commands.Cog):
	"""your every-day needs commands."""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_delete(self, msg):
		self.bot.db.snipe_messages[f"{msg.channel.id}"] = [
			f"{msg.author.id}",
			f"{msg.content}",
			f"{msg.created_at}",
		]
		self.bot.db.snipe_channels.append(msg.channel.id)

	@commands.Cog.listener()
	async def on_message_edit(self, old, new):
		self.bot.db.editsnipe_messages[f"{new.channel.id}"] = [
			f"{new.author.id}",
			f"{old.content}",
			f"{new.edited_at}",
		]
		self.bot.db.editsnipe_channels.append(new.channel.id)

	@commands.command()
	async def snipe(self, ctx):
		"""
		Shows the most recent deleted message in a channel, with the author.

		Time to expose your friends... :flushed:
		"""
		if ctx.message.channel.id in self.snipe_channels:
			things = self.snipe_messages.get(f"{ctx.message.channel.id}")
			embed = Embed(description=f"{things[1]}", color=0xFFFFFF)
			user = ctx.team.get_member(things[0])
			embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
			time = things[2]
			time_final = self.convert_time(time[11:-5])
			embed.set_footer(text=f"{time_final}")
			await ctx.send(embed=embed)
		else:
			await ctx.send("There's nothing to snipe... (yet :thinking_face:)")

	@commands.command()
	async def editsnipe(self, ctx):
		"""
		Shows the most recent edited message in a channel, with the author.

		Time to expose your friends... :flushed:
		"""
		if ctx.message.channel.id in self.editsnipe_channels:
			things = self.editsnipe_messages.get(f"{ctx.message.channel.id}")
			embed = Embed(description=f"{things[1]}", color=0xFFFFFF)
			user = ctx.team.get_member(things[0])
			embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
			time = things[2]
			time_final = self.convert_time(time[11:-5])
			embed.set_footer(text=f"{time_final}")
			await ctx.send(embed=embed)
		else:
			await ctx.send(
				"There's no edited messages to snipe... (yet :thinking_face:)"
			)

	@commands.command(aliases=["av", "pfp"])
	async def avatar(self, ctx, member: Member = None):
		"""
		Shows the avatar of the member, by default yourself.

		Example: `s!avatar @member`
		"""
		member = member or ctx.author
		embed = Embed(title=f"pfp of {member.name} ☁️", color=0x000000)
		avatar_url = str(member.avatar_url)
		embed.set_image(url=avatar_url.replace("Large", "Medium"))
		embed.set_footer(
			text=f"req by {ctx.message.author.name}",
			icon_url=ctx.message.author.avatar_url,
		)
		await ctx.send(embed=embed)

	@commands.command(aliases=["?", "cmds", "commands"])
	async def help(self, ctx, *, query: str = ""):
		"""Shows this message"""
		bot = ctx.bot
		pre = ctx.prefix
		addf = lambda e, n, v: e.add_field(name=n, value=v)
		sf = lambda e, s="": e.set_footer(text=f"shikiBot | {bot.ver}" + s)
		hlpf = lambda em, cmd: addf(em, cmd.name, cmd.short_doc or "<no help>")
		# check if user wants help for global cog
		if query.lower() == "global":
			em = Embed(title="Command list (global)", color=0x0000FF)
			for cmd in bot.walk_commands():
				hlpf(em, cmd)
				addf(em, cmd.name, cmd.short_doc or "<no help>")
			return await ctx.send(embed=sf(em))
		# check if user wants help for a cog
		for cog_name, cog in bot.cogs.items():
			if getattr(cog, 'hidden', False):
				continue
			if cog_name.lower() == query.lower():
				em = Embed(
					title=f"Command list ({cog_name})",
					description=f"Do `{pre}help [command]` to view more information and usage of a command.",
				)
				for cmd in cog.walk_commands():
					if not any(cmd.parents) and " " not in cmd.qualified_name:
						hlpf(em, cmd)
				return await ctx.send(embed=sf(em))
		# show help for command
		if query:
			cmd = await bot.get_command(query)
			if not cmd or cmd.hidden:
				return await ctx.send(
					"That command/module doesn't exist yet. "
					f"Check out all the cool commands with `{pre}help`. :sunglasses:"
				)
			em = Embed(
				title=cmd.name,
				description=cmd.description.replace(
					"@member", choice("@windowsboy111", "@shiki")
				)
				if cmd.description
				else "<no description>",
				color=0x0000FF,
			)
			addf(em, "Objective", cmd.help or "<no help>")
			args = " ".join(f"[{val.name}]" if val.default else f"({val.name})" for val in cmd.clean_params.values())
			addf(em, "Usage", f'{pre}{cmd.qualified_name} {args}')
			addf(em, "Cog", cmd.cog.qualified_name if cmd.cog else "<global>")
			if cmd.aliases:
				addf(em, "Aliases", ", ".join(cmd.aliases))
			if getattr(cmd, 'commands', False):
				# it is a group
				addf(
					em,
					"Sub-Commands",
					"\n".join(
						f"`{pre}{cmd.qualified_name}`: {cmd.short_doc}"
						for cmd in cmd.commands
					)
				)
			await ctx.send(embed=sf(em, " | [] - required, () - optional"))
			return
		# no command name supplied, list all cogs
		em = Embed(
			title="Module list (Not Commands!)",
			description="Those are the current modules. "
			f"Use `{pre}help [module]` to see a list of commands.",
		)
		for cog in bot.cogs.values():
			if not getattr(cog, 'hidden', True):
				addf(em, cog.qualified_name, cog.description or "<no description>")
		await ctx.send(embed=sf(em))


def setup(bot):
	bot.add_cog(General(bot))
