import guilded
from guilded.ext import commands


class Cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.owners = ["AnbjoWYA", "dxDY9JEd", "4WPbEZwd"]
		if self.hidden:
			for cmd in self.walk_commands():
				cmd.hidden = True

	def __init_subclass__(cls, hidden: bool = False):
		cls.hidden = hidden
