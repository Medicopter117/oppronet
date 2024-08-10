from discord import slash_command, Option
from discord.ext import commands
import discord


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="status",
        description="Setze den Status des Bots",
        options=[
            Option(
                str, name="typ",
                description="Der Typ des Status",
                choices=["playing", "stream", "custom", "listening", "watching"]
            ),
            Option(
                str,
                name="name",
                description="Der Name des Spiels, Streams oder des benutzerdefinierten Status"
            ),
            Option(
                str,
                name="status",
                description="Der Status des Bots", choices=["online", "dnd", "idle", "offline"],
                required=False
            )
        ]
    )
    async def status(self, ctx: discord.ApplicationContext, typ: str, name: str, status: str = "online"):
        if typ in ("playing", "custom", "listening", "watching"):
            act = discord.Activity(type=getattr(discord.ActivityType, typ), name=name)
        elif typ == "stream":
            act = discord.Streaming(name=name, url="https://www.twitch.tv/lennypegauofficial")
        else:
            return await ctx.respond("Ungültiger Typ angegeben.")

        if status not in ("online", "dnd", "idle", "offline"):
            return await ctx.respond("Ungültiger Status angegeben.")

        bot_status = getattr(discord.Status, status)

        await self.bot.change_presence(activity=act, status=bot_status)

        embed = discord.Embed(
            title="Erfolgreich den Status ge#ndert",
            color=discord.Color.green()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Der Status wurde Erfolgreich geändert zu", value=f"{status}", inline=False)
        embed.add_field(name="mit den Namen: ", value=f"{name}", inline=False)
        embed.add_field(name="Mit den Typ:", value=f"{typ}", inline=False)
        embed.set_footer(text="OPPRO.NET | Created by LennyPegauOfficial | Projekt des Oppro.net Development")

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
