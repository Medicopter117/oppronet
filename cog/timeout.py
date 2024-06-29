import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from datetime import timedelta


class timeout(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @slash_command(description="Timeoute einen Member")
    @discord.default_permissions(moderate_members=True)
    async def timeout(
            self, ctx,
            member: Option(discord.Member, "Wähle ein Member aus"),

            reason: Option(str, "Wähle ein Grund aus", choices=([
                "Extremes Chatverhalten | Mute - 2 Stunden",
                "Extreme Beleidigungen | Mute - 1 Woche",
                "Missachtung von Team Anweisungen | Mute - 1 Tag",
                "Sensible Themen | Mute - 4 Tage",
                "Extreme Provokation | Mute 1 Woche",
                "Support-Missbrauch | Mute - 1 Tag",
            ]), required=True)
    ):

        if reason == "Extremes Chatverhalten | Mute - 2 Stunden ":
            duration = timedelta(hours=2)

        elif reason == "Extreme Beleidigungen | Mute - 1 Woche":
            duration = timedelta(weeks=1)

        elif reason == "Missachtung von Team Anweisungen | Mute - 1 Tag":
            duration = timedelta(days=1)

        elif reason == "Sensible Themen | Mute - 4 Tage":
            duration = timedelta(days=4)

        elif reason == "Extreme Provokation | Mute 1 Woche":
            duration = timedelta(weeks=1)

        elif reason == "Support-Missbrauch | Mute - 1 Tag":
            duration = timedelta(days=1)

        try:
            await member.timeout_for(duration, reason=reason)
            embed = discord.Embed(
                title="✅ | User wurde erfolgreich getimeoutet",
                description=f"Der Member {member.mention} wurde  getimeoutet\n"
                            f"\nGrund: {reason}",
                color=discord.Color.green()
            )
            em = discord.Embed(
                title="⛔ | Fehler beim muten",
                description="Ich habe keine Berechtigung, um diesen Member zu muten",
                color=discord.Color.red()
            )
        except discord.Forbidden:
            await ctx.respond(embed=em, ephemeral=True)
            return
        await ctx.respond(embed=embed)

    @slash_command(description="Entferne einen Timeout")
    @discord.default_permissions(moderate_members=True)
    async def removetimeout(
            self, ctx,
            member: Option(discord.Member, "Wähle einen Member"),
    ):
        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="✅ | User wurde erfolgreich entmuted",
                description=f"Der Member {member.mention} wurde entmuted",
                color=discord.Color.green()
            )

            em = discord.Embed(
                title="⛔ | Fehler beim entmuten",
                description="Ich habe keine Berechtigung, um diesen Member zu entmuten",
                color=discord.Color.red()
            )

        except discord.Forbidden:
            await ctx.respond(embed=em, ephemeral=True)
            return
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(timeout(bot))