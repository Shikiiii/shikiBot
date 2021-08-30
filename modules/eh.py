from common_vars import *
import imports

@bot.event
async def on_command_error(ctx, error):
	if ctx.message.content.startswith("s!av") or ctx.message.content.startswith("s!pfp"):
		c = ctx.message.content
		if ((c == ("s!av")) or (c == ("s!pfp")) or (c == ("s!avatar"))):
			pg = urllib.request.urlopen(f'https://www.guilded.gg/api/users/{ctx.message.author.id}')
			b = str(pg.read().decode('utf-8'))
			user_data = json.loads(b)
			usr_pfp = user_data.get("user").get("profilePicture").replace('Large', 'Medium')
			embed = guilded.Embed(title=f"pfp of {ctx.message.author.name} ☁️", color=0x000000)
			embed.set_image(url=usr_pfp)
			embed.set_footer(text=f"req by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"<@{ctx.message.author.id}>, member not found. :(\nStuck? Check out `s!help`!")
	elif ctx.message.content.startswith("s!balance"):
		c = ctx.message.content
		if "s!balance" == c or "s!balance " == c:
			await balance(ctx, ctx.message.author.id)
		else:
			await ctx.send(f"<@{ctx.message.author.id}>, member not found. :(\nStuck? Check out `s!help`!")
	elif ctx.message.content.startswith("s!daily"):
		c = ctx.message.content
		if "s!daily" == c or "s!daily " == c:
			await daily(ctx, ctx.message.author.id)
		else:
			await ctx.send(f"<@{ctx.message.author.id}>, member not found. :(\nStuck? Check out `s!help`!")
	else:
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, None, file=sys.stderr)
