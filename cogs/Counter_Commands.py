################################
# Counter_Commands.py
################################

import discord
from discord.ext import commands


class Counter_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def forbid(self, ctx, message: str):
        lowered_message = ''
        for char in message:
            if char.isalpha():
                lowered_message += char.lower()
            else:
                lowered_message += char

        words = open('data/text_data/Forbidden_Words.txt', 'r+')
        word_list = []
        for line in words.readlines():
            l = line.strip()
            word_list.append(l)

        if message in word_list:
            await ctx.send(f"{lowered_message} is already forbidden!")
        else:
            words.write(f"{lowered_message}\n")
            await ctx.send(f'"{lowered_message}" has been forbidden!')



    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unforbid(self, ctx, message: str):
        lowered_message = ''
        for char in message:
            if char.isalpha():
                lowered_message += char.lower()
            else:
                lowered_message += char

        words = open('data/text_data/Forbidden_Words.txt', 'r')

        word_list = []
        for line in words.readlines():
            l = line.strip()
            word_list.append(l)

        if lowered_message in word_list:
            word_list.remove(lowered_message)
            await ctx.send(f"{lowered_message} has been unforbidden!")

            # reused code from message_events cog
            counter = open("data/text_data/Word_Counter.txt", 'r')
            first = counter.readline().strip()
            total_counter = {}
            if first != '':
                for i in range(int(first)):
                    id_counter = {}
                    id = counter.readline().strip().split(':')
                    for j in range(int(id[1])):
                        word = counter.readline().strip().split(':')
                        if word[0] != lowered_message: # this removes the unforbidden word
                            id_counter[word[0]] = word[1]
                    if (len(id_counter) > 0): # removes members who have no words stored
                        total_counter[id[0]] = id_counter

            counter = open("data/text_data/Word_Counter.txt", 'w')
            counter.write(f"{len(total_counter)}\n")
            for member in total_counter:
                counter.write(f"{member}:{len(total_counter[member])}\n")
                for w in total_counter[member]:
                    counter.write(f"{w}:{total_counter[member][w]}\n")

            counter.close()

        else:
            await ctx.send(f"{message.lower()} is not currently forbidden.")

        words = open('data/text_data/Forbidden_Words.txt', 'w')
        for word in word_list:
            words.write(f"{word}\n")


    @commands.command(aliases = ['swearjar'])
    async def check(self, ctx, member: str):
        print(f"Checking swear jar of {member}")
        f = open('data/text_data/Word_Counter.txt', 'r')
        lines = f.readlines()
        if member.startswith("<@") and len(member) >= 21:
            for line in lines:
                if member[3:-1] in line or member[2:-1] in line:
                    await ctx.send(f"{member} has said the following:")
                    l = line.strip().split(':')
                    index = lines.index(line)
                    for i in range(1, int(l[1])+1):
                        current_line = lines[index+i].strip().split(":")
                        await ctx.send(f'"{current_line[0]}" - {current_line[1]} times')

                    lines.close()
                    return

        guild_members = [member.mention for member in ctx.guild.members]
        if member not in guild_members:
            await ctx.send(f'"{member}" does not exist')
        else:
            await ctx.send(f"{member} hasn't said any forbidden words")

        lines.close()


def setup(client):
    client.add_cog(Counter_Commands(client))
