################################
# bot.py
################################

import discord
import os
from discord.ext import commands

# INITIALIZATION

client = commands.Bot(command_prefix='/')
f = open('BotToken.txt', 'r')  # BotToken.txt contains the private token
TOKEN = f.readline()
f.close()

# EVENTS


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('with my code'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have access to that command.')
        print(f"{ctx.message.author} tried to use a command they don't have access to")


# COMMANDS

@client.command()
@commands.has_permissions(administrator=True)
async def load_cog(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'Loaded cog: {extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def unload_cog(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(f'Unloaded cog: {extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def movehere(ctx):  # moves all members in vc to the vc of the author
    channels = ctx.guild.voice_channels
    for channel in channels:
        for member in channel.members:
            if member == ctx.author:
                dest = channel
                break

    for channel in channels:
        if channel != dest:
            for member in channel.members:
                await member.move_to(dest)

    await ctx.send(f'Moved all members to channel: {dest.name}')
    print(f'{ctx.author} moved all members to channel: {dest.name}')


# LOAD COGS

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded cog: {filename}')


# RUN

client.run(TOKEN)
