from discord.commands import slash_command
from discord.ext import commands
import discord
import random
import string


class Password(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="create-password", description="Erstelle ein sicheres Passwort!")
    @discord.option("länge", int, description="Bitte wähle eine Passwort-Länge! (mind. 8 - max 12)", required=True)
    async def create_password(self, ctx: discord.ApplicationContext, length: int):
        if length >= 13:
            return await ctx.respond("Das Passwort darf nicht länger als 12 Zeichen sein!", ephemeral=True)

        if length <= 7:
            return await ctx.respond("Das Passwort darf nicht kürzer als 8 Zeichen sein!", ephemeral=True)

        chars: str = string.ascii_letters + string.digits + '!"§$%&/()=?@'
        password: str = ''.join(random.choice(chars) for _ in range(length))

        await ctx.respond(f"Dein Passwort lautet: ||{password}||", ephemeral=True)


def setup(bot):
    bot.add_cog(Password(bot))
