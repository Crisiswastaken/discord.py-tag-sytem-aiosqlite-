# Author -> @MestoDan (discord @Ykpauneu#1625)
# Translated Russian -> English
# MIT
# And problems? -> Write me (discord)

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
from discord import DMChannel
from discord.ext import tasks
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

#==========VARS==========#

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)

#==========COGS==========#

@client.command()
@commands.guild_only()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
@commands.guild_only()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
@commands.guild_only()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#==========.db==========#

async def taginit():
    await client.wait_until_ready()
    tagdb = await aiosqlite.connect("tagData.db")
    await tagdb.execute("CREATE TABLE IF NOT EXISTS taggingData (guild_id int, user_added int, tag_name text, tag_text text, PRIMARY KEY (tag_name))")
    await tagdb.commit()

#==========CODE==========#

@client.event
async def on_ready():
	print("Hello World?, nah..")

#==========CLIENT==========#

client.loop.create_task(taginit())
client.run("YOUR TOKEN")
asyncio.run(tagdb.close())

#==========END==========#
