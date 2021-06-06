import discord
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from pip._vendor import requests
import datetime
import json
import mysql.connector
import asyncio
from tabulate import tabulate
import aiohttp
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import traceback
import sys
from discord.ext.commands import CommandNotFound
import bcrypt

token = 'NzcwMzQzMjM1MjE3Nzg0ODYy.X5cMCw.stMS01QFVChvz-8OQchATM8yTKk'
bot = commands.Bot(commands.when_mentioned_or('?'))
# no longer needed game = discord.Game('Alle groups server')

truckerbd = 'Jamesmay#0001'


@bot.command()
async def info(ctx):
  await ctx.message.delete()
  embed = discord.Embed(title="ALLE GROUP", color=0xFF0000)
  embed.add_field(name="CEO", value="Sully#3056 ", inline=False)
  embed.add_field(
      name="COO", value="CarlJL2006#8589,Speedy#2286", inline=False)
  embed.add_field(name="CCO", value="jamesmay#8635,LC#2328", inline=False)
  embed.add_field(name="DIRECTOR OF AGRICULTURE",
                  value="NoahTheFox#4148", inline=False)
  embed.add_field(name="TRANSPORT MANGER", value="lewis#4672", inline=False)
  embed.add_field(name="EVENT MANAGER", value="TRUCKERBEAN#0001", inline=False)
  embed.add_field(name="DIRECTOR OF DEVELOPEMENT",
                  value="_Guuuty#8864", inline=False)
  embed.add_field(name="DIRECTOR OF HUMAN RESOURCES",
                  value="Desmond Doss#9332", inline=False)
  embed.add_field(name="DEX", value="Yzzoxi#3590", inline=False)
  embed.add_field(
      name="DEV TEAM", value="Adriano Trezub#3845, StarAssassin64#9196", inline=False)
  embed.add_field(name="HUMAN RESOURCES",
                  value="Saà¹‡à¹‡à¹‡ni#8080", inline=False)
  embed.add_field(name="EVENT / MEDIA TEAM",
                  value="currently hiring", inline=False)
  await ctx.send(embed=embed)
  await ctx.message.delete()


@bot.command()
async def nextconvoy(ctx):
  embed = discord.Embed(title="ALLE GROUPS NEXT CONVOY", color=0xFF0000)
  embed.add_field(name="DATE", value=f"N/A", inline=True)
  embed.add_field(name="SERVER", value=f"N/A", inline=False)
  embed.add_field(name="ORIGIN", value=f"N/A ", inline=False)
  embed.add_field(name="DESTINATION", value=f"N/A", inline=False)
  embed.add_field(name="MEET", value=f"N/A", inline=False)
  embed.add_field(name="DEPART", value=f"N/A", inline=False)
  embed.add_field(name="CARS", value=f"N/A", inline=False)
  embed.add_field(name="TRAILERS", value=f"N/A", inline=False)
  embed.add_field(name="NO TIME ZONE", value=f"N/A", inline=False)
  embed.add_field(name="TMP EVENT SIGN UP ", value=f"N/A", inline=False)
  embed = discord.Embed(description="do `announce1` or `convoy` to add a convoy xD. But pls note that at the current time CONVOYS ARE CANCELLED. You are not seeing the convoy info due to convoys being stopped. :) P.S the next couple of public convoys are `25th-january-prime-convoy` `26th-january-rlc-convoy` `28th-january-truckers-chn-convoy` hope to see ya at them. ", inline=False)
  await ctx.send(embed=embed)
  await ctx.message.delete()


@bot.command()
async def apply(ctx):
  embed = discord.Embed(title="WELCOME TO ALLE GROUP", color=0xFF0000)
  embed.add_field(name="APPLY HERE",
                  value=f"https://truckersmp.com/vtc/13006", inline=True)
  await ctx.send(embed=embed)
  await ctx.message.delete()


