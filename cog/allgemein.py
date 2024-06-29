import discord
from discord.ext import commands
from discord import slash_command, Option
from discord.commands import SlashCommandGroup

class infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    allgemein = SlashCommandGroup("allgemein")
    @allgemein.command(description="Infomationen")
    async def infos(self, ctx):

        embed = discord.Embed(
            title="Infomationen für den Bot",
            color=discord.Color.red()
        )
        embed.set_author(name="OPPRO.NET GmbH")
        embed.add_field(name="Coder", value="Coder: LennyPegauOfficial und Oppro.net Development")
        embed.add_field(name="Name: OPPRO.NET Manage", value="", inline=False)
        embed.add_field(name="Codes:", value="Admin Tools - from CodingKeks\nucreatepassword - from CodingKeks\nFeedback - From Oppro.net Development\ninfos - From Oppro.net Development\nnews - From Oppro.net Development\nstatus - From Oppro.net Development\ntimeout - From Codingkeks\nuserinfo - from Codingkeks")
        embed.add_field(name="Rechte: ", value="Admin", inline=False)
        embed.set_footer(text="Projekt des Oppro.net Development")
        await ctx.respond(embed=embed, view=Button())

    @allgemein.command(description="Bekomme den Support Server!")
    async def support(self, ctx):

        embed = discord.Embed(
            title="Unser Support Server",
            color=discord.Color.red()
        )
        embed.set_author(name="Oppro.net GmbH")
        embed.add_field(name="Link: https://discord.gg/k38huukRcB", value="")
        embed.set_footer(text="Projekt des Oppro.net Development")
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(infos(bot))

class Button(discord.ui.View):
    @discord.ui.button(label="Links", style=discord.ButtonStyle.primary)
    async def button_callback(self, ctx, interactions):
        embed2 = discord.Embed(
            title="Hier sind die Links",
            color=discord.Color.red()
        )
        embed2.set_author(name="Oppro.net GmbH")
        embed2.add_field(name="Links:", value="https://discord.gg/codingkeks\nhttps://discord.gg/3rbVWaRTpD")
        embed2.set_footer(text="Projekt des Oppro.net Development")

        await interactions.response.send_message(embed=embed2)