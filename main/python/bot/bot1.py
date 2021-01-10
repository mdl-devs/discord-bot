import discord
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json

token = 'NzcwMzQzMjM1MjE3Nzg0ODYy.X5cMCw.2lSdAtFEIvx4QkvuKp9PZXfvecc'
bot = commands.Bot(command_prefix='?', case_insensitive=True)
game = discord.Game('alle drivers hub')
@bot.command()
async def info(ctx):
  await ctx.message.delete()
  embed=discord.Embed(title="ALLE GROUP", color=0xFF0000)
  embed.add_field(name="CEO", value="Sully#3056 ", inline=False)
  embed.add_field(name="COO", value="CarlJL2006#8589,Dr. Doof#1135", inline=False)
  embed.add_field(name="CCO", value="Speedy#2286,LC#2328", inline=False)
  embed.add_field(name="DIRECTOR OF AGRICULTURE", value="NoahTheFox#4148", inline=False)
  embed.add_field(name="DIRECTOR OF TRANSPORT", value="lewis#4672", inline=False)
  embed.add_field(name="DIRECTOR OF EVENTS/MEDIA", value="Santa Ho Ho Ho#2982", inline=False)
  embed.add_field(name="DIRECTOR OF DEVELOPEMENT", value="_Guuuty#8864", inline=False)
  embed.add_field(name="DIRECTOR OF HUMAN RESOURCES", value="Murphy#2843", inline=False)
  embed.add_field(name="HUMAN RESOURCES", value="Maki#9235,Ozone87#2547,MerlinDaSkeley#1559,Yzzoxi#3590", inline=False)
  embed.add_field(name="DEPARTMENT MANAGER", value="7cleverboys#1346,Columbusgaming1492#3904", inline=False)
  embed.add_field(name="EVENT / MEDIA TEAM", value="Gimmification#0727,Orchestrion", inline=False)
  await ctx.send(embed=embed)
name = "Alle Logistics"
slogan = "Keeping the world moving"
@bot.command()
async def vtlog(ctx):
  embed=discord.Embed(title="VT LOG INFO", color=0xFF0000)
  embed.add_field(name="VTC NAME", value=f"{name}", inline=False)
  embed.add_field(name="SLOGAN", value=f"{slogan}", inline=False)
  embed.add_field(name="FOUNDED", value=f"27th March 2020", inline=False)
  embed.add_field(name="DRIVERS", value=f"error 340", inline=False)
  await ctx.send(embed=embed)
  await ctx.message.delete()
@bot.command()
async def nextconvoy(ctx):
  embed=discord.Embed(title="ALLE GROUPS NEXT CONVOY", color=0xFF0000)
  embed.add_field(name="DATE", value=f"Wednesday 13th January 2021", inline=True)
  embed.add_field(name="SERVER", value=f"Sim 3", inline=False)
  embed.add_field(name="ORIGIN", value=f"Amsterdam ", inline=False)
  embed.add_field(name="DESTINATION", value=f"Berlin", inline=False)
  embed.add_field(name="MEET", value=f"18:30 GMT", inline=False)
  embed.add_field(name="DEPART", value=f"19:00 GMT", inline=False)
  embed.add_field(name="CARS", value=f"No", inline=False)
  embed.add_field(name="TRAILERS", value=f"Not Required but Highly Recommended, No Doubles or Triples", inline=False)
  embed.add_field(name="NO TIME ZONE", value=f"https://notime.zone/MPoqHhTnYL2oP", inline=False)
  embed.add_field(name="TMP EVENT SIGN UP ", value=f"https://truckersmp.com/events/23-alle-logistics-weekly-convoy#01", inline=False)
  embed.add_field(name="Wanna add a convoy", value=f"this option is coming soon", inline=False)
  await ctx.send(embed=embed)
  await ctx.message.delete()
@bot.command()
async def apply(ctx):
  embed=discord.Embed(title="WELCOME TO ALLE GROUP", color=0xFF0000)
  embed.add_field(name="APPLY HERE", value=f"https://truckersmp.com/vtc/13006", inline=True)
  await ctx.send(embed=embed)
  await ctx.message.delete()
  
def transformTime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%c')
getserversURL = "https://api.truckersmp.com/v2/servers"
gettimeURL = "https://api.truckersmp.com/v2/game_time"
r = requests.get(getserversURL)
rt = requests.get(gettimeURL)
data = r.json()["response"]
gametime = rt.json()["game_time"]
print("Server List")
print("")
print("(Game Time: " + transformTime(gametime) + ")")

for server in data:
    serverid = server["id"]
    game = server["game"]
    name = server["name"]
    players = str(server["players"])
    queue = str(server["queue"])
    maxplayers = str(server["maxplayers"])
    online = (server["online"])
    if online:
      online = "Online"
    else:
      online = "Offline"
    print("---------")
    print(name + " (" + game + ") - Status: " + online )
    print("Drivers online: " , players + "/" + maxplayers)
    print("Players in queue: " + queue)   
    def transformTime(timestamp):
     return datetime.datetime.fromtimestamp(timestamp).strftime('%c')
getserversURL = "https://api.truckersmp.com/v2/servers"
gettimeURL = "https://api.truckersmp.com/v2/game_time"
r = requests.get(getserversURL)
rt = requests.get(gettimeURL)
data = r.json()["response"]
for server in data:
    serverid = server["id"]
    game = server["game"]
    name = server["name"]
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
  await ctx.message.delete()
  await ctx.send("---------")
  await ctx.send(name + " (" + game + ") - Status: " + online )
  await ctx.send("Drivers online: " , players + "/" + maxplayers)
  await ctx.send("Players in queue: " + queue)@bot.command()
async def tmp(ctx):
  command = "tmp are shit"
  await ctx.send (f"{command}")
@bot.command()
async def carl(ctx):
   await ctx.send (" Mr bot greeter   :rofl: nutter :smile:")
@bot.command()
async def speedy(ctx):
   await ctx.send (" Im fast as f##k boiiii. *** look at my disco lights ***")
@bot.command()
async def sully(ctx):
    await ctx.send (" the boss i dont mess with him `error 68` ")
@bot.command()
async def add(ctx):
     await ctx.send ("wooooo steady there i am not that clever yet ` command coming soon `")
i = requests.get("https://tracker.ets2map.com/v3/fullmap")
response = i.json()
print (response)
bot.run(token, bot=True)
