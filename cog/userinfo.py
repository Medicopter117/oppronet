# ┏━━━━━━┓  ┏━━━━━━┓
# ┃      ┃  ┃      ┃
# ┃      ┃  ┃      ┃
# ┃      ┃  ┣━━━━━━┛
# ┃      ┃  ┃
# ┗━━━━━━┛  ┃



import discord
from discord import slash_command
import ezcord
from ezcord import View
class Userinfo(ezcord.Cog, emoji="<:info:1147664192325812406>"):

    @slash_command(description="Lasse dir Informationen über einen Benutzer auf den Server anzeigen")
    @discord.option("user",discord.Member,description="Wähle den User aus über den die Info sein soll")
    async def user(self,ctx:discord.ApplicationContext, member:discord.Member=None):
        if member is None:
            member = ctx.author
        if member not in ctx.guild.members:
            await ctx.respond("Dieser User ist nicht auf dem Server",ephemeral=True)
            return
        if isinstance(member, discord.Member):  # Überprüfe, ob member ein Mitglied ist
            activities = []
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    txt = f'Spotify: [{activity.artist} - {activity.title}]({activity.track_url})'
                elif isinstance(activity, discord.Game):
                    txt = f'Spielt: {activity.name}'
                elif isinstance(activity, discord.Streaming):
                    txt = f'Streamt: [{activity.twitch_name} - {activity.game}]({activity.url})'
                elif isinstance(activity, discord.CustomActivity):
                    txt = f'Status: {activity.name}'
                else:
                    txt = f'{activity.name}: {activity.details}'
                activities.append(txt)
        rlist = []
        for role in member.roles:
            rlist.append(str(role.mention))
        rlist.reverse()
        embed = discord.Embed(title=f"memberinfo über {member.display_name} <a:exclamination:1250412438281650290>", color=0x5965f2)
        embed.add_field(name="Name:", value=f"{member}")
        embed.add_field(name="Nickname", value=f"{member.nick}" if member.nick else "hat keinen Nickname",inline=True)
        embed.add_field(name="Display Name", value=f"{member.display_name}")
        embed.add_field(name="Farbe", value=f"{member.colour}")
        embed.add_field(name="Erwähnung", value=f"{member.mention}")
        embed.add_field(name='Status:', value=member.status, inline=False)
        embed.add_field(name="Booster", value=f"Ja<t:{int(member.premium_since.timestamp())}:F>" if member.premium_since else "Nein")
        embed.add_field(name="Höchste Rolle", value=f"{member.top_role.mention}")
        embed.add_field(name="Bot:", value=f'{("Ja" if member.bot else "Nein")}')
        embed.add_field(name="Server beigetreten:", value=f"<t:{int(member.joined_at.timestamp())}:F>")
        embed.add_field(name="Discord beigetreten:", value=f"<t:{int(member.created_at.timestamp())}:F>")
        embed.add_field(name=f"Rollen: {len(member.roles) - 1}", value=','.join(rlist),inline=False)
        embed.add_field(name="Timeout?",value=f"ja" if member.timed_out else "nein")
        embed.set_footer(text="OPPRO.NET | created by Lucky 👑")
        banner_user = await self.bot.fetch_user(member.id)
        try:
            embed.set_image(url=banner_user.banner.url)
        except AttributeError:
            pass
        if activities:
            embed.add_field(name='Aktivitäten', inline=False, value='\n'.join(activities))
        embed.set_author(name=f"{member}", icon_url=f"{member.display_avatar}")
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=f'Angefragt von {ctx.user.name} • {ctx.user.id}', icon_url=ctx.user.display_avatar)
        await ctx.respond(embed=embed,view=Userbutton(self,ctx,member,ctx.user))


def setup(bot: discord.Bot):
    bot.add_cog(Userinfo(bot))

