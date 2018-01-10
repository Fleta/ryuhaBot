import discord
from discord.ext import commands
import time
import datetime


import sys, traceback

def get_prefix(bot, message):
    """봇이 호출가능한 prefix."""
    prefixes = ['>', 'r/', '>?']

    # 우리가 guild 밖에 있는지 확인하기 위함. PM같은 경우
    #if not message.guild:
        # PM에서는 ?만 허용
    #    return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['google']
bot = commands.Bot(command_prefix=get_prefix, description='RyuhaBot Version 0.1')

@bot.event
async def on_command_completion(command, ctx):
    now = datetime.datetime.now()
    if command != None:
        try:
            user_id = ctx.message.author.id
            user_name = ctx.message.author.name + '#' + ctx.message.author.discriminator
            server_id = ctx.message.server.id
            server_name = ctx.message.server.name
            message = ctx.message.content
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print('-----------------------------------------------')
            print("DateTime: {0}\nServer: {1} [{2}]\nUser: {3} [{4}]\nMessage: {5}".format(current_time, server_name, server_id, user_name, user_id, message))
            print('-----------------------------------------------\n')
        except AttributeError:
            user_id = ctx.message.author.id
            user_name = ctx.message.author.name + '#' + ctx.message.author.discriminator
            message = ctx.message.content
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print('-----------------------------------------------')
            print("From DM\nDateTime: {0}\nUser: {1} [{2}]\nMessage: {3}".format(current_time, user_name, user_id, message))
            print('-----------------------------------------------\n')

@bot.event
async def on_command_error(exception, ctx):
    now = datetime.datetime.now()
    try:
        if exception != None:
            user_id = ctx.message.author.id
            user_name = ctx.message.author.name + '#' + ctx.message.author.discriminator
            server_id = ctx.message.server.id
            server_name = ctx.message.server.name
            message = ctx.message.content
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print('******************** Error ********************')
            print("DateTime: {0}\nServer: {1} [{2}]\nUser: {3} [{4}]\nMessage: {5}\nError Message: {6}".format(current_time, server_name, server_id, user_name, user_id, message, exception))
            print('******************** Error ********************\n')
    except AttributeError:
        if exception != None:
            user_id = ctx.message.author.id
            user_name = ctx.message.author.name + '#' + ctx.message.author.discriminator
            message = ctx.message.content
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print('******************** Error ********************')
            print("From DM\nDateTime: {0}\nUser: {1} [{2}]\nMessage: {3}\nError Message: {4}".format(current_time, user_name, user_id, message, exception))
            print('******************** Error ********************\n')

@bot.event
async def on_command_error(exception, ctx):
    now = datetime.datetime.now()
    try:
        if exception != None:
            user_id = ctx.message.author.id
            user_name = ctx.message.author.name + '#' + ctx.message.author.discriminator
            server_id = ctx.message.server.id
            server_name = ctx.message.server.name
            message = ctx.message.content
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print('******************** Error ********************')
            print("DateTime: {0}\nServer: {1} [{2}]\nUser: {3} [{4}]\nMessage: {5}\nError Message: {6}".format(current_time, server_name, server_id, user_name, user_id, message, exception))
            print('******************** Error ********************\n')
    except AttributeError:
        if exception != None:
            user_id = ctx.message.author.id
            user_name = ctx.message.author.name + '#' + ctx.message.author.discriminator
            message = ctx.message.content
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print('******************** Error ********************')
            print("From DM\nDateTime: {0}\nUser: {1} [{2}]\nMessage: {3}\nError Message: {4}".format(current_time, user_name, user_id, message, exception))
            print('******************** Error ********************\n')

@bot.event
async def on_ready():
    bot.google_api_key = ''

    print('\nLogged in as: ')
    print({bot.user.name})
    print({bot.user.id})
    print('\nVersion : ')
    print({discord.__version__})
    await bot.change_presence(game=discord.Game(name='>command or r/command', type=2))

    # Loading extensions ...
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}'.format(extension), file=sys.stderr)
                traceback.print_exc()
    print('Successfully logged in and booted!')

bot.run('', bot=True, reconnect=True)