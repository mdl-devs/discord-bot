import discord
from discord.colour import Color
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json


# this is the information needed for the bot, prefix is $. Just set up to say that the bot is Working as a Test In Progress
token = 'Nzk3NjE4MTQzMTczMjc5NzU0.X_pFyA.N75wby0uAALjGP-rFUCjIDYVSo0'
bot = commands.Bot(command_prefix='$', case_insensitive=True)
game = discord.Game('Working on myself, Test in Progress')

#Command for seeing [A'G] Upper Staff
@bot.command()
async def alleupperstaff(ctx):
    await ctx.message.delete()
    embed=discord.Embed(Title='Alle Group Upper Staff', color=0xFF0000)
    embed.add_field(name="CEO", value="Sully#3056", inline=False)
    embed.add_field(name="COO", value="CarlJL2006#8589 and Dr. Doof#1135", inline=False)
    embed.add_field(name="CCO", value="Speedy#2286 and LC#2328", inline=False)
    embed.add_field(name="DIRECTOR OF AGRICULTURE", value="NoahTheFox#4148", inline=False)
    embed.add_field(name="DIRECTOR OF TRANSPORT", value="lewis#4672", inline=False)
    embed.add_field(name="DIRECTOR OF EVENTS/MEDIA", value="TRUCKERBEAN#2982", inline=False)
    embed.add_field(name="DIRECTOR OF DEVELOPEMENT", value="_Guuuty#8864", inline=False)
    embed.add_field(name="DIRECTOR OF HUMAN RESOURCES", value="Murphy#2843", inline=False)
    embed.add_field(name='DIRECTOR OF EXAMINATIONS', value='Yzzoxi#3590', inline=False)
    await ctx.send(embed=embed)

#Command for [A'G] Lower Staff
@bot.command()
async def allelowerstaff(ctx):
    await ctx.message.delete()
    embed=discord.Embed(Title='Alle Group Lower Staff', color=0xFF0000)
    embed.add_field(name="Development Team", value="Adriano Trezub#3845, DaExodiaヰガび™#3621, StarAssassin64#9196", inline=False)
    embed.add_field(name='Human Resources', value='Sani#4113', inline=False)
    embed.add_field(name='Driver Supervisor', value='Maki#9235', inline=False)
    embed.add_field(name='Department Manager', value='7celverboys#1346', inline=False)
    embed.add_field(name='Event/Media Team', value='Vacant | Open for Applicants', inline=False)
    await ctx.send(embed=embed)

#Command for VTC Information
@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed=discord.Embed(Title='VTC Information', Color=0xFF0000)
    embed.add_field(name='Name', value='Alle Group', inline=False)
    embed.add_field(name='Slogan', value='Keeping the world moving!', inline=False)
    embed.add_field(name='Devisions', value='Alle Logistics, Alle Transport, Alle Air, Alle Farms', inline=False)
    embed.add_field(name='CEO and Founder', value='Sully#3056 is the Founder and CEO since 27th March, 2020!', inline=False)
    embed.add_field(name='Drivers', value='23 drivers and counting')
    await ctx.send(embed=embed)

#Command for Applicants
@bot.command()
async def VTCapply(ctx):
    embed=discord.Embed(Title='Thank you for choosing Alle Logisitics', color=0xFF0000)
    embed.add_field(name='Apply Here', value=f'https://truckersmp.com/vtc/13006', inline=True)
    await ctx.send(embed=embed)

#Experimental command for Server List
@bot.command()
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
async def servers(ctx):
    await ctx.send("---------")
    await ctx.send(name + " (" + game + ") - Status: " + online )
    await ctx.send("Drivers online: " + players + "/" + maxplayers)
    await ctx.send("Players in queue: " + queue)


bot.run(token, bot=True)