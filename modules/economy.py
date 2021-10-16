import guilded
from guilded.ext import commands


class Economy(commands.Cog):
	"""be rich. be cool."""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["bal"])
	async def balance(self, ctx, member: guilded.Member = None):
		"""
		Shows your amount of cash, or another user's amount.

		Example: s!balance @member
		"""
		member = member or ctx.author
		if member.id in self.bot.db.money:
			await ctx.send(f"<@{member.id}>'s balance is {self.bot.db.money.get(member.id)}$.")
		else:
			await self.bot.db.register_in_money_db(member.id)
			await ctx.send(f"<@{member.id}>'s balance is 100$.")

	@commands.command()
	async def daily(self, ctx, member: guilded.Member = None):
		member = member or ctx.author
		if member.id in self.bot.db.money:
			# ...
			if member.id not in self.bot.db.claimed_daily:
				self.bot.db.money[member.id] += 1000
				self.bot.db.push_money()
				if ctx.message.author.id == member.id:
					await ctx.send(
						f"<@{ctx.message.author.id}>, you've claimed your daily bonus of 1000$."
					)
					self.bot.db.claimed_daily.append(member.id)
				else:
					await ctx.send(
						f"<@{ctx.message.author.id}>, you've given your daily bonus of 1000$ to {member.name}. How nice!"
					)
					self.bot.db.claimed_daily.append(ctx.message.author.id)
				self.bot.db.push_daily()
			else:
				await ctx.send(
					f"<@{ctx.message.author.id}>, it looks like you've already claimed your daily. Try again later!"
				)
		else:
			await self.bot.db.register_in_money_db(member.id)
			if member.id not in self.bot.db.claimed_daily:
				self.bot.db.money[member.id] += 1000
				self.bot.db.push_money()
				if ctx.message.author.id == member.id:
					await ctx.send(
						f"<@{ctx.message.author.id}>, you've claimed your daily bonus of 1000$."
					)
					self.bot.db.claimed_daily.append(member.id)
				else:
					await ctx.send(
						f"<@{ctx.message.author.id}>, you've given your daily bonus of 1000$ to {member.name}. How nice!"
					)
					self.bot.db.claimed_daily.append(ctx.message.author.id)
				self.bot.db.push_daily()
			else:
				await ctx.send(
					f"<@{ctx.message.author.id}>, it looks like you've already claimed your daily. Try again later!"
				)


def setup(bot):
	bot.add_cog(Economy(bot))
