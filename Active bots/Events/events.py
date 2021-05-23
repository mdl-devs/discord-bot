import discord
from discord.ext.commands import ChannelNotFound
from dhooks import Webhook
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json
import mysql.connector
import asyncio
import aiohttp
from discord import Member, webhook
from discord.ext.commands import has_permissions, MissingPermissions
import traceback
import sys
from datetime import datetime as dt
import time
from discord.ext.commands import cooldown, BucketType



intents = intents = discord.Intents.all()


# Bots Token 
token = 'token goes here'

# Bots prefix
bot  = commands.Bot(command_prefix=('e/'))


# removes help command
bot.remove_command('help')


# ping command
@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')


# starts bot
bot.run(token)    
