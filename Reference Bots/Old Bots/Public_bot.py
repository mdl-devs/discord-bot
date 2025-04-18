import discord
from discord.ext.commands import Bot
from discord.colour import Color
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json
from discord.ext.commands import has_permissions, MissingPermissions
import mysql.connector
from discord import Member
from discord.utils import get
import re

# this is the information needed for the bot, prefix is $. Just set up to say that the bot is Working as a Test In Progress
token = 'ODAyNjgxODE0NDEzMzQ0ODA5.YAyxsQ.UYvvQk-gFHwtPWY0y542WnjBB-U'
bot = commands.Bot(command_prefix='$', case_insensitive=True)

#bot updates to a channel


@bot.command()
async def feed(ctx, channel: discord.channel = None):
  channel = ctx.message.channel
  await channel.send(f"Bot updates will now appear in this channel {channel}")

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
                  value='clear, nuke, ban, kick, unban, mute, unmute, warn, lwarns, rwarn, rallwarns, chnick')
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
  await ctx.send(f'{ctx.author.mention} {limit} messages cleared')
  clearmeme = 'https://tenor.com/view/-gif-9146411'
  await ctx.send(clearmeme)
  channel = bot.get_channel(794888270923300884)
  await channel.send(f"{ctx.author.mention}{ctx.author.name}#{ctx.author.discriminator} just cleared a channel by {limit} messages")

#nuke command


@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, amount=1000):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"@{ctx.author.name}#{ctx.author.discriminator} messages nuked.")
    nukememe = 'https://tenor.com/view/explosion-explode-clouds-of-smoke-gif-17216934'
    await ctx.send(nukememe)
    channel = bot.get_channel(794888270923300884)
    await channel.send(f"{ctx.author.name}#{ctx.author.discriminator} just nuked a channel.")


#Support Command
bot.counter = 0


@bot.command()
async def ticket(ctx, *, reason):
  channel = bot.get_channel(814701287643545630)
  await ctx.message.delete()
  embed = discord.Embed(title="Support Ticket Created ",
                        description="Your support ticket has been made please await staff",
                        color=0xFF0000)
  await ctx.send(embed=embed)
  bot.counter += 1
  embed2 = discord.Embed(title=f"Support Ticket #{bot.counter}",
                         description="use $claim [msgid] to claim the ticket", color=0xFF0000)
  embed2.add_field(name="Created by",
                   value=f"{ctx.author.mention}", inline=False)
  embed2.add_field(name="Reason", value=reason)
  moderator = discord.utils.get(ctx.guild.roles, id=794866561029767189)
  await channel.send(f'{moderator.mention}')
  await channel.send(embed=embed2)


#Claim Support Ticket Command
@bot.command()
async def claim(ctx, tknum):
  await ctx.message.delete()
  await ctx.send(f"{ctx.author.mention} just clamied ticket #{tknum}")


#Ping Command
@bot.command()
async def ping(ctx):
  await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')


#Kick Command (working)
@bot.command(pass_context=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  if ctx.message.author.guild_permissions.administrator:
   await member.kick(reason=reason)
   await ctx.send(f'{member.mention} has been kicked for the following reason {reason}')
   kickmeme = 'https://tenor.com/view/get-out-the-lion-king-comedy-humor-throw-gif-9615975'
   await ctx.send(kickmeme)

#Ban Command (working)


@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.message.author.guild_permissions.administrator:
     await member.ban(reason=reason)
     await ctx.send(f'{member.mention} has been banned for the following reason: {reason}')
     banmeme = 'https://tenor.com/view/bane-no-banned-and-you-are-explode-gif-16047504'
     await ctx.send(banmeme)

#Unban Command (working)


@bot.command(pass_context=True)
async def unban(ctx, *, member):
  if ctx.message.author.guild_permissions.administrator:
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"unbanned {user.mention}")
            unbanmeme = 'https://tenor.com/view/welcome-back-minions-gif-11950499'
            await ctx.send(unbanmeme)


#Command for force nickname command (working)
@bot.command(pass_context=True)
async def chnick(ctx, member: discord.Member, *, nick):
    if ctx.message.author.guild_permissions.administrator:
      await member.edit(nick=nick)
      await ctx.send(f'Nickname was changed for {member.mention}')
      await member.send(f"Your nickname has been changed to {nick} :rofl:")

#command to mute users


