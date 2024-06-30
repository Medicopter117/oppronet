import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import os
import asyncio
import re  # regex library
import colorama
from colorama import Fore
from dotenv import load_dotenv
import ezcord
intents = discord.Intents.default()
intents.members = True  # Stelle sicher, dass du die richtigen Intents für mitgliederbezogene Ereignisse hast

bot = discord.Bot(
    intents=intents
)

# Ban-Befehl

bot = commands.Bot(command_prefix="!")  # Beispiel-Prefix, ändern Sie es entsprechend Ihrer Konfiguration

@bot.event
async def on_ready():
    print(f'Bot ist bereit. Eingeloggt als {bot.user}.')
# NOT THIS EDIT

if __name__ == "__main__":
    for filename in os.listdir("cog"):
        if filename.endswith(".py"):
            bot.load_extension(f"cog.{filename[:-3]}")


async def delayed_print(message, delay):
    await asyncio.sleep(delay)
    print(message)
    # delete the is okay :(
async def main():
    await delayed_print(Fore.LIGHTRED_EX + "OPPRO.NET#0000", 0.5)
    await delayed_print(Fore.LIGHTBLUE_EX + "OPPRO.NET#0000", 0.5)
    await delayed_print(Fore.LIGHTWHITE_EX + "OPPRO.NET#0000", 0.5)
    await delayed_print(Fore.LIGHTYELLOW_EX + "OPPRO.NET#0000", 0.5)
    await delayed_print(Fore.LIGHTMAGENTA_EX + "OPPRO.NET Development", 1.5)
    await delayed_print("", 0)  # Leere Zeichenkette, keine Verzögerung
    await delayed_print(Fore.LIGHTCYAN_EX + "This Setup has been created by LennyPegauOfficial", 0.9)
    await delayed_print("", 0)  # Leere Zeichenkette, keine Verzögerung
    await delayed_print(Fore.LIGHTGREEN_EX + "Standardfarbe ist jetzt Grün", 1.0)

if __name__ == "__main__":
    asyncio.run(main())
# Bot System
load_dotenv()
bot.run(os.getenv("TOKEN"))
