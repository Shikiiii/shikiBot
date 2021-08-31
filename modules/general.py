from common_vars import *
from imports import *
# shiki - not sure if this should be here but i think it should be
#from modules.events import *

@bot.command()
async def snipe(ctx):
	if ctx.message.channel.id in snipe_channels:
		things = snipe_messages.get(f"{ctx.message.channel.id}")
		embed = guilded.Embed(description=f"{things[1]}", color=0xFFFFFF)
		user = ctx.team.get_member(things[0])
		embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
		time = things[2]
		time_final = convert_time(time[11:-5])
		embed.set_footer(text=f"{time_final}")
		await ctx.send(embed=embed)
	else:
		await ctx.send("There's nothing to snipe... (yet :thinking_face:)")

@bot.command()
async def editsnipe(ctx):
	if ctx.message.channel.id in editsnipe_channels:
		things = editsnipe_messages.get(f"{ctx.message.channel.id}")
		embed = guilded.Embed(description=f"{things[1]}", color=0xFFFFFF)
		user = ctx.team.get_member(things[0])
		embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
		time = things[2]
		time_final = convert_time(time[11:-5])
		embed.set_footer(text=f"{time_final}")
		await ctx.send(embed=embed)
	else:
		await ctx.send("There's no edited messages to snipe... (yet :thinking_face:)")

async def avatar(ctx, user):
	conv = commands.converters.MemberConverter()
	try:
		member = await conv.convert(ctx, user)
	except:
		await ctx.send(f"<@{ctx.message.author.id}>, member not found. :(\nTry out our `s!help` command if you're stuck.")
		return
	embed = guilded.Embed(title=f"pfp of {member.name} ☁️", color=0x000000)
	avatar_url = str(member.avatar_url)
	embed.set_image(url=avatar_url.replace('Large', 'Medium'))
	embed.set_footer(text=f"req by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
	await ctx.send(embed=embed)
