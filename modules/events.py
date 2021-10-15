import json
import urllib

from guilded.ext import commands


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		global claimed_daily
		print("Logged in as " + self.bot.user.name)
		pg = urllib.request.urlopen(self.bot.db.get_money())
		b = str(pg.read().decode("utf-8"))
		raw_data = json.loads(b)
		for user, amount in raw_data.items():
			self.bot.db.money[str(user)] = int(amount)
		pg = urllib.request.urlopen(self.bot.db.get_daily())
		b = str(pg.read().decode("utf-8"))
		claimed_daily = b.split(" ")
		print(str(self.bot.all_commands))

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.content == "s!ping" and msg.author.id != self.bot.user.id:
			await msg.channel.send("Pong!")
		elif (
			msg.content.startswith("s!userinfo")
			or msg.content.startswith("s!uf")
			or msg.content.startswith("s!whois")
		):
			await msg.channel.send(
				f"<@{msg.author.id}>, that command isn't functioning yet. It may be because of the current API limitations, or it's currently in the works. Whatever it is, it'll be here soon, very soon."
			)
		await self.bot.process_commands(msg)

	@commands.Cog.listener()
	async def on_message_delete(self, msg):
		print(f"Deleted message {msg.content} {msg.author} {msg.created_at}")

	@commands.Cog.listener()
	async def on_message_edit(self, old, new):
		print(f"Edited message {new.content} {new.author} {new.edited_at}")

	@commands.command()
	async def testevents(self, ctx):
		await ctx.send("command exists")


def setup(bot):
	bot.add_cog(Events(bot))
