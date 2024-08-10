from discord.commands import SlashCommandGroup
from discord.commands import Option
from discord.ext import commands
import aiosqlite
import traceback
import datetime
import discord


class ModerationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    admin = SlashCommandGroup("admin")
    warn_group = admin.create_subgroup("warn_system")
    ban_group = admin.create_subgroup("ban_system")

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("mod_sys.db") as db:
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS WarnList (
                warn_id INTEGER PRIMARY KEY,
                mod_id INTEGER,
                guild_id INTEGER,
                user_id INTEGER,
                warns INTEGER DEFAULT 0,
                warn_reason TEXT,
                warn_time TEXT
                )
                """
            )

    @admin.command(description="Kicke einen User aus dem Server")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def kick(
            self,
            ctx: discord.ApplicationContext,
            member: Option(discord.Member, "Wähle den User aus, den du kicken willst", required=True),
            reason: Option(str, "Gib einen Grund an, warum du den User kicken willst", required=False,
                           default="Kein Grund angegeben")
    ):
        kick_embed = discord.Embed(
            title=f"`✅` Kick {member.name}#{member.discriminator}",
            description=f"Du hast den User {member.mention} aus dem Server **{ctx.guild.name}** gekickt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        kick_embed.add_field(name="Moderator:", value=f"{ctx.user}", inline=False)
        kick_embed.add_field(name="Grund:", value=f"{reason}", inline=False)
        kick_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        kick_embed.set_thumbnail(url=member.avatar.url)
        kick_embed.set_footer(
            text=f"{self.bot.user.name}#{self.bot.user.discriminator} | Oppro.net Development",
            icon_url=self.bot.user.avatar.url
        )

        try:
            await member.kick(reason=reason)
        except (discord.Forbidden, discord.HTTPException) as error:
            error_embed = discord.Embed(
                title="`⚠️` Error",
                description=f"Es ist ein Fehler aufgetreten.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            error_embed.add_field(name=f"Beim Kicken von {member.mention} ist ein Fehler aufgetreten.",
                                  value=f"Bitte versuche es später erneut.", inline=False)
            error_embed.add_field(name=f"Fehler Code:", value=f"```{error}```", inline=False)
            error_embed.set_author(name=f"{ctx.guild.name}", icon_url=self.bot.user.avatar.url)
            error_embed.set_footer(
                text=f"{self.bot.user.name}#{self.bot.user.discriminator} | Oppro.net Development",
                icon_url=self.bot.user.avatar.url
            )

            traceback.print_exception(error)
            return await ctx.respond(embed=error_embed, ephemeral=True)

        await ctx.respond(embed=kick_embed, ephemeral=False)

    @ban_group.command(description="Banne einen User aus dem Server")
    @discord.default_permissions(ban_members=True)
    @discord.guild_only()
    async def ban(
            self,
            ctx: discord.ApplicationContext,
            member: Option(discord.Member, "Wähle den User aus, den du Bannen willst", required=True),
            reason: Option(str, "Gib einen Grund an, warum du den User Bannen willst", required=False,
                           default="Kein Grund angegeben")
    ):
        ban_embed = discord.Embed(
            title=f"`✅` Ban {member.name}#{member.discriminator}",
            description=f"Du hast den User {member.mention} aus dem Server **{ctx.guild.name}** gebannt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        ban_embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
        ban_embed.add_field(name="Grund:", value=f"{reason}", inline=False)
        ban_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        ban_embed.set_thumbnail(url=member.avatar.url)
        ban_embed.set_footer(
            text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator} | Oppro.net Development",
            icon_url=ctx.bot.user.avatar.url
        )

        try:
            await member.ban(reason=reason)
        except (discord.Forbidden, discord.HTTPException) as e:
            error_embed = discord.Embed(
                title="`⚠️` Error",
                description=f"Es ist ein Fehler aufgetreten.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            error_embed.add_field(name=f"Beim Kicken von {member.mention} ist ein Fehler aufgetreten.",
                                  value=f"Bitte versuche es später erneut.", inline=False)
            error_embed.add_field(name=f"Fehler Code:", value=f"```{e}```", inline=False)
            error_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
            error_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator} | Oppro.net Development",
                                   icon_url=ctx.bot.user.avatar.url)

            traceback.print_exception(e)
            return await ctx.respond(embed=error_embed, ephemeral=True)

        await ctx.respond(embed=ban_embed, ephemeral=False)

    @warn_group.command(description="Warne einen User aus dem Server")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def warn(
            self,
            ctx: discord.ApplicationContext,
            member: Option(discord.Member, "Wähle den User aus, den du warnen willst", required=True),
            reason: Option(
                str,
                "Gib einen Grund an, warum du den User warnen willst",
                required=False, default="Kein Grund angegeben"
            )
    ):
        warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("mod_sys.db") as db:
            await db.execute(
                "INSERT INTO WarnList "
                "(user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)",
                (member.id, ctx.guild.id, 1, reason, ctx.author.id, warn_time),
            )
            await db.commit()

            async with db.execute(
                    "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                    (member.id, ctx.guild.id),
            ) as cursor:
                row = await cursor.fetchone()
                warn_id = row[0]

        warn_user_embed = discord.Embed(
            title="`⚠️` Warn",
            description=f"Du wurdest auf dem Server **{ctx.guild.name}** gewarnt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        warn_user_embed.add_field(name="Moderator:", value=f"```{ctx.author}```", inline=False)
        warn_user_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warn_user_embed.add_field(name="Grund:", value=f"```{reason}```", inline=False)
        warn_user_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        warn_user_embed.set_thumbnail(url=member.avatar.url)
        warn_user_embed.set_footer(
            text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator} | Oppro.net Development",
            icon_url=ctx.bot.user.avatar.url
        )

        warn_embed = discord.Embed(
            title="`✅` Warn",
            description=f"Du hast den User {member.mention} auf dem Server **{ctx.guild.name}** gewarnt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        warn_embed.add_field(name="Moderator:", value=f"```{ctx.author}```", inline=False)
        warn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warn_embed.add_field(name="Grund:", value=f"```{reason}```", inline=False)
        warn_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.user.avatar.url)
        warn_embed.set_thumbnail(url=member.avatar.url)
        warn_embed.set_footer(
            text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator} | Oppro.net Development",
            icon_url=ctx.bot.user.avatar.url
        )

        await member.send(embed=warn_user_embed)
        await ctx.respond(embed=warn_embed, ephemeral=False)

    @warn_group.command(description="Unwarn einen User aus dem Server")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def unwarn(
            self,
            ctx: discord.ApplicationContext,
            member: Option(discord.Member, "Wähle den User aus, den du unwarnen willst", required=True),
            warn_id: Option(int, "Wähle die Warn ID aus, die du zurückziehen willst", required=True),
            reason: Option(
                str,
                "Gib einen Grund an, warum du den User warnen willst",
                required=False, default="Kein Grund angegeben"
            )
    ):
        unwarn_user_embed = discord.Embed(
            title="`🍀` Unwarn",
            description=f"Ein Warn von dir vom Server **{ctx.guild.name}** wurde zurückgezogen.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        unwarn_user_embed.add_field(name="Moderator:", value=f"```{ctx.author}```", inline=False)
        unwarn_user_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarn_user_embed.add_field(name="Grund:", value=f"```{reason}```", inline=False)
        unwarn_user_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
        unwarn_user_embed.set_thumbnail(url=ctx.guild.icon.url)
        unwarn_user_embed.set_footer(
            text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator} | Oppro.net Development",
            icon_url=ctx.bot.user.avatar.url
        )

        unwarn_embed = discord.Embed(
            title=f"`✅` Unwarn",
            description=f"Du hast den {member.mention} aus dem Server **{ctx.guild.name}** unwarned.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        unwarn_embed.add_field(name="Moderator:", value=f"```{ctx.author}```", inline=False)
        unwarn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarn_embed.add_field(name="Grund:", value=f"```{reason}```", inline=False)
        unwarn_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
        unwarn_embed.set_thumbnail(url=member.avatar.url)
        unwarn_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}  | Oppro.net Development",
                                icon_url=ctx.bot.user.avatar.url)

        async with aiosqlite.connect("mod_sys.db") as db:
            await db.execute(
                "DELETE FROM WarnList WHERE user_id = ? AND guild_id = ? AND warn_id = ?",
                (member.id, ctx.guild.id, warn_id)
            )
            await db.commit()

        await member.send(embed=unwarn_user_embed)
        await ctx.respond(embed=unwarn_embed, ephemeral=False)

    @warn_group.command(description="Zeige alle Warns eines Users aus dem Server an")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def warnings(self, ctx: discord.ApplicationContext, member: discord.Member):
        warns_info = []
        async with aiosqlite.connect("mod_sys.db") as db:
            async with db.execute(
                    "SELECT warn_id, mod_id, guild_id, user_id, warns, warn_reason, warn_time "
                    "FROM WarnList WHERE user_id = ? AND guild_id = ?",
                    (member.id, ctx.guild.id)) as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    warn_id, mod_id, guild_id, user_id, warns, warn_reason, warn_time = row
                    warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
                    warns_info.append(
                        f"**Warn-ID:** __{warn_id}__ | "
                        f"**Warn ausgestellt am:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    warns_info.append(f"**Moderator:** <@{mod_id}> | **Mod-ID**: __{mod_id}__\n")
                    warns_info.append(f"**> Grund:**\n```{warn_reason}```")
                    warns_info.append("\n")

        if not warns_info:
            warnings_embed = discord.Embed(
                title="`⚠️` The user has no warns!",
                description=f"User: {member.mention}",
                color=discord.Color.red(),
            )
        else:
            warnings_embed = discord.Embed(
                title=f"`⚠️` Warn Liste {member.name}#{member.discriminator}",
                description=f"__**Liste der Warns**__",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
        warnings_embed.add_field(name="", value="".join(warns_info), inline=False)
        warnings_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)
        warnings_embed.set_thumbnail(url=member.avatar.url)
        warnings_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}  | Oppro.net Development",
                                  icon_url=ctx.bot.user.avatar.url)

        await ctx.respond(embed=warnings_embed, ephemeral=False)

    @admin.command(description="Lösche Nachrichten aus dem Channel")
    @commands.has_permissions(administrator=True)
    async def purge(
            self,
            ctx: discord.ApplicationContext,
            amount: Option(int, "Anzahl an Nachrichten (min. 1 | max. 100)", required=True)
    ):
        if amount > 101:
            error_embed = discord.Embed(
                title="`❌` Fehler!",
                description="`Ich kann nicht mehr als 100 Nachrichten Löschen!`",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            error_embed.set_thumbnail(url=ctx.guild.icon.url)
            error_embed.set_footer(text=f"| {ctx.bot.user.name}#{ctx.bot.user.discriminator}",
                                   icon_url=ctx.bot.user.avatar.url)
            error_embed.set_author(
                name=f"Purge | Moderation System | Oppro.net Development",
                icon_url=ctx.bot.user.avatar.url
            )

            return await ctx.respond(embed=error_embed, delete_after=6, ephemeral=True)

        deleted = await ctx.channel.purge(limit=amount)

        success_embed = discord.Embed(
            title="`✅` Erfolgreich!",
            description="**{}** `Nachrichten gelöscht!`".format(len(deleted)),
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        success_embed.set_thumbnail(url=ctx.guild.icon.url)
        success_embed.set_footer(
            text=f"| {ctx.bot.user.name}#{ctx.bot.user.discriminator}",
            icon_url=ctx.bot.user.avatar.url
        )
        success_embed.set_author(
            name=f"Purge | Moderation System | Oppro.net Development",
            icon_url=ctx.bot.user.avatar.url
        )

        await ctx.respond(embed=success_embed, delete_after=3, ephemeral=True)


def setup(bot):
    bot.add_cog(ModerationSystem(bot))
