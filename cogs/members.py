import discord
from discord.ext import commands

class Members:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, ctx, *, member: discord.Member):
        """해당 멤버가 언제 접속했는지 알려줌"""
        await ctx.send('{member.display_name} joined on {member.joined_at}')

    @commands.command(name='top_role', aliases=['toprole'])
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """멤버의 역할을 보여주는 명령어"""

        if member is None:
            member = ctx.author

        await ctx.send('The top role for {member.display_name} is {member.top_role.name}')

    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """Member의 Guild Permission을 체크하는 커맨드. Member가 제공되지 않으면 Author를 체크함"""

        if not member:
            member = ctx.author

        # 각각의 권한에 대한 값이 True인지 체크함
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # Embed 로 묶음
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF는 비어있는 field name을 적을 때 씀
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, user=None):
        """유저의 아이콘을 보여주는 명령어. (prefix)avatar (username or space)"""
        if user == None:
            msg = discord.Embed(color=7458112)
            msg.set_image(url=ctx.message.author.avatar_url)
            await self.bot.say(embed=msg)
        elif user.startswith("<@"):
            user = user.replace("<@", "").replace(">", "")
            member = discord.utils.find(lambda m: m.id == user, ctx.message.server.members)
            msg = discord.Embed(color=7458112, title=member.name + "#" + member.discriminator)
            await self.bot.say(embed=msg)
        else:
            member_storage = []
            for member in ctx.message.server.members:
                member_storage.append(member.display_name.lower())
            user = difflib.get_close_matches(user, member_storage, cutoff=0.1)
            member = discord.utils.find(lambda m: m.display_name.lower() == user[0], ctx.message.server.members)
            msg = discord.Embed(color=7458112, title=member.name + "#" + discord.discriminator)
            msg.set_image(url=member.avatar_url)
            await bot.say(embed=msg)


def setup(bot):
    bot.add_cog(Members(bot))