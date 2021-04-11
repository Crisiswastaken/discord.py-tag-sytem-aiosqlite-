#==========IMPORTS==========#

import discord
from discord.ext import commands
import requests
import sqlite3
from discord.ext.commands import Bot
from discord import Game
from discord import Embed
import time
import asyncio
from discord import utils
from discord import Activity, ActivityType
from discord.ext.commands import errors
import datetime
import random
import json
import math
import os
import aiosqlite
import aiofiles
import aiohttp
import pytz
from datetime import datetime
import nekos
import sys
from samp_client.client import SampClient
import psutil
import colorama

#==========CODE==========#

class TagsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_unload(self):
        print("TagsCog - Unloaded")
        print("---")

    @commands.command()
    @commands.guild_only()
    async def addtag(self, ctx, tag_name, *, tag_text):
        tagdb = await aiosqlite.connect("tagData.db")
        await tagdb.execute("INSERT OR ROLLBACK INTO taggingData (guild_id, user_added, tag_name, tag_text) VALUES (?,?,?,?)", (ctx.guild.id, ctx.author.id, tag_name, tag_text))
        await tagdb.commit()
        embed=discord.Embed(title=".addtag", color=0x000000)
        embed.add_field(name="Status:", value="Added", inline=False)
        embed.add_field(name="Name:", value=tag_name, inline=False)
        embed.add_field(name="Text:", value=tag_text, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def tag(self, ctx, tag_name):
        tagdb = await aiosqlite.connect("tagData.db")

        async with tagdb.execute("SELECT user_added, tag_text FROM taggingData WHERE guild_id = ? AND tag_name = ?", (ctx.guild.id, tag_name)) as cursor:
            async for tagvar in cursor:
                user_added, tag_text = tagvar
                user_name = ctx.guild.get_member(user_added)

            embed=discord.Embed(title=f".tag {tag_name}", description="", color=0x000000)
            embed.add_field(name="Text:", value=tag_text, inline=False)
            embed.add_field(name="Added:", value=user_name.mention, inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def mytags(self, ctx, member:discord.Member=None):
        member = ctx.author
        tagdb = await aiosqlite.connect("tagData.db")
        index = 0
        embed=discord.Embed(title=f"Tags {member.name}", description="", color=0x000000)
        embed.set_thumbnail(url=member.avatar_url)
        msg = await ctx.send(embed=embed)
        async with tagdb.execute("SELECT tag_name, tag_text FROM taggingData WHERE guild_id = ? AND user_added = ?", (ctx.guild.id, member.id,)) as cursor:
            async for tagget, textget in cursor:
                index += 1
                tag_name = tagget
                tag_text = textget
                embed.description += f"Tag: {index} | Name: {tag_name}\n"
            await msg.edit(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def removetag(self, ctx, tag_input):
        tagdb = await aiosqlite.connect("tagData.db")
        await tagdb.execute("DELETE FROM taggingData WHERE guild_id = ? AND tag_name = ?", (ctx.guild.id, tag_input))
        await tagdb.commit()
        embed = discord.Embed(title=".removetag",color=0xff0000)
        embed.add_field(name='Admin:',value=ctx.message.author.mention,inline=False)
        embed.add_field(name='Tag:',value=tag_input,inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def tags(self, ctx, member:discord.Member):
        tagdb = await aiosqlite.connect("tagData.db")
        index = 0
        embed=discord.Embed(title=f"Tags {member.name}", description="", color=0x000000)
        embed.set_thumbnail(url=member.avatar_url)
        msg = await ctx.send(embed=embed)
        async with tagdb.execute("SELECT tag_name, tag_text FROM taggingData WHERE guild_id = ? AND user_added = ?", (ctx.guild.id, member.id,)) as cursor:
            async for tagget, textget in cursor:
                index += 1
                tag_name = tagget
                tag_text = textget
                embed.description += f"Tag: {index} | Name: {tag_name}\n"
            await msg.edit(embed=embed)

#==========LOADING==========#

def setup(client):      
    client.add_cog(TagsCog(client))
    print("TagsCog - Loaded")
    print("---")

#==========END==========#
