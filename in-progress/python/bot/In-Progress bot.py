import discord
from discord import client
from discord.colour import Color
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json
from discord.ext.commands import has_permissions, MissingPermissions
import mysql.connector

# this is the information needed for the bot, prefix is $. Just set up to say that the bot is Working as a Test In Progress
token = 'PRIVATE INFO'
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
  embed.set_thumbnail(
      url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
  embed.set_footer(
      text="Bot code developed by Alle Devs")
  embed.add_field(name='Alle Group Info',
                  value="alleupperstaff, allelowerstaff, info, vtcapply, members", inline=False)
  embed.add_field(name='TMP Server info', value="servers", inline=False)
  embed.add_field(name='ETS Server traffic',
                  value="traffic, traffic2, traffic3, trafficarc, trafficus, trafficpm, trafficpmarc", inline=False)
  embed.add_field(name='ATS Server traffic',
                  value="atstrafficus, atstrafficusarc, atstrafficeu")
  embed.add_field(name='Administation Commands (Admin Only)',
                  value='clear, ')
  await ctx.send(embed=embed)


#Command for seeing [A'G] Upper Staff
@bot.command()
async def alleupperstaff(ctx):
    await ctx.message.delete()
    embed = discord.Embed(Title='Alle Group Upper Staff', color=0xFF0000)
    embed.add_field(name="CEO", value="Sully#3056", inline=False)
    embed.add_field(name="COO",
                    value="CarlJL2006#8589, ProjektSpeedy#2286, and Dr. Doof#1135", inline=False)
    embed.add_field(name="CCO", value="spock#0001 and LC#2328", inline=False)
    embed.add_field(name="DIRECTOR OF AGRICULTURE",
                    value="NoahTheFox#4148", inline=False)
    embed.add_field(name="DIRECTOR OF TRANSPORT",
                    value="lewis#4672", inline=False)
    embed.add_field(name="DIRECTOR OF EVENTS/MEDIA",
                    value="Sani#0189", inline=False)
    embed.add_field(name="DIRECTOR OF DEVELOPEMENT",
                    value="_Guuuty#8864", inline=False)
    embed.add_field(name='DIRECTOR OF EXAMINATIONS',
                    value='Yzzoxi#3590', inline=False)
    embed.set_thumbnail(
        url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    await ctx.send(embed=embed)


#Command for VTC Information
@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(Title='VTC Information', Color=0xFF0000)
    embed.add_field(name='Name', value='Alle Group', inline=False)
    embed.add_field(
        name='Slogan', value='Keeping the world moving!', inline=False)
    embed.add_field(
        name='Devisions', value='Alle Logistics, Alle Transport, Alle Air, Alle Farms', inline=False)
    embed.add_field(name='CEO and Founder',
                    value='Sully#3056 is the Founder and CEO since 27th March, 2020!', inline=False)
    embed.add_field(name='Alle Website',
                    value=f'https://alle-group.com/', inline=False)
    embed.set_thumbnail(
        url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    await ctx.send(embed=embed)


#Command for Applicants
@bot.command()
async def VTCapply(ctx):
    embed = discord.Embed(Title='Alle Driver Application', color=0xFF0000)
    embed.add_field(
        name='Thank you!', value='We strive to have the best join our VTC!', inline=False)
    embed.add_field(name='Apply Here',
                    value=f'https://truckersmp.com/vtc/13006', inline=False)
    embed.set_thumbnail(
        url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    await ctx.send(embed=embed)


#Experimental command for Server List
@bot.command()
async def servers(ctx):
 getserversURL = "https://api.truckersmp.com/v2/servers"
 r = requests.get(getserversURL)
 data = r.json()["response"]
 embed = discord.Embed(title="TMP Server Status",
                       url="https://traffic.krashnz.com/", color=0xFF0000)
 embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
 embed.set_footer(
     text="Bot code developed by Alle Devs")
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
    embed.add_field(name=game + ": " + name + online,
                    value=players + '/' + maxplayers, inline=True)
 await ctx.send(embed=embed)

 #Commands for Traffic


@bot.command()
async def traffic(ctx):
  getinfoURL = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim1/top.json"
  embed = discord.Embed(title="TMP ETS2 Sim 1 Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
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
async def drivers(ctx):
  await ctx.message.delete()
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Fv4&4*JT61%8WGj&vwj",
      database="alle_hub"
  )
  mycursor = mydb.cursor()
  cursor = mydb.cursor()

  mycursor.execute("SELECT name FROM users")
  myresult = mycursor.fetchall()
  cursor.execute("select count(name) from users;")
  result = cursor.fetchall()
  embed = discord.Embed(title="Drivers List", color=0xFF0000)
  embed.add_field(name="List of drivers", value=myresult, inline=False)
  embed.add_field(name="Total Number Of Drivers", value=result, inline=False)
  #await ctx.send(tabulate(myresult, headers=['users'], tablefmt='psql'))
  await ctx.send(embed=embed)
  results = result

  channel = bot.get_channel(794888270923300884)
  embed1 = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}",
                         icon_url=ctx.author.avatar_url, color=0xFF0000)
  embed1.add_field(name="This user  just checked the amount of drivers using ",
                   value="`?drivers`", inline=False)
  await channel.send(embed=embed1)


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
  embed.set_footer(
      text="Bot code developed by Alle Devs")
  await ctx.send(embed=embed)


#Command for Minecraft server Information
@bot.command(pass_context=True)
@commands.has_role(794865933487046677)
async def minecraftinfo(ctx):
    embed = discord.Embed(title='Minecraft Server Info', color=0xFF0000)
    embed.add_field(name='Minecraft Small Server',
                    value='176.57.144.138 | 4 slots', inline=False)
    embed.add_field(name='Minecraft Large Server',
                    value='allesever2.aternos.me | 100 slots', inline=False)
    embed.set_thumbnail(
        url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    embed.set_footer(
        text="Bot code developed by Alle Devs")
    await ctx.send(embed=embed)


#Clear Commands
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, limit: int = None):
  await ctx.message.delete()
  await ctx.channel.purge(limit=limit)
  await ctx.send(f'Deleted {limit} messages')
  channel = bot.get_channel(794888270923300884)
  await channel.send(f"{ctx.author.name}#{ctx.author.discriminator} just purged a channel by {limit} messages")

#nuke command


@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, amount=1000):
    await ctx.channel.purge(limit=amount)
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} ")


#Support Command
@bot.command(pass_contex=True)
@commands.has_permissions(administrator=True)
async def supportmessage(ctx, user: discord.User, *, message):
    #user = bot.get_user(755493797160288286)
    await ctx.message.delete()
    await user.send(f"{ctx.author.name}#{ctx.author.discriminator} just sent u a message contents = {message}")


#Player report command
#@bot.command()
#async def bplayer(ctx, name, discordname, tmpid, steamid):
#  embed = discord.Embed(
#      title="New Player Issue Report Player Name" "=" f"{name}")
#  embed.add_field(name="Discord Tag/Name",
#                  value=f"{discordname}", inline=False)
#  embed.add_field(name="Tmp ID", value=f"{tmpid}", inline=False)
#  embed.add_field(name="Steam ID", value=f"{steamid}", inline=False)
#  await ctx.send(embed=embed)


#Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')


#Kick Command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} has been kicked for the following reason{reason}')


#Ban Command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned for the following reason: {reason}')


#Unban Command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"unbanned {user.mention}")


#Command for force nickname command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def chnick(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


bot.run(token, bot=True)
