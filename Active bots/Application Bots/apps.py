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
import time
from datetime import datetime
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
    applied_times = 0
    rate_limit_for_applications = 5
    time_to_wait_to_avoid_rate_limit = 60
    role = discord.utils.get(ctx.guild.roles, name="Applicant")
    await ctx.author.add_roles(role)
    await ctx.message.delete()
    await bot.wait_until_ready()
    applied_times += 1
    if applied_times % rate_limit_for_applications == 0:  # used to check if 30 dms are sent
        # wait till we can continue
        asyncio.sleep(time_to_wait_to_avoid_rate_limit)
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

    em = discord.Embed(title="New application from {}#{}".format(
        ctx.author.name, ctx.author.discriminator), description="{}".format(message_content), color=0x00a8ff)
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

    created_em = discord.Embed(title="Alle Group Applications", description="Your application ticket has been created at {}".format(
        ticket_channel.mention), color=0x00a8ff)
    hook = Webhook(
        'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
    userapplyed = discord.Embed(title="Alle Group Applications",
                                description=f"{ctx.author.mention} Has applied.  Channel name:{ticket_channel.mention}")
    hook.send(embed=userapplyed)
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
        f"SELECT id FROM applications WHERE applicationid = '{ticket_number}';")
    myresult = cursor.fetchall()
    warningmsg = discord.Embed(title="Alle Group Applications",
                               description=f"To see the status of your application do `a/status id` your Application ID is {myresult} .")
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
            sql = f"UPDATE applications SET status = 'Closed', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
            mycursor.execute(sql)
            mydb.commit()
            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            userapplyed = discord.Embed(title="Alle Group Applications",
                                        description=f"Updated Mysql applications to 'closed'.")
            hook.send(embed=userapplyed)
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            await ctx.author.remove_roles(role)
            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            now = datetime.now()
            userapplyed = discord.Embed(title="Alle Group Applications",
                                        description=f"{ctx.author.mention} Has closed Application {id} @ {now}")
            hook.send(embed=userapplyed)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Alle Group Applications", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await asyncio.sleep(60)
            await ctx.send(embed=em)


@bot.command()
async def hire(ctx, id, tmpid,  member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, id=794865611956158484)
  if role in ctx.author.roles:
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()
    sql = f"UPDATE applications SET status = 'Hired', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
    mycursor.execute(sql)
    mydb.commit()
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
            await member.remove_roles(role)
            await member.add_roles(role2)

            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            info1 = discord.Embed(title="Alle Group Applications",
                                        description=f"Updated **mysql** table `applications` SET status of application {id} to `hired`")
            hook.send(embed=info1)
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
            userapplyed = discord.Embed(title="Alle Group Applications",
                                        description=f"{ctx.author.mention} Hired {member.mention}")
            hook.send(embed=userapplyed)
            await ctx.send("Driver added to our database and to our company")
            await ctx.channel.delete()

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
      em2 = discord.Embed(title="Player lookup (tmp)",
                          url=f"https://truckersmp.com/user/{tmpid}", color=0x00FF00)
      em2.set_thumbnail(
          url=data["avatar"])
      em2.add_field(name="Name", value=data["name"], inline=True)
      em2.add_field(name="Tmp id", value=data["id"], inline=True)
      em2.add_field(name="Steam id", value=data["steamID64"], inline=True)
      em2.add_field(name="Banned", value=data["banned"], inline=True)
      em2.add_field(name="Banned until",
                    value=data["bannedUntil"], inline=True)
      em2.add_field(name="Bans count", value=data["bansCount"], inline=True)
      em2.add_field(name="Join Date", value=data["joinDate"], inline=True)
      em2.add_field(name="Discord User ID",
                    value=data["discordSnowflake"], inline=True)
     await ctx.send(embed=em2)
    except:
        em3 = discord.Embed(title="Player lookup (tmp) Error",
                            description="we could not lookup this user", color=0xFF0000)
        await ctx.send(embed=em3)


@bot.command()
async def claim(ctx, id):
 role = discord.utils.get(ctx.guild.roles, id=794865611956158484)
 if role in ctx.author.roles:
   await ctx.message.delete()
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="Fv4&4*JT61%8WGj&vwj",
       database="alleapi"
   )

   mycursor = mydb.cursor()
   sql = f"UPDATE applications SET status = 'Claimed/inprogress', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
   mycursor.execute(sql)
   mydb.commit()
   getapplicationinfourl = f"http://51.195.223.137/api/v2/applications/{id}"
   em2 = discord.Embed(description=f"{ctx.author.mention} just claimed application id {id}",
                       url=f"http://51.195.223.137/api/v2/applications/{id}")
   await ctx.send(embed=em2)