@bot.command()
async def test(ctx, *, message):
    embed = discord.Embed(description=message, color=0xFF0000)
    await ctx.send(embed=embed)


# @bot.command()
# async def announce(ctx, *, message):
#     await ctx.message.delete()
#     channel1 = bot.get_channel(794887947865817088)
#     embed = discord.Embed(description=message, color=0xFF0000)
#     embed.set_footer(
#         text=f"sent by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
#     await channel1.send(embed=embed)


@bot.command()
async def hub(ctx, name, steam_ID, tmp_ID, password):
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="user_hub_info"
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO user_info_basic  (steamID, tmpID, name, password) VALUES (%s, %s, %s, %s)"
    val = (f"{steam_ID}", f"{tmp_ID}", f"{name}", f"{password}")
    mycursor.execute(sql, val)
    mydb.commit()

    embed = discord.Embed(
        title=" Alle Hub Account Made", color=0xFF0000
    )
    embed.add_field(name="UserName", value=name, inline=False)
    embed.add_field(name="Tmp ID", value=tmp_ID, inline=False)
    embed.add_field(name="Steam ID", value=steam_ID, inline=False)
    embed.add_field(
        name="Password", value="what ever u set it to :wink:", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def partnerc(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(
        title="ALLE GROUP PARTNER / PUBLIC CONVOY POSTING SYSTEM", color=0xFF0000)
    embed.add_field(name="convoy info", value=message, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def carl(ctx):
   await ctx.message.delete()
   await ctx.send(" Mr bot greeter   :rofl: nutter :smile:")


#@bot.command()
#async def speedy(ctx):
   #await ctx.message.delete()
   ##(" Im fast as f##k boiiii. *** look at my disco lights ***")
   ##await ctx.send("its my brithday woooooo im another year older :partying_face: :partying_face: :partying_face: :partying_face: :partying_face: :partying_face: :partying_face: :partying_face:")
   ##("https://cdn.discordapp.com/attachments/794887186990366750/801142872966561812/20210119153518_1.jpg")
   #await ctx.send("https://cdn.discordapp.com/attachments/797843659957600266/809214826484203550/20210120004307_1.png")
@bot.command()
async def clear(ctx, limit: int = None):
    passed = 0
    failed = 0
    async for msg in ctx.message.channel.history(limit=limit):
        if msg.author.id == bot.user.id:
            try:
                await msg.delete()
                passed += 1
            except:
                failed += 1
    print(f"[Complete] Removed {passed} messages with {failed} fails")


@bot.command()
async def nuke(ctx, amount=1000):
    await ctx.channel.purge(limit=amount)
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} ")


@bot.command()
async def sully(ctx):
    await ctx.message.delete()
    await ctx.send("ahh mr viper what do u need with mr viper")


@bot.command()
async def dm(ctx, user: discord.User, *, message):
    #user = bot.get_user(755493797160288286)
    await ctx.message.delete()
    await user.send(f"{ctx.author.name}#{ctx.author.discriminator} just sent u a message contents = {message}")


@bot.command()
@commands.has_role('Human Resources')
async def add(ctx, steamid, tmpid, name):
 await ctx.message.delete()
 mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="Fv4&4*JT61%8WGj&vwj",
     database="alle_hub"
 )
 mycursor = mydb.cursor()

 sql = "INSERT INTO users (steamid, tmpid, name) VALUES (%s, %s, %s)"
 val = (f"{steamid}", f"{tmpid}", f"{name}")
 mycursor.execute(sql, val)

 mydb.commit()
 embed = discord.Embed(title="Welldone u added a driver", color=0xFF0000)
 embed.add_field(name="Name", value=f"{name}", inline=False)
 embed.add_field(name="TMP ID", value=f"{tmpid}", inline=False)
 embed.add_field(name="STEAM ID", value=f"{steamid}", inline=False)
 await ctx.send(embed=embed)
 channel1 = bot.get_channel(794888270923300884)
 embed1 = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}",
                        icon_url=ctx.author.avatar_url, color=0xFF0000)
 embed1.add_field(
     name=f"This user  just added driver {name} to the api using", value="`?add`", inline=False)
 await channel1.send(embed=embed1)
 mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="Fv4&4*JT61%8WGj&vwj",
     database="alle_hub"
 )
 cursor = mydb.cursor()
 cursor.execute("select count(name) from users;")
 result = cursor.fetchall()
 results = result
 await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{results} drivers"))


