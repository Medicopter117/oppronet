import discord
from discord.ext import commands
from discord import slash_command, Option
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('channels_id_newslog.db')
    return conn

class news1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Sende News")
    @commands.has_permissions(administrator=True)
    async def news(
        self,
        ctx,
        title: Option(str, "hier kommt der Title hin"),
        text: Option(str, "Hier kommt die Beschreibung hin"),
        channel: Option(discord.TextChannel, "Hier kommt der Channel hin")):

        embed = discord.Embed(
            title=f"{title}",
            color=discord.Color.red()
        )
        embed.set_author(name="OPPRO.NET GmbH")
        embed.add_field(name="", value=f"{text}", inline=False)
        embed.add_field(name="Links:", value="[Invite](https://discord.com/oauth2/authorize?client_id=1248265007381348403&permissions=8&integration_type=0&scope=bot) | [Support Server](https://discord.gg/3rbVWaRTpD)")
        embed.set_footer(text="Created by Oppro.net Development")

        await channel.send(embed=embed)

        embed = discord.Embed(
            title=f"News wurden erstellt für {title}",
            color=discord.Color.green()
        )
        embed.set_author(name="OPPRO.NET GmbH")
        embed.add_field(name="mit dem Inhalt:", value=f"{text}", inline=False)
        embed.add_field(name="Links:", value="[Invite](https://discord.com/oauth2/authorize?client_id=1248265007381348403&permissions=8&integration_type=0&scope=bot) | [Support Server](https://discord.gg/3rbVWaRTpD)")
        embed.set_footer(text="Created by Oppro.net Development")

        await ctx.respond(embed=embed, ephemeral=True)
def setup(bot):
    bot.add_cog(news1(bot))