class Userbutton(View):
    def __init__(self,bot,ctx,member,user) -> None:
        self.bot = bot
        self.ctx = ctx
        self.member = member
        self.user = user
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🔰 Home", style=discord.ButtonStyle.green, custom_id="info")
    async def info(self, button,ctx: discord.Interaction):
        if self.member is None:
            self.member = self.ctx.author
        if isinstance(self.member, discord.Member):
            activities = []
            for activity in self.member.activities:
                if isinstance(activity, discord.Spotify):
                    txt = f'Spotify: [{activity.artist} - {activity.title}]({activity.track_url})'
                elif isinstance(activity, discord.Game):
                    txt = f'Spielt: {activity.name}'
                elif isinstance(activity, discord.Streaming):
                    txt = f'Streamt: [{activity.twitch_name} - {activity.game}]({activity.url})'
                elif isinstance(activity, discord.CustomActivity):
                    txt = f'Status: {activity.name}'
                else:
                    txt = f'{activity.name}: {activity.details}'
                activities.append(txt)
        rlist = []
        for role in self.member.roles:
            rlist.append(str(role.mention))
        rlist.reverse()
        embed = discord.Embed(title=f"Memberinfo über {self.member.display_name}", color=0x5965f2)
        embed.add_field(name="Name:", value=f"{self.member}")
        embed.add_field(name="Nickname", value=f"{self.member.nick}" if self.member.nick else "hat keinen Nickname",inline=True)
        embed.add_field(name="Display Name", value=f"{self.member.display_name}")
        embed.add_field(name="Farbe", value=f"{self.member.colour}")
        embed.add_field(name="Erwähnung", value=f"{self.member.mention}")
        embed.add_field(name='Status:', value=self.member.status, inline=False)
        embed.add_field(name="Booster", value=f"Ja<t:{int(self.member.premium_since.timestamp())}:F>" if self.member.premium_since else "Nein")
        embed.add_field(name="Höchste Rolle", value=f"{self.member.top_role.mention}")
        embed.add_field(name="Bot:", value=f'{("Ja" if self.member.bot else "Nein")}')
        embed.add_field(name="Server beigetreten:", value=f"<t:{int(self.member.joined_at.timestamp())}:F>")
        embed.add_field(name="<:Discord:1239890198674800671>  Discord beigetreten:", value=f"<t:{int(self.member.created_at.timestamp())}:F>")
        embed.add_field(name=f"Rollen: {len(self.member.roles) - 1}", value=','.join(rlist),inline=False)
        embed.add_field(name="Timeout?",value=f"ja" if self.member.timed_out else "nein")
        banner_user = await ctx.client.fetch_user(self.member.id)
        try:
            embed.set_image(url=banner_user.banner.url)
        except AttributeError:
            pass
        if activities:
            embed.add_field(name='Aktivitäten', inline=False, value='\n'.join(activities))
        embed.set_thumbnail(url=self.member.display_avatar)
        await ctx.response.edit_message(embed=embed)

    
    @discord.ui.button(label="Avatar", style=discord.ButtonStyle.gray, custom_id="avatar")
    async def avatar(self, button,ctx: discord.ApplicationContext):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Du hast den Command nicht ausgeführt",ephemeral=True)
        embed = discord.Embed(title="Avatar von {}".format(self.member.display_name))
        embed.set_image(url=self.member.display_avatar)
        await ctx.response.edit_message(embed=embed)
    
    @discord.ui.button(label="Banner", style=discord.ButtonStyle.blurple, custom_id="banner")
    async def banner(self, button,ctx: discord.Interaction):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Du hast den Command nicht ausgeführt",ephemeral=True)
        
        embed = discord.Embed(title="Banner von {}".format(self.member.display_name))
        if self.member.bot:
            embed.add_field(name=" ",value="Bots haben keinen Banner")
            return await ctx.response.edit_message(embed=embed)
        banner_user = await ctx.client.fetch_user(self.member.id)
        try:
            embed.set_image(url=banner_user.banner.url)
        except AttributeError:
            embed.add_field(name=" ",value="Dieser User hat keinen Banner")
        await ctx.response.edit_message(embed=embed)

    @discord.ui.button(label="Berechtigungen", style=discord.ButtonStyle.red, custom_id="berechtigungen")
    async def berechtigungen(self, button,ctx: discord.ApplicationContext):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Du hast den Command nicht ausgeführt",ephemeral=True)
        
        embed = discord.Embed(title="Berechtigungen von {}".format(self.member.display_name))
        embed.add_field(name="Berechtigungen",value=",".join([str(perm[0]) for perm in self.member.guild_permissions if perm[1]]))
        await ctx.response.edit_message(embed=embed)


    @discord.ui.button(label="Rollen", style=discord.ButtonStyle.blurple, custom_id="Rollen")
    async def rollen(self, button,ctx: discord.ApplicationContext):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Du hast den Command nicht ausgeführt",ephemeral=True)
        rlist = []
        for role in self.member.roles:
            if role.name == "@everyone":
                continue
            rlist.append(str(role.mention))
        embed = discord.Embed(title="Rollen von {}".format(self.member.display_name))
        if len(rlist) == 0:
            embed.add_field(name="Rollen",value="Dieser User hat keine Rollen")
            return await ctx.response.edit_message(embed=embed)
        embed.add_field(name=f"Rollen: {len(self.member.roles) - 1}", value=','.join(rlist),inline=False)

        await ctx.response.edit_message(embed=embed)