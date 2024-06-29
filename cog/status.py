import discord
from discord.ext import commands
from discord import slash_command, Option
from discord import Embed

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="status",
        description="Setze den Status des Bots",
        options=[
            Option(str, name="typ", description="Der Typ des Status", choices=["game", "stream", "custom", "listening", "watching"]),
            Option(str, name="name", description="Der Name des Spiels, Streams oder des benutzerdefinierten Status"),
            Option(str, name="status", description="Der Status des Bots", choices=["online", "dnd   ", "idle", "offline"], required=False)
        ]
    )
    async def status(self, ctx: discord.ApplicationContext, typ: str, name: str, status: str = "online"):
        if typ == "game":
            act = discord.Game(name=name)
        elif typ == "stream":
            act = discord.Streaming(name=name, url="https://www.twitch.tv/lennypegauofficial")
        elif typ == "custom":
            act = discord.Activity(type=discord.ActivityType.custom, name=name)
        elif typ == "listening":
            act = discord.Activity(type=discord.ActivityType.listening, name=name)
        elif typ == "watching":
            act = discord.Activity(type=discord.ActivityType.watching, name=name)
        else:
            await ctx.respond("Ungültiger Typ angegeben.")
            return

        if status == "online":
            bot_status = discord.Status.online
        elif status == "dnd":
            bot_status = discord.Status.dnd
        elif status == "idle":
            bot_status = discord.Status.idle
        elif status == "offline":
            bot_status = discord.Status.offline
        else:
            await ctx.respond("Ungültiger Status angegeben.")
            return

        await self.bot.change_presence(activity=act, status=bot_status)

        embed = discord.Embed (
            title="Erfolgerich den Status geandert",
            color=discord.Color.green()
       )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Der Status wurde Erfolgerich geandert zu", value=f"{status}", inline=False)
        embed.add_field(name="mit den Namen: ", value=f"{name}", inline=False)
        embed.add_field(name="Mit den Typ:", value=f"{typ}", inline=False)
        embed.set_footer(text="OPPRO.NET | Created by LennyPegauOfficial | Projekt des Oppro.net Development")

        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(Status(bot))