@bot.command()
async def dev1(ctx):
  if ctx.message.author.server_permissions.administrator:
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
   await ctx.send(tabulate(myresult, headers=['users'], tablefmt='psql'))


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


@bot.event
async def on_ready():
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="Fv4&4*JT61%8WGj&vwj",
       database="alle_hub"
   )
   cursor = mydb.cursor()
   cursor.execute("select count(name) from users;")
   result = cursor.fetchall()
   results = result
   print("My body is ready")
   await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"CONGRATS ALLE GROUP WE ARE SO PROUD OF U :)"))
# change async def (members) change the members bit to what ever u want.


@bot.command()
async def members(ctx):
 r = requests.get("https://api.truckersmp.com/v2/vtc/13006")
 data = r.json()
 members_count = r.json()['response']['members_count']
 await ctx.send(f'The amount of drivers and staff in this vtc is {members_count}')


@bot.command()
async def bplayer(ctx, name, discordname, tmpid, steamid):
  embed = discord.Embed(
      title="New Player Issue Report Player Name" "=" f"{name}")
  embed.add_field(name="Discord Tag/Name",
                  value=f"{discordname}", inline=False)
  embed.add_field(name="Tmp ID", value=f"{tmpid}", inline=False)
  embed.add_field(name="Steam ID", value=f"{steamid}", inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def vtchop(ctx, name, discordname, tmpid, steamid):
  embed = discord.Embed(
      title="New Vtc Hopper Report Player Name" "=" f"{name}")
  embed.add_field(name="Discord Tag/Name",
                  value=f"{discordname}", inline=False)
  embed.add_field(name="Tmp ID", value=f"{tmpid}", inline=False)
  embed.add_field(name="Steam ID", value=f"{steamid}", inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def servers(ctx):
 await ctx.message.delete()
 getserversURL = "https://api.truckersmp.com/v2/servers"
 r = requests.get(getserversURL)
 data = r.json()["response"]
 embed = discord.Embed(title="TMP Server Status",
                       url="https://traffic.krashnz.com/", color=0xFF0000)
 embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
 embed.set_footer(
     text="Bot Devloped by  StarAssassin64#9196 and Jamesmay#0001")
 for server in data:
    serverid = server["id"]
    game = server["game"]
    name = server["shortname"]
    players = str(server["players"])
    queue = str(server["queue"])
    maxplayers = str(server["maxplayers"])
    online = (server["online"])
    if online:
      online = " :white_check_mark:"
    else:
      online = " :x:"
    embed.add_field(name=game + ": " + name + online,
                    value=players + '/' + maxplayers, inline=True)
 await ctx.send(embed=embed)
# command ofa


@bot.command()
async def traffic(ctx):
 await ctx.message.delete()
 getserversURL = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim1/top.json"
 r = requests.get(getserversURL)
 data = r.json()["response"]
 embed = discord.Embed(title="TMP Traffic Status (SIM 1)",
                       url="https://traffic.krashnz.com/", color=0xFF0000)
 embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
 embed.set_footer(
     text="Bot Devloped by  StarAssassin64#9196 and Jamesmay#0001")
 for top in data["top"]:
    id = top["id"]
    name = top["name"]
    country = top["country"]
    players = str(top["players"])
    severity = top["severity"]
    embed.add_field(name=name,
                    value=severity + '' + ':octagonal_sign: ' + "(" + players + ")", inline=True)
 await ctx.send(embed=embed)


@bot.command()
async def traffic2(ctx):
 await ctx.message.delete()
 getserversURL = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim2/top.json"
 r = requests.get(getserversURL)
 data = r.json()["response"]
 embed = discord.Embed(title="TMP Traffic Status (SIM 2)",
                       url="https://traffic.krashnz.com/", color=0xFF0000)
 embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
 embed.set_footer(
     text="Bot Devloped by  StarAssassin64#9196 and " + "" + truckerbd)
 for top in data["top"]:
    id = top["id"]
    name = top["name"]
    country = top["country"]
    players = str(top["players"])
    severity = top["severity"]
    embed.add_field(name=name,
                    value=severity + '' + ':octagonal_sign: ' + "(" + players + ")", inline=True)
 await ctx.send(embed=embed)


@bot.command()
async def traffic3(ctx):
 await ctx.message.delete()
 getserversURL = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim3/top.json"
 r = requests.get(getserversURL)
 data = r.json()["response"]
 embed = discord.Embed(title="TMP Traffic Status (SIM 3)",
                       url="https://traffic.krashnz.com/", color=0xFF0000)
 embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
 embed.set_footer(
     text="Bot Devloped by  StarAssassin64#9196 and Jamesmay#0001")
 for top in data["top"]:
    id = top["id"]
    name = top["name"]
    country = top["country"]
    players = str(top["players"])
    severity = top["severity"]
    embed.add_field(name=name,
                    value=severity + '' + ':yellow_circle: : ' + "(" + players + ")", inline=True)
 await ctx.send(embed=embed)


#@bot.command()
#async def status(ctx):
 #await ctx.message.delete()
 #embed = discord.Embed(title="ALLE SERVICES STATUS", color=0xFF0000)
 #embed.add_field(name=" BOT STATUS",
 #                value=":green_square:  BOT IS ONLINE", inline=True)
 #embed.add_field(name=" CONVOY ADDING STATUS",
 #                value=":yellow_square:  CONVOY ADDING IS IN BETA", inline=True)
 #embed.add_field(name="WEB SERVER STAUS",
 #                value=":red_square: WEB SERVER IS BROKEN", inline=True)
 #embed.add_field(name="ALLE DRIVERS HUB STAUS",
 #                value=":yellow_square:  ALLE DRIVERS HUB IS BETA", inline=True)
 #embed.add_field(name="DISCORD RICH PRESENCE STAUS",
 #                value=":red_square: DISCORD RICH PRESENCE IS OFFLINE", inline=True)
 #embed.add_field(name="API STAUS",
 #                value=":yellow_square: API IS IN BETA", inline=True)
 #embed.add_field(name="JOB TRACKING STAUS",
 #value=":yellow_square: JOB TRACKING IS IN BETA", inline=True)
 #embed.add_field(name=" ADD A DRIVER STAUS",
 #                value=":green_square: ADD A DRIVER IS ONLINE", inline=True)
 #embed.add_field(name=" MYSQL DATABASE STATUS",
 #               value=":green_square: MYSQL DATABASE IS ONLINE", inline=True)
 #embed.set_footer(
 #    text="ALLE SERVICES POWERED BY ALLE API. ANY SUPPORT ISSUES PLEASE EMAIL TruckerBean@alle-group.com OR DM ME")
 #await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')


@bot.command()
@commands.has_role('''A'G | Staff''')
async def convoy(ctx, Destination, Server, Start, Meet_time, Start_time, DLC, Cars, Trailers, No_time_zone, TMP, date):
 await ctx.message.delete()
 mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="Fv4&4*JT61%8WGj&vwj",
     database="convoys"
 )
 mycursor = mydb.cursor()

 sql = "INSERT INTO convoyinfo (Destination, Server, Start, Meet_time, Start_time, DLC, Cars, Trailers, No_time_zone, TMP, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
 val = (f"{Destination}", f"{Server}", f"{Start}",
        f"{Meet_time}", f"{Start_time}", f"{DLC}", f"{Cars}", f"{Trailers}", f"{No_time_zone}", f"{TMP}", f"{date}")
 mycursor.execute(sql, val)

 mydb.commit()
 await ctx.send("new convoy added to #our-events")
 #sends the convoy info to next convoy channel
 channel1 = bot.get_channel(794886155551637534)
 embed1 = discord.Embed(title="New Convoy on" f"{date}")
 embed.add_field(name="Destination", value=f"{Destination}", inline=False)
 embed.add_field(name="Start Location", value=f"{Start}", inline=False)
 embed.add_field(name="Convoy Meet Time", value=f"{Meet_time}", inline=False)
 embed.add_field(name="Start Time", value=f"{Start_time}", inline=False)
 embed.add_field(name="DLC", value=f"{DLC}", inline=False)
 embed.add_field(name="Cars", value=f"{Cars}", inline=False)
 embed.add_field(name="Trailers", value=f"{Trailers}", inline=False)
 embed.add_field(name="No Time Zone", value=f"{No_time_zone}", inline=False)
 embed.add_field(name="TMP Event Page Link", value=f"{TMP}", inline=False)
 await channel1.send(embed=embed1)
 logchannel = bot.get_channel(794888270923300884)
 await logchannel.send(f"{ctx.author.name}#{ctx.author.discriminator} just added a convoy")

#kick command


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} has been kicked for the following reason{reason}')


