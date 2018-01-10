import discord
import datetime
import time
import random
import asyncio
import difflib
import sys
import gc
from discord.ext import commands

class Extensions():
    def __init__(self, bot):
        self.bot = bot

    #context-passing이 제대로 되나 확인할 용도의 명령어
    @commands.group(pass_context=True)
    async def godGame(self, ctx):
        """^~^b"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('No, {0.subcommand_passed} is NOT GOD GAME'.format(ctx))

    @godGame.command(name='Noraneko', aliases=['noraneko', '노라네코', 'ノラと猫と野良猫ハート', '노라와 황녀와 도둑고양이 하트', 'ノラ猫', 'ノラネコ', '노라네코하트', '野良猫ハート', 'ノラネコハート'])
    async def _bot(self):
        """노라네코는 갓겜인가?"""
        await self.bot.say('ノラと猫と野良猫ハート IS GOD GAME')

    @commands.command()
    async def clr(self, ctx, limit:int=20, user:discord.Member=None):
        cnt = 0
        print(ctx)
        if user != None:
            async for message in self.bot.logs_from(ctx.message.channel, limit=500, before=ctx.message):
                if cnt == limit:
                    await self.bot.delete_message(ctx.message)
                    return
                await self.bot.delete_message(message)
                cnt += 1
        else:
            await self.bot.delete_message(ctx.message)

    @commands.command()
    async def say(self, ctx):
        """봇에게 어떤 말을 시킬 수 있다"""
        await self.bot.delete_message(ctx.message)
        await self.bot.say(ctx.message.content)

    @commands.command()
    async def info(self):
        """봇에 대한 정보를 볼 수 있음"""
        memory_usage = round(sum(sys.getsizeof(i) for i in gc.get_objects()) / 1000000, 2)
        total_server = len(self.bot.servers)
        total_text_channel = 0
        total_voice_channel = 0
        for channel in self.bot.get_all_channels():
            if channel.type == discord.ChannelType.text:
                total_text_channel += 1
            elif channel.type == discord.ChannelType.voice:
                total_voice_channel += 1

        msg = discord.Embed(color=7458112, title="RyuhaBot Information")
        msgCon = {
            'Developer': 'Ryuha#7918',
            'Bot ID': '{}'.format(self.bot.user.id),
            'Memory usage': '{} MB'.format(memory_usage),
            'Connection status': '{0} servers,\n{1} text channels,\n{2} voice channels'.format(total_server,
                                                                                               total_text_channel,
                                                                                               total_voice_channel)
        }
        msgConlist = msgCon.keys()
        for i in msgConlist:
            msg.add_field(name=i, value=msgCon[i], inline=False)
        await self.bot.say(embed=msg)

    @commands.command()
    async def choose(self, *choices: str):
        """여러가지 선택지 중 하나를 선택함"""
        await self.bot.say(random.choice(choices))


def setup(bot):
    bot.add_cog(Extensions(bot))