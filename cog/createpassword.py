import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import random


class Password(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="createpassword", description="Erstelle ein sicheres Passwort!")
    @discord.option("länge", int, description="Bitte wähle eine Passwort-Länge! (mind. 8 - max 12)", required=True)
    async def createpassword(self,ctx, länge: int):
        if länge >= 13: # Maximale Passwort-Länge +1
            await ctx.respond("Das Passwort darf nicht länger als 128 Zeichen sein!", ephemeral=True)
            return
        if länge <= 7: # Mindest Passwort-Länge -1
            await ctx.respond("Das Passwort darf nicht kürzer als 8 Zeichen sein!", ephemeral=True)
            return

        chars = 'abcdefghijklmnpqstuvxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"§$%&/()=?@'
        password = ''.join(random.choice(chars) for _ in range(länge))
        await ctx.respond(f"Dein Passwort lautet: ||{password}||", ephemeral=True)


def setup(bot):
    bot.add_cog(Password(bot))