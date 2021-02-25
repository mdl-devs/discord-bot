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

token = 'NzcwMzQzMjM1MjE3Nzg0ODYy.X5cMCw.stMS01QFVChvz-8OQchATM8yTKk'
bot = commands.Bot(commands.when_mentioned_or('?'))
# no longer needed game = discord.Game('Alle groups server')

truckerbd = 'spock#0001'

# a simple test message command 
@bot.command()
async def test(ctx, *, message):
    embed = discord.Embed(description=message, color=0xFF0000)
    await ctx.send(embed=embed)

#make user account for the alle hub
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

#dm users by ping
@bot.command()
async def dm(ctx, user: discord.User, *, message):
    #user = bot.get_user(755493797160288286)
    await ctx.message.delete()
    await user.send(f"{ctx.author.name}#{ctx.author.discriminator} just sent u a message contents = {message}")

#to add a new driver to the vtc
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

#dev command
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

#shows the amount of drivers in our database in the VTC
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
  embed = discord.Embed(title="Total Number of drivers", color=0xFF0000)
  embed.add_field(name="Number =", value=result, inline=False)
  #await ctx.send(tabulate(myresult, headers=['users'], tablefmt='psql'))
  await ctx.send(embed=embed)
  #results = result

  #channel = bot.get_channel(794888270923300884)
  #embed1 = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}",
  # icon_url=ctx.author.avatar_url, color=0xFF0000)
  #embed1.add_field(name="This user  just checked the amount of drivers using ",
  # value="`?drivers`", inline=False)
  #await channel.send(embed=embed1)

#on ready showing presence etc.. 
@bot.event
async def on_ready():
   
   print("My body is ready")
   await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"CONGRATS ALLE GROUP WE ARE SO PROUD OF U :)"))


#showing the member count of the vtc using the TMP api
@bot.command()
async def members(ctx):
 r = requests.get("https://api.truckersmp.com/v2/vtc/13006")
 data = r.json()
 members_count = r.json()['response']['members_count']
 await ctx.send(f'The amount of drivers and staff in this vtc is {members_count}')



#server ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')

#status command for devs only
@bot.command()
async def statusapi(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="ERROR", color=0xFF0000)
    embed.add_field(name="REQUEST ERROR",
                    value="Failed to establish a new connectionConnection refused", inline=True)
    embed.set_footer(text="ALLE SERVICES API REFUSED THE CONNECTION")
    await ctx.send(embed=embed)
    await ctx.send("https://tenor.com/view/lifeissohard-problems-life-homer-homer-simpson-gif-13342474")

#check if a driver is on the API (currently not working)
@bot.command()
async def check(ctx, nameid):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as cs:
      async with cs.get('http://51.195.223.137/users?name={nameid}') as r:
        res = await r.json()
        await ctx.send(res)

#to fire users and drivers **(working) **
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

#removing of the help command
bot.remove_command('help')

#simple help command
@bot.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Most Common Commands are listed below", color=0xFF0000)
    embed.add_field(
        name="?add", value="This command is locked for HR to add new drivers to our Databases", inline=True)
    embed.add_field(
        name="?ping", value="This command allows users to check the bots ping to and from the server", inline=True)
    embed.add_field(
        name="?members", value="This command uses the TMP api to display the number of drivers in our vtc at one time", inline=True)
    embed.add_field(
        name="?fire", value="This command is locked for HR and is used to kick people out of the VTC", inline=True)
    embed.add_field(
        name="?check", value="This command uses our own alle api to allow users to check if they are in our vtc or not (OUT OF USE)", inline=True)
    embed.add_field(
        name="?dm", value="This command allows u to message other people using the bot. This atm is not locked to a role but if missused it will be.", inline=True)
    embed.add_field(
        name="?dev1", value="This command is for devs only (OUT OF USE)", inline=True)
    await ctx.send(embed=embed)

#simple status command giving a link to the alle groups status page
@bot.command()
async def status(self, ctx):
    await ctx.send("Visit our status page to see our systems status https://allegroup.statuspage.io/")


#uses the token to run the bot
bot.run(token, bot=True)
