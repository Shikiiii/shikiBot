from common_vars import (
    convert_time,
    editsnipe_channels,
    editsnipe_messages,
    snipe_channels,
    snipe_messages,
)
from imports import commands, guilded


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        snipe_messages[f"{msg.channel.id}"] = [
            f"{msg.author.id}",
            f"{msg.content}",
            f"{msg.created_at}",
        ]
        snipe_channels.append(msg.channel.id)

    @commands.Cog.listener()
    async def on_message_edit(self, old, new):
        editsnipe_messages[f"{new.channel.id}"] = [
            f"{new.author.id}",
            f"{old.content}",
            f"{new.edited_at}",
        ]
        editsnipe_channels.append(new.channel.id)

    @commands.command()
    async def snipe(self, ctx):
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

    @commands.command()
    async def editsnipe(self, ctx):
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
            await ctx.send(
                "There's no edited messages to snipe... (yet :thinking_face:)"
            )

    @commands.command(aliases=["av", "pfp"])
    async def avatar(self, ctx, member: guilded.Member = None):
        member = member or ctx.author
        embed = guilded.Embed(title=f"pfp of {member.name} ☁️", color=0x000000)
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
        # check if user wants help for global cog
        if query.lower() == "global":
            em = guilded.Embed(title="Command list (global)", color=0x0000FF)
            for cmd in bot.walk_commands():
                em.add_field(name=cmd.name, value=cmd.short_doc or "<no help>")
            return await ctx.send(embed=em)
        # check if user wants help for a cog
        for cog_name, cog in bot.cogs.items():
            if cog_name.lower() == query.lower():
                em = guilded.Embed(
                    title="Command list",
                    description=f"wd: `/{cog.qualified_name}`",
                )
                for cmd in cog.walk_commands():
                    if any(cmd.parents) or " " in cmd.qualified_name:
                        continue
                    em.add_field(name=cmd.name, value=cmd.short_doc or "<no help>")
                return await ctx.send(embed=em)
        # show help for command
        if query:
            cmd = await bot.get_command(query, i=ctx.message)
            if not cmd or cmd.hidden:
                return await ctx.send("help: :mag: Command not found.")
            em = guilded.Embed(
                title=cmd.name,
                description=cmd.description or "<no description>",
                color=0x0000FF,
            )
            usage = pre + cmd.qualified_name + " "
            for val in cmd.clean_params.values():
                usage += f"<{val.name}>" if val.default else f"<[{val.name}]> "
            em.add_field(name="Objective", value=cmd.help)
            em.add_field(name="Usage", value=usage)
            em.add_field(
                name="Cog",
                value="<global>" if not cmd.cog else cmd.cog.qualified_name,
            )
            if cmd.aliases:
                em.add_field(
                    name="Aliases",
                    value=", ".join(cmd.aliases),
                )
            if hasattr(cmd, "commands") and any(cmd.commands):
                # it is a group
                em.add_field(
                    name="Sub-Commands",
                    value="".join(
                        [
                            f"`{pre}{cmd.qualified_name}`: {cmd.short_doc}\n"
                            for cmd in cmd.commands
                        ]
                    ),
                )
            await ctx.send(embed=em)
            return
        # no command name supplied, list all cogs
        em = guilded.Embed(title="Cogs list (Not Commands!)")
        for cog in bot.cogs.values():
            em.add_field(
                name=cog.qualified_name,
                value=cog.description or "<no description>",
            )
            em.set_footer(
                text="These are not commands, but groups of commands. `/help core` and stuff"
            )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(General(bot))
