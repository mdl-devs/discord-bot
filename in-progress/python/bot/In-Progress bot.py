import discord
from discord import client
from discord.colour import Color
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json


# this is the information needed for the bot, prefix is $. Just set up to say that the bot is Working as a Test In Progress
token = 'ODAyNjgxODE0NDEzMzQ0ODA5.YAyxsQ.UYvvQk-gFHwtPWY0y542WnjBB-U'
bot = commands.Bot(command_prefix='$', case_insensitive=True)

#Changes Presence
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over the Alle Public Server"))

#Help command
bot.remove_command('help')
@bot.command()
async def help(ctx):
  embed = discord.Embed(title='Commands', color=0xFF0000)
  embed.set_thumbnail(url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  embed.add_field(name='Alle Group Info', value="alleupperstaff, allelowerstaff, info, vtcapply, members", inline=False)
  embed.add_field(name='TMP Server info', value="servers", inline=False)
  embed.add_field(name='ETS Server traffic', value="traffic, traffic2, traffic3, trafficarc, trafficus, trafficpm, trafficpmarc", inline=False)
  embed.add_field(name='ATS Server traffic', value="atstrafficus, atstrafficusarc, atstrafficeu")
  await ctx.send(embed=embed)

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
    embed.set_thumbnail(url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
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
    embed.set_thumbnail(url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
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
    embed.add_field(name='Alle Website', value=f'https://alle-group.com/', inline=False)
    embed.set_thumbnail(url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    await ctx.send(embed=embed)

#Command for Applicants
@bot.command()
async def VTCapply(ctx):
    embed=discord.Embed(Title='Alle Driver Application', color=0xFF0000)
    embed.add_field(name='Thank you!', value='We strive to have the best join our VTC!', inline=False)
    embed.add_field(name='Apply Here', value=f'https://truckersmp.com/vtc/13006', inline=False)
    embed.set_thumbnail(url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    await ctx.send(embed=embed)

#Experimental command for Server List
@bot.command()
async def servers(ctx):
 getserversURL = "https://api.truckersmp.com/v2/servers"
 r = requests.get(getserversURL)
 data = r.json()["response"]
 embed = discord.Embed(title="TMP Server Status", url="https://traffic.krashnz.com/", color=0xFF0000)
 embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
 embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
 for server in data:
    game = server["game"]
    name = server["shortname"]
    players = str(server["players"])
    maxplayers = str(server["maxplayers"])
    online = (server["online"])
    if online:
      online = " :white_check_mark:"
    else:
      online = " :x:"
    embed.add_field(name=game + ": " + name + online, value=players + '/' + maxplayers, inline=True)
 await ctx.send(embed=embed)

 #Commands for Traffic
@bot.command()
async def traffic(ctx):
  getinfoURL = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim1/top.json"
  embed = discord.Embed(title="TMP ETS2 Sim 1 Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getinfoURL)
  data = r.json()["response"]
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + "/" + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def traffic2(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim2/top.json"
  embed = discord.Embed(title="TMP ETS2 Sim 2 Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def traffic3(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim3/top.json"
  embed = discord.Embed(title="TMP ETS2 Sim 3 Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def trafficARC(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ets2/arc1/top.json"
  embed = discord.Embed(title="TMP ETS2 EU Arcade Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def trafficUS(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ets2/us/top.json"
  embed = discord.Embed(title="TMP ETS2 US Sim Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def trafficPM(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/promods/pm/top.json"
  embed = discord.Embed(title="TMP Promods Sim Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def trafficPMARC(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/promods/pm-arc/top.json"
  embed = discord.Embed(title="TMP Promods Arcade Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def ATSTrafficUS(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ats/us-sim/top.json"
  embed = discord.Embed(title="TMP ATS US Sim Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def ATSTrafficUSArc(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ats/us-arc/top.json"
  embed = discord.Embed(title="TMP ATS US Arcade Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

@bot.command()
async def ATSTrafficEU(ctx):
  getSim2TFC = "https://traffic.krashnz.com/api/v2/public/server/ats/sim/top.json"
  embed = discord.Embed(title="TMP ATS EU Sim Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)

#Command for Member Counts
@bot.command()
async def members(ctx):
 r = requests.get("https://api.truckersmp.com/v2/vtc/13006")
 data = r.json()
 members_count = r.json()['response']['members_count']
 print(members_count)
 embed = discord.Embed(title='Alle Members (WIP)', color=0xFF0000)
 embed.add_field(name="Logisitics Members", value=members_count, inline=True)
 embed.set_thumbnail(url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
 await ctx.send(embed=embed)

#Gametime Command
@bot.command()
async def gametime(ctx):
  def transformTime(timestamp):
   return datetime.datetime.fromtimestamp(timestamp).strftime('%c')
  gettimeURL = "https://api.truckersmp.com/v2/game_time"
  rt = requests.get(gettimeURL)
  gametime = rt.json()["game_time"]
  time = transformTime(gametime)
  embed = discord.Embed(title='TruckersMP Game time', color=0xFF0000)
  embed.add_field(name='Game Time', value=time, inline=True)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(text="Bot code made by StarAssassin64#9196 and Jamesmay#0001")
  await ctx.send(embed=embed)
  


bot.run(token, bot=True)