#command to request training.


@bot.command()
async def request(ctx, date, time, *, message):
    await ctx.message.delete()
    day = dt.now()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"SELECT COUNT(discordname) FROM applications WHERE discordname = '{ctx.author}'")
    result = mycursor.fetchall()
    hook = Webhook(
        'https://discord.com/api/webhooks/825657922703982622/frltOXWR9Di-VYeNelDDHoLiO3sqcO7o6FgxHWt68MTzL3wZpQOrxlqRuNe0IU9LY-CO')
    em2 = discord.Embed(title=f"New training request.", color=0x00FF00)
    em2.add_field(
        name="User", value=f"{ctx.author.name}#{ctx.author.discriminator}")
    em2.add_field(name="Requested Date", value=f"{date}", inline=True)
    em2.add_field(name="Requested Time", value=f"{time}", inline=True)
    em2.add_field(name="Message", value=f"{message}", inline=False)
    em2.add_field(name="Request date and time", value=f"{day}", inline=True)
    em2.add_field(name="Number of applications from user",
                  value=f"{result}", inline=False)
    hook.send(embed=em2)
    await ctx.send("Your Training request has been sent to the admissions team.")


@bot.command()
async def confirm(ctx, tmpid, status, videourl=None, *, notes):
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    getplayerinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
    r = requests.get(getplayerinfourl)
    data = r.json()["response"]
    for server in data:
     mycursor = mydb.cursor()
     sql = "INSERT INTO trainings(tmpid, steamid, trainedby, videoevidence, traineename, notes, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
     val = (f"{tmpid}", data["steamID64"], f"{ctx.author}",
            f"{videourl}", data["name"], f"{notes}", f"{status}")
    mycursor.execute(sql, val)
    mydb.commit()
    hook = Webhook(
        'https://discord.com/api/webhooks/825683286428483594/nQbl4rw8fBcD_Q1Ig9ceNgUsHy9lQ-EOtTwCCyYTges0W8J2OIPVpXNQl6rLCWrj4JhF')
    em2 = discord.Embed(
        title=data["name"], description=f"You have {status} your training", color=0x00FF00)
    hook.send(embed=em2)


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
        f"SELECT status FROM applications WHERE  id = '{id}';")
    myresult = cursor.fetchall()
    em = discord.Embed(title="Your application status is", url=f"http://51.195.223.137/api/v2/applications/{id}",
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
    val = (f"{tmpid}", f"{steamid}",
           f"{ctx.author.name}#{ctx.author.discriminator}")
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
async def promote(ctx, roled,  member: discord.Member, roleid=None):
       role = discord.utils.get(ctx.guild.roles, id=794865611956158484)
       if role in ctx.author.roles:
          await ctx.message.delete()
          mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password="Fv4&4*JT61%8WGj&vwj",
              database="alleapi"
          )
          mycursor = mydb.cursor()
          sql = f"UPDATE applications SET status = '{roled}' WHERE discordname = '{member}'"
          mycursor.execute(sql)
          mydb.commit()
          em = discord.Embed(
              title=f"Promoted driver {member}", description=f"{ctx.author.mention} you promoted {member} to {roled}")
          await ctx.send(embed=em)
          await member.send(f"{ctx.author.mention} just promoted you to {roled}.")
          hook = Webhook(
              'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
          em2 = discord.Embed(
              title=f"{member.mention} has been promoted to {roled}", description="")
          hook.send(embed=em2)
          role = f"{roleid}"
          await member.add_roles(role)


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


@bot.command(case_insensitive=True, aliases=["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files=True, embed_links=True)
async def reminder(ctx, member: discord.Member, time, *, reminder):
    await ctx.message.delete()
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(text="Alle Group training reminding system credit: truckerbean",
                     icon_url=f"{bot.user.avatar_url}")
    seconds = 0
    if reminder is None:
        # Error message
        embed.add_field(
            name='Warning', value='Please specify what do you want me to remind you about.')
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(
            name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}. **It will be sent in a dm to you :)**")
        await asyncio.sleep(seconds)
        await ctx.author.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        await member.send(f"Hey, {ctx.author.mention} has sent you a reminder that {reminder} will happen in {counter}")
        return
    await ctx.send(embed=embed)


@bot.command()
async def convert(ctx, hours):
    await ctx.message.delete()
    hours = int(f"{hours}")
    minutes = hours * 60
    embed = discord.Embed(color=0x55a7f7)
    embed.add_field(name='Time conversation system Alle Group',
                    value=f"Your conversation from **{hours}hrs** to **{minutes}mins** credit: Truckerbean")
    await ctx.send("Look in your dms :)")
    await ctx.author.send(embed=embed)


@bot.command()
async def convertd(ctx, ):
    await ctx.message.delete()
    embed = discord.Embed(color=0x55a7f7)
    embed.add_field(name='Time conversation system Alle Group',
                    value=f"credit: Truckerbean", inline=False)
    embed.add_field(name='1 day',
                    value=f"24 hours", inline=False)
    embed.add_field(name='2 days',
                    value=f"48 hours", inline=False)
    embed.add_field(name='3 days',
                    value=f"72 hours", inline=False)
    embed.add_field(name='4 days',
                    value=f"96 hours", inline=False)
    embed.add_field(name='5 days',
                    value=f"120 hours", inline=False)
    embed.add_field(name='10 days',
                    value=f"240 hours", inline=False)
    await ctx.send("Look in your dms :)")
    await ctx.author.send(embed=embed)
# Fire a driver

##removed due to not working
#@bot.event
#async def on_message(message):
 #   id = bot.get_guild(688060261470568567)

  #  if message.content.find("hello") != -1:
   #     await message.channel.send(f"Hi {message.author.mention}")
   # elif message.content == "!users":
  # #     await message.channel.send(f"""# of Members: {id.member_count}""")
   # elif message.content == "trucker bean":
   #     await message.channel.send(f"""bean is a nub""")
   # elif message.content == "antonio":
   #     await message.channel.send(f"""Disco Truck time""")
  #  elif message.content == "star":
 #       await message.channel.send(f"""Hey <@344999742847320064>, someone is talking about you""")
#

#@bot.event
#async def on_message(message):
 # if message == "StarAssassin" or "starassassin" or "star":
  #  await bot.send_message(message.channel, "Hey <@344999742847320064>, someone is talking about you")


@bot.command()
async def apinfo(ctx, tmpid):
    await ctx.message.delete()
    try:
     getplayerinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
     r = requests.get(getplayerinfourl)
     data = r.json()["response"]
     for server in data:
      em2 = discord.Embed(title="Player lookup (tmp)",
                          url=f"https://truckersmp.com/user/{tmpid}", color=0x00FF00)
      em2.set_thumbnail(
          url=data["avatar"])
      em2.add_field(name="Name", value=data["name"], inline=True)
      em2.add_field(name="Tmp id", value=data["id"], inline=True)
      em2.add_field(name="Steam id", value=data["steamID64"], inline=True)
      em2.add_field(name="Banned", value=data["banned"], inline=True)
      em2.add_field(name="Banned until",
                    value=data["bannedUntil"], inline=True)
      em2.add_field(name="Bans count", value=data["bansCount"], inline=True)
      em2.add_field(name="Join Date", value=data["joinDate"], inline=True)
      em2.add_field(name="Discord User ID",
                    value=data["discordSnowflake"], inline=True)
      em2.add_field(name="Game Admin?",
                    value=data["permissions"]["isGameAdmin"], inline=True)
      em2.add_field(name="Tmp Staff?",
                    value=data["permissions"]["isStaff"], inline=True)
      em2.add_field(name="Tmp Upper Staff?",
                    value=data["permissions"]["isUpperStaff"], inline=True)
      em2.add_field(name="In a Vtc?",
                    value=data["vtc"]["inVTC"], inline=True)
      # find ID by right clicking on server icon and choosing "copy id" at the bottom
      guild = bot.get_guild(688060261470568567)
    # find ID by right clicking on a user and choosing "copy id" at the bottom
      if guild.get_member(755493797160288286)is not None:
        em2.add_field(name="In Discord server?",
                      value="Yes", inline=True)
      else:
          em2.add_field(name="In Discord server?",
                        value="No", inline=True)
     await ctx.send(embed=em2)

    except:
        em3 = discord.Embed(title="Player lookup (tmp) Error",
                            description="we could not lookup this user", color=0xFF0000)
        await ctx.send(embed=em3)
# start the bot
bot.run(token, bot=True)
