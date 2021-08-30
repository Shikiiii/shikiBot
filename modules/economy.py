from common_vars import *
import imports
# shiki - i'm not entirely sure if this should be here, but i think it should
from modules.events import *

@bot.command()
async def balance(ctx, user):
	conv = commands.converters.MemberConverter()
	try:
		member = await conv.convert(ctx, user)
	except:
		await ctx.send(f"<@{ctx.message.author.id}>, member not found. :(\nTry out our `s!help` command if you're stuck.")
		return
	if member.id in money:
		await ctx.send(f"<@{member.id}>'s balance is {money.get(member.id)}$.")
	else:
		await register_in_money_db(member.id)
		await ctx.send(f"<@{member.id}>'s balance is 100$.")

@bot.command()
async def daily(ctx, user):
	conv = commands.converters.MemberConverter()
	try:
		member = await conv.convert(ctx, user)
	except:
		await ctx.send(f"<@{ctx.message.author.id}>, member not found. :(\nTry out our `s!help` command if you're stuck.")
		return
	if member.id in money:
		# ...
		if member.id not in claimed_daily:
			money[member.id] += 1000
			push_money()
			if ctx.message.author.id == member.id:
				await ctx.send(f"<@{ctx.message.author.id}>, you've claimed your daily bonus of 1000$.")
				claimed_daily.append(member.id)
			else:
				await ctx.send(f"<@{ctx.message.author.id}>, you've given your daily bonus of 1000$ to {member.name}. How nice!")
				claimed_daily.append(ctx.message.author.id)
			push_daily()
		else:
			await ctx.send(f"<@{ctx.message.author.id}>, it looks like you've already claimed your daily. Try again later!")
	else:
		await register_in_money_db(member.id)
		if member.id not in claimed_daily:
			money[member.id] += 1000
			push_money()
			if ctx.message.author.id == member.id:
				await ctx.send(f"<@{ctx.message.author.id}>, you've claimed your daily bonus of 1000$.")
				claimed_daily.append(member.id)
			else:
				await ctx.send(f"<@{ctx.message.author.id}>, you've given your daily bonus of 1000$ to {member.name}. How nice!")
				claimed_daily.append(ctx.message.author.id)
			push_daily()
		else:
			await ctx.send(f"<@{ctx.message.author.id}>, it looks like you've already claimed your daily. Try again later!")
