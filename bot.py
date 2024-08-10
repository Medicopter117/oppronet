from discord.ext import commands
from colorama import Fore
import discord

__all__ = (
    "Bot",
)


class Bot(commands.Bot):
    def __init__(self, /, **kwargs):
        intents = kwargs.get("intents", None)
        if not intents:
            intents = discord.Intents.default()
            intents.members = True

        super().__init__("")

    async def on_ready(self):
        print(f'Bot ist bereit. Eingeloggt als {self.user.name}.')

        print(Fore.LIGHTRED_EX + "OPPRO.NET#0000")
        print(Fore.LIGHTBLUE_EX + "OPPRO.NET#0000")
        print(Fore.LIGHTWHITE_EX + "OPPRO.NET#0000")
        print(Fore.LIGHTYELLOW_EX + "OPPRO.NET#0000")
        print(Fore.LIGHTMAGENTA_EX + "OPPRO.NET Development")
        print(Fore.LIGHTCYAN_EX + "This Setup has been created by LennyPegauOfficial")
        print(Fore.LIGHTGREEN_EX + "Standardfarbe ist jetzt Grün")
