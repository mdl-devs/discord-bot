from dhooks import Webhook
from discord.ext.commands import CommandNotFound
from tabulate import tabulate
import discord
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
from dhooks import Webhook 
from datetime import datetime as dt

# Bots token
token = 'ODIxMzY2NDg2NDUzOTc3MTA5.YFCrJg.voB8yvcVVx0IgUtbBR7kotIk-PQ'

# Bots prefix 
bot = commands.Bot(command_prefix=('a/'))

#global variables go here (if any)


#starting off with removing the help command
bot.remove_command('help')

#staring to build the applications command 
@bot.command()
async def apply(ctx,  *, args=None):
    role = discord.utils.get(ctx.guild.roles, name="Applicant")
    await ctx.author.add_roles(role)
    await ctx.message.delete()
    await bot.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    
    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1
    category = discord.utils.get(ctx.guild.categories, name="Applications")
    ticket_channel = await ctx.guild.create_text_channel("application-{}".format(ticket_number), category=category)
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New application from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)
    await ticket_channel.send(embed=em)
    em2 = discord.Embed(title="Welcome to ALLE Groups Applications System",
                       description="To Become a driver at Alle Group we ask u submit an application. To do this, reply to this message answering in this template ```Your TMP name = _________   Your TMP ID = _____________ Your Steam ID = __________ What department are you applying for e.g Driver __________ What country are your from __________ Your age__________``` Once you have done a member of our Admissions Team will reply and take your application further. **It could take up to 1 - 2 days for a application to be viewed.**")
    await ticket_channel.send(embed=em2)
    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="Alle Group Applications", description="Your application ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
    
    await ctx.send(embed=created_em)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()
    
    day = dt.now()
    sql = "INSERT INTO  applications(discordname, applicationdate, applicationid, status, statusaddedby) VALUES (%s, %s, %s, %s, %s)"
    val = (f"{ctx.author.name}#{ctx.author.discriminator}",
           f"{day}", f"{ticket_number}", f"Sent", f"applications bot",)
    mycursor.execute(sql, val)
    mydb.commit()
    
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT applicationidapi FROM applications WHERE applicationid = '{ticket_number}';")
    myresult = cursor.fetchall()
    warningmsg = discord.Embed(title="Alle Group Applications", description=f"To see the status of your application do `a/status id` your Application ID is {myresult} .")
    await asyncio.sleep(60)
    await ticket_channel.send(embed=warningmsg)

@bot.command()
async def close(ctx, *, id):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(
                title="Alle Group Applications", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)

            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Fv4&4*JT61%8WGj&vwj",
                database="alleapi"
            )
            mycursor = mydb.cursor()
            sql = f"UPDATE applications SET status = 'closed', statusaddedby = '{ctx.author}' WHERE applicationidapi = '{id}'"
            mycursor.execute(sql)
            mydb.commit()
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Alle Group Applications", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await asyncio.sleep(60)
            await ctx.send(embed=em)
            
@bot.command()
async def hire(ctx, id, tmpid,  member: discord.Member):
  if ctx.author.guild_permissions.administrator:
    await ctx.message.delete()
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "yes"

        try:

            em = discord.Embed(
                title="Alle Group Applications", description="Are you sure you want to hire this driver? Reply with `yes` if you are sure.", color=0x00a8ff)

            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            role2 = discord.utils.get(ctx.guild.roles, name="Trainee")
            await ctx.author.remove_roles(role)
            await ctx.author.add_roles(role2)
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Fv4&4*JT61%8WGj&vwj",
                database="alleapi"
            )
            mycursor = mydb.cursor()
            sql = f"UPDATE applications SET status = 'Hired', statusaddedby = '{ctx.author}' WHERE applicationidapi = '{id}'"
            mycursor.execute(sql)
            mydb.commit()
            getinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
            r = requests.get(getinfourl)
            data = r.json()["response"]   
            cursor = mydb.cursor()
            sql = "INSERT INTO drivers (name, discordname, tmpid, steamid, role) VALUES (%s, %s, %s, %s, %s)"
            val = (data["name"], f"{member}", f"{tmpid}",
                   data["steamID64"], f"Trainee")
            cursor.execute(sql, val)
            mydb.commit()
            await member.send(f"{ctx.author} just updated your application at Alle Group to `Hired`")
            await member.send("Welcome to Alle Group Your role is `Trainee`")
            channel1 = bot.get_channel(797186729232433193)
            await channel1.send(f"Welcome to alle group {member.mention}. A member of the Examantions team will contact you to do your training.")
            hook = Webhook(
                'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
            em2 = discord.Embed(
                title=f"{member.mention} has been promoted to trainee", description="")
            hook.send(embed=em2)
            await ctx.send("Driver added to our database and to our company")
            await ctx.channel.delete()
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            role2 = discord.utils.get(ctx.guild.roles, name="Trainee")
            await ctx.member.remove_roles(role)
            await ctx.member.add_roles(role2)
            
        #this will happen if it times out after 60 secs
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Alle Group Applications", description="You have run out of time to hire this driver. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)

  else:
        errormsg = discord.Embed(
            title="Alle Group applications", description="You do not have the correct roles or perms to use the command `hire`", color=0xFF0000
        )
        await ctx.send(errormsg)          
  