#use this to ban members / users


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned for the following reason: {reason}')

#use this to unban banned members


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

# ust this to change nicknames of users. In your discord server.


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def chnick(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@bot.command()
async def statusapi(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="ERROR", color=0xFF0000)
    embed.add_field(name="REQUEST ERROR",
                    value="Failed to establish a new connectionConnection refused", inline=True)
    embed.set_footer(text="ALLE SERVICES API REFUSED THE CONNECTION")
    await ctx.send(embed=embed)
    await ctx.send("https://tenor.com/view/lifeissohard-problems-life-homer-homer-simpson-gif-13342474")


@bot.command()
async def check(ctx, nameid):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as cs:
      async with cs.get('http://51.195.223.137/users?name={nameid}') as r:
        res = await r.json()
        await ctx.send(res)


@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    await ctx.send('do u know this cat if so take it back NOW!!!')
    await ctx.send('https://media.discordapp.net/attachments/794887127086530570/803393677207535647/gnnhhnhg.png?width=485&height=595')


@bot.command()
async def job(ctx):
    embed = discord.Embed(title="JOB COMPLETE", color=0xFF0000)
    embed.add_field(name="From", value="BETA", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def helpconvoy(ctx):
    await ctx.message.delete()
    await ctx.send("`?convoy 19/01/2021 sim-3 test-location test-location test-location 7pm no yes testing testing` the command structure is like this *** date, server, origin, destination, meet, depart, cars, trailers, no time zone link, tmp events page link. *** ` YOU MUST MAKE SURE TO HAVE IT IN THAT ORDER ` *** please have `-` between words e.g no-trailers-please ***")


#remove command coming soon
@bot.command()
async def removec(ctx, *, date):
 await ctx.message.delete()
 mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="Fv4&4*JT61%8WGj&vwj",
     database="convoys"
 )
 mycursor = mydb.cursor()

 sql = f"DELETE FROM convoyinfo WHERE DATE = '{date}'"
 mycursor.execute(sql)

 mydb.commit()
#


@bot.command()
async def fire(ctx, *, name):
 await ctx.message.delete()
 mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="Fv4&4*JT61%8WGj&vwj",
     database="alle_hub"
 )
 mycursor = mydb.cursor()

 sql = f"DELETE FROM users WHERE name = '{name}'"
 mycursor.execute(sql)

 mydb.commit()


bot.run(token, bot=True)
