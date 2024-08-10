from discord.commands import slash_command, Option
from discord.ext import commands
from datetime import timedelta
import discord


class Timeout(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @slash_command(description="Timeoute einen Member")
    @discord.default_permissions(moderate_members=True)
    async def timeout(
            self,
            ctx: discord.ApplicationContext,
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
        match reason:
            case "Extremes Chatverhalten | Mute - 2 Stunden":
                duration = timedelta(hours=2)
            case "Extreme Beleidigungen | Mute - 1 Woche":
                duration = timedelta(weeks=1)
            case "Missachtung von Team Anweisungen | Mute - 1 Tag":
                duration = timedelta(days=1)
            case "Sensible Themen | Mute - 4 Tage":
                duration = timedelta(days=4)
            case "Extreme Provokation | Mute 1 Woche":
                duration = timedelta(weeks=1)
            case "Support-Missbrauch | Mute - 1 Tag":
                duration = timedelta(days=1)
            case _:
                return discord.Embed(
                    title="✅ | User wurde erfolgreich getimeoutet",
                    description=f"",
                    color=discord.Color.green()
                )

        try:
            await member.timeout_for(duration, reason=reason)
            embed = discord.Embed(
                title="✅ | User wurde erfolgreich getimeoutet",
                description=f"Der Member {member.mention} wurde  getimeoutet\n"
                            f"\nGrund: {reason}",
                color=discord.Color.green()
            )
        except (AttributeError, discord.Forbidden):
            return await ctx.respond(
                embed=discord.Embed(
                    title="⛔ | Fehler beim muten",
                    description="Ich habe entweder keine Berechtigung, "
                                "um diesen Member zu muten oder dieser User ist nicht Teil dieses Servers",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )

        await ctx.respond(embed=embed)

    @slash_command(description="Entferne einen Timeout")
    @discord.default_permissions(moderate_members=True)
    async def remove_timeout(
            self, ctx,
            member: Option(discord.Member, "Wähle einen Member"),
    ):
        try:
            await member.Timeout(None)
            embed = discord.Embed(
                title="✅ | User wurde erfolgreich entmuted",
                description=f"Der Member {member.mention} wurde entmuted",
                color=discord.Color.green()
            )
        except discord.Forbidden:
            return await ctx.respond(
                embed=discord.Embed(
                    title="⛔ | Fehler beim entmuten",
                    description="Ich habe keine Berechtigung, um diesen Member zu entmuten",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Timeout(bot))