@bot.command()
async def mute(ctx, member: discord.Member = None, reason=None):
    if ctx.message.author.guild_permissions.administrator:
     role = discord.utils.get(ctx.guild.roles, name="Muted")
     if not member:
       await ctx.send("please specify a member")
       return
     mutememe = 'https://tenor.com/view/shhh-shush-silence-nose-gif-17895433'
     await member.add_roles(role)
     await ctx.send(f"{member.mention} was muted")
     await ctx.send(mutememe)
     await member.send(f"You have been muted in one of Alle Groups servers by {ctx.author.name}#{ctx.author.discriminator} the reason is {reason}.")


#command to unmute users
@bot.command()
async def unmute(ctx, member: discord.Member = None):
  if ctx.message.author.guild_permissions.administrator:

    try:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        unmutememe = 'https://tenor.com/view/start-speaking-loretta-scott-kemushichan-kemushichan%E3%83%AD%E3%83%AC%E3%83%83%E3%82%BF-say-something-gif-17871953'
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} speak")
        await ctx.send(unmutememe)
        await member.send(f"You have now been unmuted by {ctx.author.name}#{ctx.author.discriminator} you can now speak enjoy :)")

    except:
        await ctx.send(f"It would appear {member.mention} does not have the {role} role :( or is not allowing me to dm them ")


#command to warn people
@bot.command()
async def warn(ctx, member: discord.Member = None, *, reason=None):
 if ctx.message.author.guild_permissions.administrator:
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Fv4&4*JT61%8WGj&vwj",
      database="warnings"
  )
  mycursor = mydb.cursor()
  cursor = mydb.cursor()
  sql = "INSERT INTO userwarns  (discordname, reason, warnedby) VALUES (%s, %s, %s)"
  val = (f"{member}", f"{reason}",
         f"{ctx.author.name}#{ctx.author.discriminator}")
  mycursor.execute(sql, val)
  mydb.commit()
 try:
     await member.send(f"You have been warned in one of Alle Groups discord servers by {ctx.author.name}#{ctx.author.discriminator} for {reason}")
     await ctx.send(f"{member.mention} was warned by {ctx.author.name}#{ctx.author.discriminator} for {reason}")
 except:
     await ctx.send(f"{member.mention} I can not dm u the warning message")
     await ctx.send(f"{member.mention} was warned by {ctx.author.name}#{ctx.author.discriminator} for {reason}")


#command to remove warnings from one user
@bot.command()
async def rwarn(ctx, id):
 if ctx.message.author.guild_permissions.administrator:
  try:
      mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="Fv4&4*JT61%8WGj&vwj",
          database="warnings"
      )
      mycursor = mydb.cursor()
      cursor = mydb.cursor()
      sql = f"DELETE FROM userwarns WHERE id = {id}"
      mycursor.execute(sql)
      mydb.commit()
      await ctx.send(f"removed warning with id {id}")
  except:
      await ctx.send("I could not find that id in the database please try again")

#command to list users warnings
@bot.command()
async def lwarns(ctx, member: discord.Member = None):
  if ctx.message.author.guild_permissions.administrator:
     mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="Fv4&4*JT61%8WGj&vwj",
         database="warnings"
     )
     mycursor = mydb.cursor()
     cursor = mydb.cursor()

     mycursor.execute(
         f"SELECT id FROM userwarns WHERE discordname = '{member}';")

     myresult = mycursor.fetchall()
     cursor.execute(
         f"SELECT reason FROM userwarns WHERE discordname = '{member}';")
     result = cursor.fetchall()

     embed = discord.Embed(title=f"warnings for {member}",  Color=0xFF0000)
     embed.add_field(name="warning ids", value=f"{myresult}", inline=True)
     embed.add_field(name="reason", value=f"{result}", inline=True)
     await ctx.send(embed=embed)

#command to remove all server warnings
@bot.command()
async def rswarns(ctx):
  if ctx.message.author.guild_permissions.administrator:
      mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="Fv4&4*JT61%8WGj&vwj",
          database="warnings"
      )
      mycursor = mydb.cursor()

      mycursor.execute(
        "DELETE FROM userwarns"
      )
      mydb.commit()
      await ctx.send("removed all server warnings.") 
  
@bot.command()
async def lswarns(ctx):
  if ctx.message.author.guild_permissions.administrator:
      mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="Fv4&4*JT61%8WGj&vwj",
          database="warnings"
      )
      mycursor = mydb.cursor()

      mycursor.execute(
        "SELECT * FROM userwarns"
      )
      result = mycursor.fetchall()
      mydb.commit()
      await ctx.send(result)

