import asyncio
import discord
import logging
import random
import re
from colour import Color
from discord import utils

log = logging.getLogger('LOG')

def getColor(incolor):
    if len(incolor.split(',')) == 3:
        try:
            incolor = incolor.strip("()").split(',')
            if float(incolor[0]) > 1.0 or float(incolor[1]) > 1.0 or float(incolor[2]) > 1.0:
                red = float(int(incolor[0]) / 255)
                blue = float(int(incolor[1]) / 255)
                green = float(int(incolor[2]) / 255)
            else:
                red = incolor[0]
                blue = incolor[1]
                green = incolor[2]
            outcolor = Color(rgb=(float(red), float(green), float(blue)))
        except:
            outcolor = None
    else:
        try:
            outcolor = Color(incolor)
        except:
            outcolor = None

        if outcolor is None:
            try:
                outcolor = Color('#' + incolor)
            except:
                outcolor = None

        if outcolor is None:
            try:
                outcolor = Color('#' + incolor[2:])
            except:
                outcolor = None
    return outcolor

async def edit(ctx, content=None, embed=None, ttl=None):
    perms = ctx.channel.permissions_for(ctx.me).embed_links
    ttl = None if ctx.message.content.endswith(' stay') else ttl
    try:
        if ttl and perms:
            await ctx.message.edit(content=content, embed=embed)
            await asyncio.sleep(ttl)
            try:
                await ctx.message.delete()
            except:
                log.error('Failed to delete Message in {}, #{}'.format(ctx.guild.name, ctx.channel.name))
                pass
        elif ttl is None and perms:
            await ctx.message.edit(content=content, embed=embed)
        elif embed is None:
            await ctx.message.edit(content=content, embed=embed)
        elif embed and not perms:
            await ctx.message.edit(content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Perms for Embeds', delete_after=5)
    except:
        if embed and not perms:
            await ctx.message.edit(content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Perms for Embeds', delete_after=5)
        else:
            await ctx.send(content=content, embed=embed, delete_after=ttl, file=None)

def permEmbed(message):
    return message.channel.permissions_for(message.author).embed_links

