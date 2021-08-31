from common_vars import (
    commands,
    money,
    claimed_daily,
    push_money,
    register_in_money_db,
    push_daily,
    balance,
    daily,
)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx, user):
        conv = commands.converters.MemberConverter()
        try:
            member = await conv.convert(ctx, user)
        except:
            await ctx.send(
                f"<@{ctx.message.author.id}>, member not found. :(\nTry out our `s!help` command if you're stuck."
            )
            return
        if member.id in money:
            await ctx.send(f"<@{member.id}>'s balance is {money.get(member.id)}$.")
        else:
            await register_in_money_db(member.id)
            await ctx.send(f"<@{member.id}>'s balance is 100$.")

    @commands.command()
    async def daily(self, ctx, user):
        conv = commands.converters.MemberConverter()
        try:
            member = await conv.convert(ctx, user)
        except Exception:
            await ctx.send(
                f"<@{ctx.message.author.id}>, member not found. :(\nTry out our `s!help` command if you're stuck."
            )
            return
        if member.id in money:
            # ...
            if member.id not in claimed_daily:
                money[member.id] += 1000
                push_money()
                if ctx.message.author.id == member.id:
                    await ctx.send(
                        f"<@{ctx.message.author.id}>, you've claimed your daily bonus of 1000$."
                    )
                    claimed_daily.append(member.id)
                else:
                    await ctx.send(
                        f"<@{ctx.message.author.id}>, you've given your daily bonus of 1000$ to {member.name}. How nice!"
                    )
                    claimed_daily.append(ctx.message.author.id)
                push_daily()
            else:
                await ctx.send(
                    f"<@{ctx.message.author.id}>, it looks like you've already claimed your daily. Try again later!"
                )
        else:
            await register_in_money_db(member.id)
            if member.id not in claimed_daily:
                money[member.id] += 1000
                push_money()
                if ctx.message.author.id == member.id:
                    await ctx.send(
                        f"<@{ctx.message.author.id}>, you've claimed your daily bonus of 1000$."
                    )
                    claimed_daily.append(member.id)
                else:
                    await ctx.send(
                        f"<@{ctx.message.author.id}>, you've given your daily bonus of 1000$ to {member.name}. How nice!"
                    )
                    claimed_daily.append(ctx.message.author.id)
                push_daily()
            else:
                await ctx.send(
                    f"<@{ctx.message.author.id}>, it looks like you've already claimed your daily. Try again later!"
                )

    @commands.Cog.listener()
    async def cog_command_error(self, ctx, error):
        if ctx.message.content.startswith("s!balance"):
            c = ctx.message.content
            if "s!balance" == c or "s!balance " == c:
                await balance(ctx, ctx.message.author.id)
            else:
                await ctx.send(
                    f"<@{ctx.message.author.id}>, member not found. :(\nStuck? Check out `s!help`!"
                )
        elif ctx.message.content.startswith("s!daily"):
            c = ctx.message.content
            if "s!daily" == c or "s!daily " == c:
                await daily(ctx, ctx.message.author.id)
            else:
                await ctx.send(
                    f"<@{ctx.message.author.id}>, member not found. :(\nStuck? Check out `s!help`!"
                )


def setup(bot):
    bot.add_cog(Economy(bot))