@bot.command()
async def pinfo(ctx, tmpid):
    await ctx.message.delete()
    try:
     getplayerinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
     r = requests.get(getplayerinfourl)
     data = r.json()["response"]
     for server in data:
      em2 = discord.Embed(title="Player lookup (tmp)", url=f"https://truckersmp.com/user/{tmpid}", color=0x00FF00)
      em2.add_field(name="Name", value= data["name"], inline=True)
      em2.add_field(name="Tmp id", value=data["id"], inline=True)
      em2.add_field(name="Steam id", value=data["steamID64"], inline=True)
      em2.add_field(name="Banned", value=data["banned"], inline=True)
      em2.add_field(name="Banned until",
                    value=data["bannedUntil"], inline=True)
      em2.add_field(name="Bans count", value=data["bansCount"], inline=True)
     await ctx.send(embed=em2)
    except:
        em3 = discord.Embed(title="Player lookup (tmp) Error",
                            description="we could not lookup this user", color=0xFF0000)
        await ctx.send(embed=em3)                    

@bot.command()
async def claim(ctx, id):
 if ctx.author.guild_permissions.administrator:
   await ctx.message.delete()
 try: 
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="Fv4&4*JT61%8WGj&vwj",
       database="alleapi"
   )
 except:
     errormsg1 = discord.Embed(title="Alle Applications | Error", description="We could not connect to the mysql database using password `##########################################` :(", color=0xFF0000
     )
     await ctx.send(embed=errormsg1)  
 try:   
    mycursor = mydb.cursor()
    sql = f"UPDATE applications SET status = 'Claimed/inprogress', statusaddedby = '{ctx.author}' WHERE applicationidapi = '{id}'"
    mycursor.execute(sql)
    mydb.commit()
 except:
     errormsg2 = discord.Embed(title="Alle Applications | Error", description="We could not add the new record to our mysql database :("
     ) 

@bot.command()
async def status(ctx, id):
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT status FROM applications WHERE  applicationidapi = '{id}';")
    myresult = cursor.fetchall()
    em = discord.Embed(title="Your application status is",
                       description=f"{myresult}")
    await ctx.send(embed=em)                   
#black list a user from applying by there steamid (BETA)
@bot.command()
async def blacklist(ctx, steamid, tmpid=None):
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
     )
    mycursor = mydb.cursor()
    sql = "INSERT INTO  blacklistvtc(tmpid, steamid, addedby) VALUES (%s, %s, %s)"
    val = (f"{tmpid}",f"{steamid}", f"{ctx.author.name}#{ctx.author.discriminator}")
    mycursor.execute(sql, val)
    mydb.commit()
    await ctx.send(f"User Blacklisted {steamid}")
    
#check drivers / users bans
@bot.command()
async def checkb(ctx, tmpid):
      await ctx.message.delete()
      try: 
       getbaninfourl = f"https://api.truckersmp.com/v2/bans/{tmpid}"
       re = requests.get(getbaninfourl)
       data = re.json()['response']
       embed = discord.Embed(
           title=f"Ban lookup for {tmpid}", url=f"https://api.truckersmp.com/v2/bans/{tmpid}", description=f"{data}", color=0x00FF00)
       await ctx.send(embed=embed)
      except:
              em = discord.Embed(
          title=f"Ban Lookup Error", description=f"we could not look up the bans for player with id {tmpid}", color=0xFF0000
       )
              await ctx.send(embed=em)

@bot.command()
async def look(ctx, tmpid):
    await ctx.message.delete()


@bot.command()
async def reply(ctx, *, message):
     await ctx.message.delete()
     em = discord.Embed(title="", description=f"{message}")
     await ctx.send(embed=em)



@bot.command()
async def promote(ctx, role, member: discord.Member, roleid = None):
          await ctx.message.delete()
          mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password="Fv4&4*JT61%8WGj&vwj",
              database="alleapi"
             )
          mycursor = mydb.cursor()
          sql = f"UPDATE drivers SET role = '{role}' WHERE discordname = '{member}'"
          mycursor.execute(sql)
          mydb.commit()
          em = discord.Embed(title=f"Promted driver {member}", description=f"{ctx.author.mention} you promoted {member} to {role}")
          await ctx.send(embed=em)
          await member.send(f"{ctx.author.mention} just promoted you to {role}.")
          hook = Webhook(
                  'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
          em2 = discord.Embed(title=f"{member} has been promoted to {role}", description="")
          hook.send(embed=em2)
          role = f"{roleid}"
@bot.command()
async def demote(ctx, role, member: discord.Member):
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()
    sql = f"UPDATE drivers SET role = '{role}' WHERE discordname = '{member}'"
    mycursor.execute(sql)
    mydb.commit()
    em = discord.Embed(
        title=f"Demoted driver {member}", description=f"{ctx.author.mention} you demoted {member} to {role}")
    await ctx.send(embed=em)
    await member.send(f"{ctx.author.mention} just demoted you to {role}.")
    hook = Webhook(
        'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
    em2 = discord.Embed(
        title=f"{member} has been demoted to {role}", description="")
    hook.send(embed=em2)

# Fire a driver

# start the bot
bot.run(token, bot=True)
 
