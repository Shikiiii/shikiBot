from common_vars import claimed_daily, get_daily, get_money, money
from imports import commands, guilded, json, urllib


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global claimed_daily
        print("Logged in as " + self.bot.user.name)
        pg = urllib.request.urlopen(get_money())
        b = str(pg.read().decode("utf-8"))
        raw_data = json.loads(b)
        for user, amount in raw_data.items():
            money[str(user)] = int(amount)
        pg = urllib.request.urlopen(get_daily())
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
            # ctx = await bot.get_context(msg)
            # await userinfo(ctx, msg.content.split(" ")[1])
            # return
        elif msg.content.startswith("s!help") and msg.author.id != self.bot.user.id:
            if len(msg.content) < 8:
                embed = guilded.Embed(
                    description="Those are the current modules. Use `s!help [module]` to see a list of commands.\n\n  - `general`\n   > your every-day needs commands.\n  - `fun`\n   > commands to have fun with, by yourself and w other people.\n  - `mod`\n   > moderation commands, for mods.\n  - `economy`\n   > be rich. be cool.",
                    color=0xFFFFFF,
                )
                embed.set_author(name=f"{msg.author.name}")
                embed.set_footer(text="shikiBot | v0.0.1")
                await msg.channel.send(f"<@{msg.author.id}>", embed=embed)
            else:
                module = msg.content[7:]
                if module.lower() == "general":
                    embed = guilded.Embed(
                        description="The commands in `general` are:\n\n`avatar`\n`snipe`\n`editsnipe`\n`userinfo`\n\nDo `s!help [command]` to view more information and usage of a command.",
                        color=0xFFFFFF,
                    )
                    embed.set_author(name=f"{msg.author.name}")
                    embed.set_footer(text="shikiBot | v0.0.1")
                    await msg.channel.send(f"<@{msg.author.id}>", embed=embed)
                elif module.lower() == "economy":
                    embed = guilded.Embed(
                        description="The commands in `economy` are:\n\n`balance`\n\nDo `s!help [command]` to view more information and usage of a command.",
                        color=0xFFFFFF,
                    )
                    embed.set_author(name=f"{msg.author.name}")
                    embed.set_footer(text="shikiBot | v0.0.1")
                    await msg.channel.send(f"<@{msg.author.id}>", embed=embed)
                else:
                    if module.lower() == "avatar":
                        embed = guilded.Embed(
                            title="`avatar`",
                            description="Shows the avatar of the member you pointed to, or your own avatar, if you didn't point at anyone.\n\nUsage: `s!avatar (member)`\nExample: `s!avatar @shiki`\n\nAliases: `av`, `pfp`",
                            color=0xFFFFFF,
                        )
                        embed.set_author(name=f"{msg.author.name}")
                        embed.set_footer(
                            text="shikiBot | v0.0.1 | [] - required, () - optional"
                        )
                        await msg.channel.send(f"<@{msg.author.id}>", embed=embed)
                    elif module.lower() == "snipe":
                        embed = guilded.Embed(
                            title="`snipe`",
                            description="Shows the most recent deleted message in a channel, alongside with who sent it. Time to expose your friends... :flushed:\n\nUsage: `s!snipe`\nExample: Try it out yourself!\n\nAliases: None",
                            color=0xFFFFFF,
                        )
                        embed.set_author(name=f"{msg.author.name}")
                        embed.set_footer(
                            text="shikiBot | v0.0.1 | [] - required, () - optional"
                        )
                        await msg.channel.send(f"<@{msg.author.id}>", embed=embed)
                    elif module.lower() == "editsnipe":
                        embed = guilded.Embed(
                            title="`editsnipe`",
                            description="Shows the most recent edited message in a channel, alongside with who sent it. Time to expose your friends... :flushed:\n\nUsage: `s!editsnipe`\nExample: Try it out yourself!\n\nAliases: None",
                            color=0xFFFFFF,
                        )
                        embed.set_author(name=f"{msg.author.name}")
                        embed.set_footer(
                            text="shikiBot | v0.0.1 | [] - required, () - optional"
                        )
                        await msg.channel.send(f"<@{msg.author.id}>", embed=embed)
                    elif module.lower() == "userinfo":
                        embed = guilded.Embed(
                            title="`userinfo`",
                            description="Shows information about a user, some of which you can't normally access.\n\nUsage: `s!userinfo (user)`\nExample: s!userinfo shiki\n\nAliases: `uf`, `whois`",
                            color=0xFFFFFF,
                        )
                        embed.set_author(name=f"{msg.author.name}")
                        embed.set_footer(
                            text="shikiBot | v0.0.1 | [] - required, () - optional"
                        )
                        await msg.channel.send(f"<@{msg.author.id}>", embed=embed)

                    # economy
                    elif module.lower() == "balance":
                        embed = guilded.Embed(
                            title="`balance`",
                            description="Shows your amount of cash, or another user's amount.\n\nUsage: `s!balance (user)`\nExample: s!balance shiki\n\nAliases: None",
                            color=0xFFFFFF,
                        )
                        embed.set_author(name=f"{msg.author.name}")
                        embed.set_footer(
                            text="shikiBot | v0.0.1 | [] - required, () - optional"
                        )
                        await msg.channel.send(f"<@{msg.author.id}>", embed=embed)

                    else:
                        await msg.channel.send(
                            "That command/module doesn't exist yet. Check out all the cool commands with `s!help`. :sunglasses:"
                        )
            return
        await self.bot.process_commands(msg)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        print(f"Deleted message {msg.content} {msg.author} {msg.created_at}")

    @commands.Cog.listener()
    async def on_message_edit(self, old, new):
        print(f"Edited message {new.content} {new.author} {new.edited_at}")


def setup(bot):
    bot.add_cog(Events(bot))