#command to remove all warnings from one user
@bot.command()
async def rallwarns(ctx, member: discord.Member = None):
  if ctx.message.author.guild_permissions.administrator:
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="Fv4&4*JT61%8WGj&vwj",
       database="warnings"
   )
   mycursor = mydb.cursor()
   cursor = mydb.cursor()
   cursor.execute("select count(id) from userwarns;")
   result = cursor.fetchall()
   sql = f"DELETE FROM userwarns WHERE discordname = '{member}';"
   mycursor.execute(sql)
   mydb.commit()
   await ctx.send(f"removed all warnings for {member} Total Removed: {result}")
   await member.send(f"Congrats all your warnings were removed by {ctx.author.name}#{ctx.author.discriminator} you should thank them :) ")


@bot.command()
async def gm(ctx):
  await ctx.message.delete()
  await ctx.send(f"good morning {ctx.author.mention}")
  gmmeme = 'https://tenor.com/view/puppy-cup-good-morning-cute-puppy-yawn-gif-14168332'
  await ctx.send(gmmeme)


@bot.command()
async def gn(ctx):
  await ctx.message.delete()
  await ctx.send(f"good night {ctx.author.mention}")
  gnmeme = 'https://tenor.com/view/night-good-night-sleep-tired-collapse-gif-10609182'
  await ctx.send(gnmeme)

@bot.command()
async def gnu(ctx, member: discord.Member):
  await ctx.message.delete()
  await ctx.send(f"good night {member.mention}")
  await ctx.send("https://tenor.com/view/night-good-night-sleep-tired-collapse-gif-10609182")


@bot.command()
async def gmu(ctx, member: discord.Member):
  await ctx.message.delete()
  await ctx.send(f"good morning {member.mention}")
  gmmeme = 'https://tenor.com/view/puppy-cup-good-morning-cute-puppy-yawn-gif-14168332'
  await ctx.send(gmmeme)


@bot.command()
async def adde(ctx, date, time, start, end, game, server, note, Route, Tmp):
  await ctx.message.delete()
  role = discord.utils.find(
     lambda r: r.name == 'Upper Staff [D/M]', ctx.message.guild.roles)
  if role in ctx.author.roles:
    embed = discord.Embed(title=f"Alle Group Convoy {date}" ,  description=f"Alle Group vtc invite you to come to there convoy.",  Color=0xFF0000)
    embed.set_thumbnail(
      url='https://alle-group.com/wp-content/uploads/2021/01/cropped-alle.png')
    embed.add_field(name=f":alarm_clock: Time:", value=f"{time}", inline=False)
    embed.add_field(name=f":one:  Start:", value=f"{start}", inline=False)
    embed.add_field(name=f":two:  End:", value=f"{end}", inline=False)
    embed.add_field(name=f":truck: Game:", value=f"{game}", inline=False)
    embed.add_field(name=f":globe_with_meridians: Server:", value=f"{server}", inline=False)
    embed.add_field(name=f":pushpin: Note:", value=f"{note}", inline=False)
    embed.add_field(name=f":map: Route:", value=f"[Link]({Route})", inline=False)
    embed.add_field(name=f":page_facing_up: Tmp:",
                  value=f"[Link]({Tmp})", inline=False)
    embed.set_footer(text=f"Posted by {ctx.author.mention}")
    await ctx.send(embed=embed)
  else:
      error = discord.Embed(title="Missing permissions",
                            description=f"You dont have the role `Upper Staff [D/M]`")
      await ctx.send(embed=error)


@bot.command()
async def addep(ctx, route, channelname, *, message):
 await ctx.message.delete()
 role = discord.utils.find(
     lambda r: r.name == 'Upper Staff [D/M]', ctx.message.guild.roles)
 if role in ctx.author.roles:
        
  category = discord.utils.get(ctx.guild.categories, name="𝙀𝙫𝙚𝙣𝙩𝙨 𝘾𝙖𝙡𝙚𝙣𝙙𝙚𝙧")
  event_channel = await ctx.guild.create_text_channel(f"{channelname}", category=category)
  eventinfo = discord.Embed(
     title=f"{channelname}", description=f"New convoy that Alle Group will be attending",  Color=0xFF0000)
  eventinfo.add_field(name=f"Convoy Info", value=f"{message}", inline=False) 
  eventinfo.add_field(name=f"Route/image", value=f"{route}", inline=False)
  await event_channel.send(embed=eventinfo)
  await event_channel.edit(sync_permissions=True)
 else:
      error = discord.Embed(title="Missing permissions", description=f"You dont have the role `Upper Staff [D/M]`")
      await ctx.send(embed=error) 
bot.run(token, bot=True)
