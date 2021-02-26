import discord
from discord.colour import Color
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json

getserversURL = "https://api.truckersmp.com/v2/servers"
gettimeURL = "https://api.truckersmp.com/v2/game_time"

client = discord.Client()


@bot.command()
async def members(ctx):
 r = requests.get("https://api.truckersmp.com/v2/vtc/13006")
 data = r.json()
 members_count = r.json()['response']['members_count']
 print(members_count)
 await ctx.send(members_count

@bot.command()
async def servers(ctx):
    
getserversURL = "https://api.truckyapp.com/v2/truckersmp/servers"
b = requests.get(getserversURL)
data = b.json()["response"]
for server in data:
    serverid = server["id"]
    game = server["game"]
    name = server["shortname"]
    players = str(server["players"])
    queue = str(server["queue"])
    maxplayers = str(server["maxplayers"])
    online = (server["online"])
    if online:
      online = "Online"
    else:
      online = "Offline"
      
@bot.command()
async def servers(ctx):
    await ctx.send("---------")
    await ctx.send(name + " (" + game + ") - Status: " + online )
    await ctx.send("Drivers online: " + players + "/" + maxplayers)
    await ctx.send("Players in queue: " + queue)



Bot.run('Nzk3NjE4MTQzMTczMjc5NzU0.X_pFyA.N75wby0uAALjGP-rFUCjIDYVSo0', bot=True)