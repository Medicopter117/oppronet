import discord
from discord.ext import commands
from discord import slash_command, Option

class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Bewerte unsere Team Mitglieder")
    async def feedback(
            self,
            ctx,
            nutzer: Option(discord.Member, "Den Member den du Bewerten willst (Nur Teamler!)"),
            sterne: Option(int, "Bewertung in Sternen (1-5)", choices=[1, 2, 3, 4, 5]),
            text: Option(str, "Die Bewertung")
    ):
        # Channel-ID des Feedback-Channels
        feedback_channel_id = 1255631012801675304  # Ersetze dies mit der tatsächlichen Channel-ID

        # Sende die Nachricht in den Feedback-Channel
        feedback_channel = self.bot.get_channel(feedback_channel_id)
        if feedback_channel:
            embed = discord.Embed(
                title=f"Neue Bewertung für den User {nutzer}",
                color=discord.Color.yellow()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.add_field(name="Bewertung von", value=ctx.author.mention, inline=True)
            embed.add_field(name="Für", value=nutzer.mention, inline=True)
            embed.add_field(name="Bewertung", value=text, inline=False)
            embed.add_field(name="Sterne", value="⭐" * sterne, inline=False)
            embed.set_footer(text="OPPRO.NET | LennyPegauOfficial has be created")

            await feedback_channel.send(embed=embed)

        embed = discord.Embed(
            title="Bewertung wurde erfolgreich gesendet",
            color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name= "Deine Bewertung für",value=f"{nutzer} wurde erfolgreich versendet")
        embed.add_field(name=f"mit {sterne} von 5", value="⭐" * sterne, inline=False)
        embed.set_footer(text="OPPRO.NET | LennyPegauOfficial has be created")

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Feedback(bot))