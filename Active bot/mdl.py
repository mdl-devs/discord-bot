import os
from discord import Spotify
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
from discord_slash import SlashCommand, SlashContext
from discord.ext.commands import cooldown, BucketType
import pytz
import functools
import itertools
import youtube_dl
from async_timeout import timeout
import math
import random
from discord.utils import get
import string

intents = intents = discord.Intents.all()


# Bots token
token = 'ODM3ODAwNjk4MDY2MTA4NDM2.YIx0tA.QbeQPybTciQBMh69wiTmrUl9KhQ'

# Bots prefix
bot = commands.Bot(commands.when_mentioned_or('m/'), intents=intents)
slash = SlashCommand(bot)



#global variables go here (if any)
userid = 0
eventid = 0
bug_id = 12

timestamp67 = datetime.now(pytz.timezone("Europe/London"))
timestamp68 = datetime.now(pytz.timezone("Europe/London"))
time_main = timestamp67.strftime(r"On: %d/%m/%Y At: %H:%M %p")
time_main2 = timestamp68.strftime(r"%H:%M %p")
time_main3 = timestamp67.strftime(r"%d/%m/%Y")
# when a user boosts the server


tracked_users = []


@bot.event
async def on_member_update(before, after):
    if before.premium_since is None and after.premium_since is not None:
        await on_nitro_boost(after)

# sending startup message to server


@bot.event
async def on_ready():
    global command_prefix
    activity = discord.Game(
        name=f"Bean ❤️", type=3)
    await bot.change_presence(status="Test", activity=activity)


#send a dm to every user new user and creates new user profile  in there name
@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(855864762504052767)
    welcome_em = discord.Embed(
        description=f"{member.mention} {member}", icon_url=f"{member.avatar_url}", color=0x00993C)
    welcome_em.set_author(name="User Joined | Welcome",
                          icon_url=f"{member.avatar_url}")
    welcome_em.set_footer(text=f"ID: {member.id} â€¢ {time_main3}")
    await welcome_channel.send(embed=welcome_em)

    bot_commands_channel = bot.get_channel(855590931767099452)
    await member.send(f'Welcome to Moondog Logistics | If you would like to join our vtc do `m/apply` in {bot_commands_channel.mention}')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="userprofiles"
    )
    cursor = mydb.cursor()
    joindate = member.joined_at.strftime("%b/%d/%Y")
    jointime = member.joined_at.strftime(" %I:%M %p")
    sql = f"INSERT INTO  userprofiles (id, join_date, join_time, discord_name) VALUES (%s, %s, %s, %s)"
    global userid
    userid += 1

    val = (f"{userid}",
           f"{joindate}", f"{jointime}", f"{member.name}")
    cursor.execute(sql, val)
    mydb.commit()
    com_member_role = discord.utils.get(
        welcome_channel.guild.roles, id=837609123755327508)
    await member.add_roles(com_member_role)


@bot.event
async def on_member_remove(member):
    leaving_channel = bot.get_channel(855864778933272576)
    global time_main3
    welcome_em = discord.Embed(
        description=f"{member.mention} {member}", icon_url=f"{member.avatar_url}", color=0x00993C)
    welcome_em.add_field(name="Roles", value=f"")
    welcome_em.set_author(name="User Left | Goodbye :wave:",
                          icon_url=f"{member.avatar_url}")
    welcome_em.set_footer(text=f"ID: {member.id} At: {time_main3}")
    await leaving_channel.send(embed=welcome_em)


#starting off with removing the help command
bot.remove_command('help')


# ping command


@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')


@ping.error
async def apply_handler(ctx, error):
    pingerr = discord.Embed(title="Ping command error",
                            description=f"{error}", color=0xFF0000)
    await ctx.send(embed=pingerr)


# @bot.command()
# async def joinvtc(ctx):
#      await ctx.message.delete()
#       mydb = mysql.connector.connect(
#            host="localhost",
#            user="root",
#            password="Fv4&4*JT61%8WGj&vwj",
#            database="userprofiles"
#            )
#       mycursor = mydb.cursor()
#       mycursor.execute(
#             f"SELECT  discord_name  FROM userprofiles WHERE discord_name  = '{ctx.author.name}'")
#       results = mycursor.fetchall()
#         # gets the number of rows affected by the command executed
#       row_count = mycursor.rowcount
#       if ctx.author.name == 'PDragon_7':
#             await ctx.send("ITS PD!!!!, Hey PD")
#             joined_server = ctx.author.joined_at.strftime("%d/%b/%Y")
#             joined_server_time = ctx.author.joined_at.strftime("%I:%M %p")
#             sql = "INSERT INTO  userprofiles (id, join_date, join_time, discord_name,  have_they_applied, applied_date, applied_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#             val = (f"{userid}",
#                    f"{joined_server}", f"{joined_server_time}", f"{ctx.author.name}",  f"Yes", "N/A", "N/A")
#             mycursor.execute(sql, val)
#             mydb.commit()
#             await ctx.send(f"{ctx.author.mention} Your Basic Driver Profile Has Been Made :clap:")
#         else:
#             print("not PD")
#         if row_count > 0:
#            Member_already_blacklisted = discord.Embed(
#                title="Moondog Logistics Applications | `join` error", description=f"Hey {ctx.author.mention} you have already made an account please dont make another.. DiscordID: {ctx.author.id}", color=0xFF0000)
#            await ctx.send(embed=Member_already_blacklisted)
#         else:

#          joined_server = ctx.author.joined_at.strftime("%d/%b/%Y")
#          joined_server_time = ctx.author.joined_at.strftime("%I:%M %p")
#          sql = "INSERT INTO  userprofiles (id, join_date, join_time, discord_name,  have_they_applied, applied_date, applied_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#          val = (f"{userid}",
#                 f"{joined_server}", f"{joined_server_time}", f"{ctx.author.name}",  f"Yes", "N/A", "N/A")
#          mycursor.execute(sql, val)
#          mydb.commit()
#          await ctx.send(f"{ctx.author.mention} Your Basic Driver Profile Has Been Made :clap:")

#Apply Command (allows users to apply to join the vtc.)


@bot.command()
# cool down of 4 mins to counter spamming
@commands.cooldown(1, 240, commands.BucketType.user)
async def apply(ctx, *, args=None):
    applied_times = 0
    rate_limit_for_applications = 5
    time_to_wait_to_avoid_rate_limit = 60
    role = discord.utils.get(ctx.guild.roles, name="Applicant")
    await ctx.author.add_roles(role)
    await ctx.message.delete()
    await bot.wait_until_ready()
    applied_times += 1
    if args == None:
        message_content = "Please wait, we will be with you shortly!"

    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)
    ticket_number = int(data["ticket-counter"])
    ticket_number += 1
    category = discord.utils.get(
        ctx.guild.categories, name="| ðŽðŸðŸð¢ðœðž ð”ð¬ðž")
    ticket_channel = await ctx.guild.create_text_channel("application-{}".format(ticket_number), category=category)
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New application from {}#{}".format(
        ctx.author.name, ctx.author.discriminator), description="{}".format(message_content), color=0x00a8ff)
    await ticket_channel.send(embed=em)
    em2 = discord.Embed(title="Welcome to Monndog Logistics Applications System",
                        description="To Become a driver at Moondog Logistics we ask u submit an application. To do this, reply to all the messages the bot will send you one at a time **It could take up to 1 - 2 days for a application to be viewed.**")
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

    created_em = discord.Embed(title="Moondog Logistics Applications", description="Your application ticket has been created at {}".format(
        ticket_channel.mention), color=0x00a8ff)
    hook = Webhook(
        'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
    userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                description=f"{ctx.author.mention} Has applied.  Channel name:{ticket_channel.mention}")
    hook.send(embed=userapplyed)
    await ctx.send(embed=created_em)

    # checks to see if the user is a Diretor if they are then they will not be allowed to apply
    Diretor_role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
    if Diretor_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role = discord.Embed(
            title="Moondog Logistics Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `director role` so you dont need to apply.", color=0xFF0000)
        global time_main2
        Member_has_too_high_role.set_footer(
            text=f"Moondog Logistics Applications | Apply Error Message â€¢ {time_main2}")
        await ctx.author.send(embed=Member_has_too_high_role)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel3 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_1 = discord.Embed(
            ttitle="Moondog Logistics Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Director`**", color=0xFF0000)
        staff_log_messageing_1.set_footer(
            text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
        await channel3.send(embed=staff_log_messageing_1)

    # checks to see if the user is already a driver and then they dont need to apply / cant apply. If they are abusing the system then it will flag to the staff team.
    Drivers_role = discord.utils.get(ctx.guild.roles, id=837666217413967882)
    if Drivers_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role_2 = discord.Embed(
            title="Moondog Logistics Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `drivers role` so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role_2.set_footer(
            text=f"Moondog Logistics Applications | Apply Error Message â€¢ {time_main2}")
        await ctx.author.send(embed=Member_has_too_high_role_2)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel2 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_2 = discord.Embed(
            title="Moondog Logistics Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Driver`**", color=0xFF0000)
        staff_log_messageing_1.set_footer(
            text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
        await channel2.send(embed=staff_log_messageing_2)

    # checks to see if the user is a member of lower staff, however they should have the above role anyway :)
    lower_staff_role = discord.utils.get(
        ctx.guild.roles, id=837606669830848523)
    if lower_staff_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role_3 = discord.Embed(
            title="Moondog Logistics Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `lower staff` role so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role_3.set_footer(
            text=f"Moondog Logistics Applications | Apply Error Message â€¢ {time_main2}")
        await ctx.author.send(embed=Member_has_too_high_role_3)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel1 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_3 = discord.Embed(
            title="Moondog Logistics Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Staff Team`**", color=0xFF0000)
        staff_log_messageing_3.set_footer(
            text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
        await channel1.send(embed=staff_log_messageing_3)

    await asyncio.sleep(20)

    def check(message):
        return message.author == ctx.author and message.channel == ticket_channel
    await ticket_channel.send(f"{ctx.author.mention}")
    try:
     question1_em = discord.Embed(
         title="Moondog Logistics Applications | Question 1 ", description=f"Hey, {ctx.author.name} what is your name?", color=0xFF0000)
     question1_em.set_footer(
         text=f"Moondog Logistics Applications | Question 1 â€¢ {time_main2}")
     remove1 = await ticket_channel.send(embed=question1_em)
     msg = await bot.wait_for('message', check=check, timeout=3600)
     response = (msg.content)
    except asyncio.TimeoutError:
        em = discord.Embed(
             title="Moondog Logistics Applications", description=f"Hey {ctx.author.name}, are you there? You opened up a application @ Moondog Logistics and have not answered any of the questions after 1hr.", color=0x00a8ff)
        await asyncio.sleep(3600)
        await ctx.author.send(embed=em)
        try:
             question1_em = discord.Embed(
                 title="Moondog Logistics Applications | Question 1 ", description=f"Hey, {ctx.author.name} what is your name?", color=0xFF0000)
             question1_em.set_footer(
                 text=f"Moondog Logistics Applications | Question 1 â€¢ {time_main2}")
             remove1 = await ticket_channel.send(embed=question1_em)
             msg = await bot.wait_for('message', check=check, timeout=7200)
             response = (msg.content)
        except:
                em2 = discord.Embed(
                    title="Moondog Logistics Applications", description=f"Hey {ctx.author.name}, Your application with Moondog Logistics will be closed in 5 mins as you have not responded to any of the questions in 2hrs", color=0x00a8ff)
                await asyncio.sleep(3600)
                await ctx.author.send(embed=em2)
                await asyncio.sleep(300)
                await ticket_channel.delete()
                await ctx.author.send(f"{ctx.author.name} Your Application Has been closed.")
                role = discord.utils.get(
                      ctx.guild.roles, id=837608034721071104)
                await ctx.author.remove_roles(role)
                index = data["ticket-channel-ids"].index(ticket_channel.id)
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
    question2_em = discord.Embed(
        title="Moondog Logistics Applications | Question 2 ", description=f"Hey, {ctx.author.name} what is your TMPID?", color=0xFF0000)
    question2_em.set_footer(
        text=f"Moondog Logistics Applications | Question 2 â€¢ {time_main2}")
    remove2 = await ticket_channel.send(embed=question2_em)
    msg2 = await bot.wait_for('message', check=check)
    response2 = (msg2.content)
    # question 3 removed due to no longer being needed
    question3_em = discord.Embed(
        title="Moondog Logistics Applications | Question 3 ", description=f"Hey, {ctx.author.name} what country are you from?", color=0xFF0000)
    question3_em.set_footer(
        text=f"Moondog Logistics Applications | Question 3 â€¢ {time_main2}")
    remove3 = await ticket_channel.send(embed=question3_em)
    msg4 = await bot.wait_for('message', check=check)
    response4 = (msg4.content)
    question4_em = discord.Embed(
        title="Moondog Logistics Applications | Question 4 ", description=f"Hey, {ctx.author.name} what is your age?", color=0xFF0000)
    question4_em.set_footer(
        text=f"Moondog Logistics Applications | Question 4 â€¢ {time_main2}")
    remove4 = await ticket_channel.send(embed=question4_em)
    msg5 = await bot.wait_for('message', check=check)
    response5 = (msg5.content)

    #checks if they are older then
    #if msg5.content < 16:
    #your_not_old_enough = discord.Embed(
    #  title="Moondog Logistics Applications | Age Check ", description=f"Hey, {ctx.author.name} your application has been **`Automatically Denied`** as you are under the age of 16.", color=0xFF0000)
    #your_not_old_enough.set_footer(
    #text="Moondog Logistics Applications | Age Check â€¢ 2021")
    #await ctx.author.send(embed=your_not_old_enough)
    #   await ticket_channel.delete()
    #role = discord.utils.get(ctx.guild.roles, id=837608034721071104)
    #await ctx.author.remove_roles(role)
    #index = data["ticket-channel-ids"].index(ticket_channel.id)
    #del data["ticket-channel-ids"][index]
    #with open('data.json', 'w') as f:
    #json.dump(data, f)
    #mydb = mysql.connector.connect(
    #host="localhost",
    # user="root",
    #   password="Fv4&4*JT61%8WGj&vwj",
    #  database="alleapi"
    #)
    #mycursor = mydb.cursor()
    #sql = f"UPDATE applications SET status = 'Closed / Under Age', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
    #mycursor.execute(sql)
    #mydb.commit()
    timestamp = datetime.now(pytz.timezone("Europe/London"))
    
    Diretor_role2 = discord.utils.get(ctx.guild.roles, id=837606126795227136)
    await ticket_channel.send(f"{Diretor_role2.mention} New application finshed. The answers are below!!")
    thanks_for_answering_alle_questions = discord.Embed(title="Moondog Logistics Applications | Your Application Has Been Recived.",
                                                        description=f"Hey {ctx.author.name}, Thanks for answering all the questions a member of staff will now deal with your application. **Please remember it can take up to 2 days for your application to be viewed.**", color=0xFF0000)
    thanks_for_answering_alle_questions.set_footer(
        text=f"Moondog Logistics Applications | Applications System â€¢ {time_main2}")
    await ctx.author.send(embed=thanks_for_answering_alle_questions)
    questionr = discord.Embed(title="Moondog Logistics Applications | Answers To Application Questions",
                              description=f"Here are the answers to the application questions:", color=0xFF0000)
    questionr.add_field(name="Name", value=f"{response}", inline=True)
    questionr.add_field(name="TMPID", value=f"{response2}", inline=True)
    questionr.add_field(name="Country", value=f"{response4}", inline=True)
    questionr.add_field(name="Age", value=f"{response5}", inline=True)
    questionr.add_field(name="Applicant's Discord:",
                        value=f"{ctx.author}", inline=True)
    questionr.add_field(name="Application Submitted:", value=timestamp.strftime(
        r"On: %d/%m/%Y At: %I:%M %p"), inline=True)
    questionr.set_footer(
        text=f"Moondog Logistics Applications | Applications System â€¢ {time_main2}")
    await ticket_channel.send(embed=questionr)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()

    day = dt.now()
    sql = "INSERT INTO  applications(discordname, applicationdate, applicationid, status, statusaddedby, tmpid) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (f"{ctx.author.name}#{ctx.author.discriminator}",
           f"{day}", f"{ticket_number}", f"Sent", f"applications bot", f"{response2}")
    mycursor.execute(sql, val)
    mydb.commit()
    await remove1.delete()
    await remove2.delete()
    await remove3.delete()
    await remove4.delete()

    await msg.delete()
    await msg2.delete()
    await msg4.delete()
    await msg5.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT  discordid FROM blacklist WHERE discordid = '{ctx.author.id}'")
    results = cursor.fetchall()
    # gets the number of rows affected by the command executed
    row_count = cursor.rowcount
    if row_count > 0:
        Member_already_blacklisted = discord.Embed(
            title="Moondog Logistics Applications | `blacklist` error", description=f"That person is already blacklisted. DiscordID: {ctx.author.id}", color=0xFF0000)
        await ticket_channel.send(embed=Member_already_blacklisted)
        you_are_blacklisted = discord.Embed(
            title="Moondog Logistics Applications | Blacklist System", description=f"Your application with Moondog Logistics has been **Automatically Denied** because  you are **blacklisted** from applying. If you attempt to evade this then you will be banned.", color=0xFF0000)
        you_are_blacklisted.set_footer(
            text=f"Moondog Logistics Applications | Blacklist System â€¢ {time_main2}")
        await ctx.author.send(embed=you_are_blacklisted)

        await ticket_channel.delete()
        role = discord.utils.get(ctx.guild.roles, id=837608034721071104)
        await ctx.author.remove_roles(role)
        index = data["ticket-channel-ids"].index(ticket_channel.id)
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

    try:
     getplayerinfourl = f"https://api.truckersmp.com/v2/player/{response2}"
     r = requests.get(getplayerinfourl)
     data = r.json()["response"]
     hook = Webhook(
         'https://discord.com/api/webhooks/843949554738135091/gFJX3o2BTLPK2758j0G3t-ZtNDL8Yx4Md_S05ImrW6sBCIQrB-WuOo-L3zUUInpRQY3V')
     for server in data:
      em2 = discord.Embed(title="Player lookup (tmp)",
                          url=f"https://truckersmp.com/user/{response2}", color=0x00FF00)
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
      em2.add_field(name="Applicants Discord Name And ID",
                    value=f"{ctx.author.name} & {ctx.author.id}")
     hook.send(embed=em2)
     in_a_vtc_check = (data["vtc"]["inVTC"])
     if in_a_vtc_check == True:
        in_a_vtc_true = discord.Embed(title="Moondog Logistics Applications| Application System",
                                      description=f"Hey {ctx.author.name}, Your already in a vtc. We dont allow dual vtcing. If you wish to join Moondog Logistics please leave this vtc and then we can carry on with your application. You will have 1hr to do this. Then your application channel will be Automatically closed after the bot checks for one more time.", color=0xFF0000)
        in_a_vtc_true.set_footer(
            text="Moondog Logistics Applications| Application System")
        await ctx.author.send(embed=in_a_vtc_true)

        this_user_is_in_a_vtc = discord.Embed(title="Moondog Logistics Applications| Application System",
                                              description=f"Hey Moondog, the user {ctx.author.name} is already in vtc. They have been given 1hr to leave.", color=0xFF0000)
        this_user_is_in_a_vtc.set_footer(
            text="Moondog Logistics Applications| Application System")
        await hook.send(embed=this_user_is_in_a_vtc)
        channel = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        await ticket_channel.send(f"Hey staff member please make sure to check this channel {channel.mention}")

     banned = (data["banned"])
     if banned == False:
        bannedem = discord.Embed(
            title=f":green_circle: {ctx.author} is **not** currently  banned. :green_circle: ", color=0x00FF00)
        hook.send(embed=bannedem)
     else:
        bannedem = discord.Embed(
            title=f":warning: {ctx.author} is currently banned. Until:" + data["bannedUntil"] + ":warning:", color=0x00FF00)
        hook.send(embed=bannedem)
     if banned > 2 and banned < 5:
        banned4 = f"{ctx.author.mention} HAS MORE THEN 2 BANS BUT IS LESS THEN 5"
        hook.send(banned4)
     else:
        banned5 = f"{ctx.author.mention} HAS LESS THEN 2 BANS"
        hook.send(banned5)
     if banned == 5:
        hook3 = webhook(
            'https://discord.com/api/webhooks/843949554738135091/gFJX3o2BTLPK2758j0G3t-ZtNDL8Yx4Md_S05ImrW6sBCIQrB-WuOo-L3zUUInpRQY3V'
        )
        em34 = discord.Embed(title=f":warning: DRIVER IS PERM BANNED :warning:", description=f"Someone has tired to apply when they are perm banned on TMP this was dected by Moondogs auto ban detection system. Drivers info TMP Name:" +
                             data["name"] + "" f"Discord Name and ID: {ctx.author} {ctx.author.id}" + "" + "TMP ID:" + "" + data["id"])
        hook3.send(embed=em34)
        await ctx.channel.delete()
        role = discord.utils.get(ctx.guild.roles, name="Applicant")
        await ctx.author.remove_roles(role)
        index = data["ticket-channel-ids"].index(ticket_channel.id)
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
        hook1 = Webhook(
            'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
        userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                    description=f"Updated Mysql applications to 'closed'.")
        hook1.send(embed=userapplyed)
        hook1.send(
            f"{ticket_channel.mention} has been removed as the user had 5 bans.")
        ctx.author.send("Your application with Moondog Logistics has been canceled. Reason: `5 bans or more` **This is a auto system action if this is wrong please contact a member of the upper staff team**")
        # Checks if user is already blacklisted (checks by discordID)

     else:
         pass
         print("channel not removed")

    except:
        em3 = discord.Embed(title="Player lookup (tmp) Error",
                            description="we could not lookup this user", color=0xFF0000)
        hook.send(embed=em3)
        error34 = discord.Embed(title="Moondog Logistics Applications",
                                description=f"The TMPID you gave does not seem to exist  TMPID = {response2}")
        await ticket_channel.send(embed=error34)

    warningmsg = discord.Embed(title="Moondog Logistics Applications",
                               description=f"To see the status of your application do `a/status id` your Application ID is {ticket_number}")
    await asyncio.sleep(60)
    await ticket_channel.send(embed=warningmsg)


@apply.error
async def apply_handler_command_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}")
        global time_main2
        # sends error if the command has not be used in a application ticket channel.
        apply_on_cooldown = discord.Embed(title="Moondog Logistics Applications | `apply` error",
                                          description=f"Im sorry but at this time this command is on a cooldown please try again in {error.retry_after:.2f}s", color=0xFF0000)
        apply_on_cooldown.set_footer(
            text=f"Moondog Logistics Applications |  apply error message â€¢ {time_main2}")
        await ctx.send(embed=apply_on_cooldown)


@bot.command()
async def close(ctx, id, user: discord.Member):
    await ctx.message.delete()
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(
                title="Moondog Logistics Applications", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)

            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            await user.remove_roles(role)
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
            sql = f"UPDATE applications SET status = 'Closed', statusaddedby = '{ctx.author}' WHERE applicationid = '{id}'"
            mycursor.execute(sql)
            mydb.commit()
            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"Updated Mysql applications to 'closed'.")
            hook.send(embed=userapplyed)
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            await ctx.author.remove_roles(role)
            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            now = datetime.now(pytz.timezone("Europe/London"))
            userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"{ctx.author.mention} Has closed Application {id} @ {now}")
            hook.send(embed=userapplyed)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Moondog Logistics Applications", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await asyncio.sleep(60)
            await ctx.send(embed=em)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)


@close.error
async def close_handler_missing_arg(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # sends error if the command has not be used in a application ticket channel.
        provide_args = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                     description="Please include `id` and `member` at the end of the command `a/close`", color=0xFF0000)
        await ctx.send(embed=provide_args)


@close.error
async def close_handler(ctx, error):
    if isinstance(error, commands.BadArgument):
        no_member = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                  description="I cant find that member in this guild :(", color=0xFF0000)
        await ctx.send(embed=no_member)


@bot.command()
async def hire(ctx, id, tmpid,  member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
  if role in ctx.author.roles:
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()
    sql = f"UPDATE applications SET status = 'Hired', statusaddedby = '{ctx.author}' WHERE applicationid = '{id}'"
    mycursor.execute(sql)
    mydb.commit()
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "yes"

        try:

            em3445 = discord.Embed(
                title="Moondog Logistics Applications", description="Are you sure you want to hire this driver? Reply with `yes` if you are sure.", color=0x00a8ff)
            await ctx.send(embed=em3445)
            await bot.wait_for('message', check=check, timeout=60)
            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            role2 = discord.utils.get(
                ctx.guild.roles, name="Probationary Driver")
            await member.remove_roles(role)
            await member.add_roles(role2)

            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            info1 = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"Updated **mysql** table `applications` SET status of application {id} to `hired`")
            hook.send(embed=info1)
            getinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
            r = requests.get(getinfourl)
            data = r.json()["response"]
            cursor = mydb.cursor()
            sql = "INSERT INTO drivers (name, discordname, tmpid, steamid, role) VALUES (%s, %s, %s, %s, %s)"
            val = (data["name"], f"{member}", f"{tmpid}",
                   data["steamID64"], f"Probationary Driver")
            cursor.execute(sql, val)
            mydb.commit()
            await member.send(f"{ctx.author} just updated your application at Moondog Logistics to `Hired`")
            await member.send("Welcome to Moondog Logistics Your role is `Probationary Driver`")
            channel1 = bot.get_channel(797186729232433193)
            #await channel1.send(f"Welcome to Moondog Logistics {member.mention}. Please Book your training here https://alle-group.com/book-training/")
            hook = Webhook(
                'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
            em2 = discord.Embed(
                title=f"{member} has been promoted to Probationary Driver", description="")
            #hook.send(embed=em2)
            userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"{ctx.author.mention} Hired {member.mention}")
            #hook.send(embed=userapplyed)
            await ctx.send("Driver added to our database and to our company")
            await ctx.channel.delete()

            try:
                role1 = discord.utils.get(
                    ctx.guild.roles, id=837666217413967882)
                role2 = discord.utils.get(
                    ctx.guild.roles, id=837607050417537045)
                role3 = discord.utils.get(
                    ctx.guild.roles, id=837608034721071104)
                hours = 60*60
                await asyncio.sleep(3628800)
                await member.remove_roles(role3)
                await member.add_roles(role1)
                await member.add_roles(role2)
                joined_server = member.joined_at.strftime("%b %d, %Y")
                await member.send(f"Hey, your probation period is up congrats. You have been in Moondog Logisticss Discord server since: {joined_server}")
            except:
                await ctx.send("oh it did not work")

            # Adding in #staff-logs logging for this bot!
            try:
                hire_log_msg = discord.Embed(
                    title="Moondog | Applications", description=f"New driver hired by {ctx.author.mention} | Addded to the company api and database | Please add to the staff hub (coming soon!!)")
                staff_logs_channel = bot.get_channel(837715287092232264)
                await staff_logs_channel.send(embed=hire_log_msg)

            except:
                hire_log_err_msg = discord.Embed(
                    title="Moondog | Applications | Error", descrition=f"Error could not send the log message to {staff_logs_channel.mention}.")
                await ctx.author.send(embed=hire_log_err_msg)

            # Add to staff hub message (send in dms).
            try:
                advice_msg = discord.Embed(
                    title="Moondog | Applications", descrition=f"{member} | has been hired. | Please add them to the staff hub.")
                await ctx.author.send(embed=advice_msg)

            except:
                advice_msg_error = discord.Embed(
                    title="Moondog | Applications", descrition=f"{ctx.author.mention} I tried to send you a msg in dms but i could not. pepesad")
                main_chat_channel = bot.get_channel(837713193672900688)
                await ctx.main_chat_channel.send(embed=advice_msg_error)

         #this will happen if it times out after 60 secs
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Moondog Logistics Applications", description="You have run out of time to hire this driver. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Moondog Logistics Applications | `hire` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)
  else:
      errormsg = discord.Embed(
          title="Moondog Logistics applications", description="You do not have the correct roles or perms to use the command `hire`", color=0xFF0000
      )
      await ctx.send(embed=errormsg)


@hire.error
async def hire_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
       forgotiderr = discord.Embed(
           title="Moondog Logistics Applications | `hire` error", description=f"This command requires the following arguments `id` `tmpid` `member` one of these are not present in your command `(a/hire application-id, tmpid, member(discord ping))`", color=0xFF0000)
    await ctx.send(embed=forgotiderr)


@hire.error
async def hire_handler2(ctx, error):
    if isinstance(error, commands.BadArgument):
        no_member = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                  description="I cant find that member in this guild :(", color=0xFF0000)
        await ctx.send(embed=no_member)


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


# fixed claim command.
@bot.command()
async def claim(ctx, id):
    await ctx.message.delete()
    with open('data.json') as f:
        data = json.load(f)

    # if statement checks if the channel id the command was used in is a application channel or not ONLY WORKS FOR ACTIVE APPLICATION CHANNELS
    if ctx.channel.id in data["ticket-channel-ids"]:
     role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
     # if statement checks if the author of the command has the role mentioned above.
     if role in ctx.author.roles:
        channel_id = ctx.channel.id
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fv4&4*JT61%8WGj&vwj",
            database="alleapi"
        )

        mycursor = mydb.cursor()
        sql = f"UPDATE applications SET status = 'Claimed/inprogress', statusaddedby = '{ctx.author}' WHERE applicationid = '{id}'"
        mycursor.execute(sql)
        mydb.commit()
        em2 = discord.Embed(description=f"{ctx.author.mention} just claimed application id {id}",
                            url=f"https://api-alle-group.com/api/v2/applications/{id}")
        await ctx.send(embed=em2)
     else:
         # sends error msg if the user does not have the right role.
         does_not_have_role = discord.Embed(title="Moondog Logistics Applications | `claim` error",
                                            description=f"This command can only be used by people with the `Director` Role", color=0xFF0000)
         await ctx.send(embed=does_not_have_role)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Moondog Logistics Applications | `claim` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)


# send error if they do not provide a application id.
@claim.error
async def claim_handler2(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        forgotiderr = discord.Embed(
            title="Moondog Logistics Applications | `claim` error", description=f"Please provide a `id`", color=0xFF0000)
    await ctx.send(embed=forgotiderr)


#command to request training.
# @bot.command()
# async def request(ctx):
#     await ctx.message.delete()
#     #day = dt.now()
#     #mydb = mysql.connector.connect(
#     #host="localhost",
#     # user="root",
#     #  password="Fv4&4*JT61%8WGj&vwj",
#     #   database="alleapi"
#     #)
#     #mycursor = mydb.cursor()
#     #mycursor.execute(
#    #     f"SELECT COUNT(discordname) FROM applications WHERE discordname = '{ctx.author}'")
#    # result = mycursor.fetchall()
#    # hook = Webhook(
#     #    'https://discord.com/api/webhooks/825657922703982622/frltOXWR9Di-VYeNelDDHoLiO3sqcO7o6FgxHWt68MTzL3wZpQOrxlqRuNe0IU9LY-CO')
#    # em2 = discord.Embed(title=f"New training request.", color=0x00FF00)
#    # em2.add_field(
#    #     name="User", value=f"{ctx.author.name}#{ctx.author.discriminator}")
#    # em2.add_field(name="Requested Date", value=f"{date}", inline=True)
#    # em2.add_field(name="Requested Time", value=f"{time}", inline=True)
#    # em2.add_field(name="Message", value=f"{message}", inline=False)
#     #em2.add_field(name="Request date and time", value=f"{day}", inline=True)
#     #em2.add_field(name="Number of applications from user",
#    #               value=f"{result}", inline=False)
#    # hook.send(embed=em2)
#    # await ctx.send("Your Training request has been sent to the admissions team.")
#     we_dont_do_trainings = discord.Embed(title="Moondog Logistics Applications | Out Of Date Command",
#                                          description=f"Hey {ctx.author.name}, we no longer offer driver training. As there is a new system in place now :)")
#     global time_main2
#     we_dont_do_trainings.set_footer(
#         text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
#     await ctx.send("Look in your dms")
#     try:
#         await ctx.author.send(embed=we_dont_do_trainings)
#     except:
#         your_dms_are_disabled = discord.Embed(
#             title="Moondog Logistics Applications | Out Of Date Command Error", description=f"{ctx.author.mention} i tried to dm you but i could not :(")
#         your_dms_are_disabled.set_footer(
#             text=f"Moondog Logistics Applications | Error Logging Message â€¢ {time_main2}")
#         await ctx.send(embed=your_dms_are_disabled)


# @bot.command()
# async def confirm(ctx):
#     await ctx.message.delete()
#     #mydb = mysql.connector.connect(
#     #  host="localhost",
#     # user="root",
#     #   password="Fv4&4*JT61%8WGj&vwj",
#     #  database="alleapi"
#     #)
#     #getplayerinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
#     #r = requests.get(getplayerinfourl)
#     #data = r.json()["response"]
#     #for server in data:
#     # mycursor = mydb.cursor()
#     # sql = "INSERT INTO trainings(tmpid, steamid, trainedby, videoevidence, traineename, status, date, time, server, orgin, destinaton) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     # val = (f"{tmpid}", data["steamID64"], f"{ctx.author}",
#     #        f"{videourl}", data["name"],  f"{status}", f"{date}", f"{time}", f"{server}", f"{orgin}", f"{destination}")
#     #mycursor.execute(sql, val)
#     #mydb.commit()
#     #hook = Webhook(
#     #    'https://discord.com/api/webhooks/825683286428483594/nQbl4rw8fBcD_Q1Ig9ceNgUsHy9lQ-EOtTwCCyYTges0W8J2OIPVpXNQl6rLCWrj4JhF')
#     #em2 = discord.Embed(
#     #   title=data["name"], description=f"You have {status} your training", color=0x00FF00)
#     ##hook.send(embed=em2)
#     #hook2 = webhook(
#     #   'https: // discord.com/api/webhooks/833366266332708894/xoL7IBrAFGRpcUaIi2NMbLgEpQJqQ8nB-ogQe9AYEuJG2Tt9JQ8qOFBF1qvFtEHxLlq2'
#     #)
#     #em3 = discord.Embed(
#     #   title=data["name"], description=f"Has passed there training. Trained by:{ctx.author}", color=0x00FF00)
#     #hook2.send(embed=em3)
#     global time_main2
#     we_dont_do_trainings = discord.Embed(title="Moondog Logistics Applications | Out Of Date Command",
#                                          description=f"Hey {ctx.author.name}, we no longer offer driver training. As there is a new system in place now :)")
#     we_dont_do_trainings.set_footer(
#         text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
#     await ctx.send("Look in your dms")
#     try:
#         await ctx.author.send(embed=we_dont_do_trainings)
#     except:
#         your_dms_are_disabled = discord.Embed(
#             title="Moondog Logistics Applications | Out Of Date Command Error", description=f"{ctx.author.mention} i tried to dm you but i could not :(")
#         your_dms_are_disabled.set_footer(
#             text=f"Moondog Logistics Applications | Error Logging Message â€¢ {time_main2}")
#         await ctx.send(embed=your_dms_are_disabled)

# allows anyone to view a training that has been added to the DB.


@bot.command()
async def checkt(ctx, tmpid):
   await ctx.message.delete()
   global time_main2
   we_dont_do_trainings = discord.Embed(title="Moondog Logistics Applications | Out Of Date Command",
                                        description=f"Hey {ctx.author.name}, we no longer offer driver training. As there is a new system in place now :)")
   we_dont_do_trainings.set_footer(
       text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
   await ctx.send("Look in your dms")
   try:
       await ctx.author.send(embed=we_dont_do_trainings)
   except:
       your_dms_are_disabled = discord.Embed(
           title="Moondog Logistics Applications | Out Of Date Command Error", description=f"{ctx.author.mention} i tried to dm you but i could not :(")
       your_dms_are_disabled.set_footer(
           text=f"Moondog Logistics Applications | Error Logging Message â€¢ {time_main2}")
       await ctx.send(embed=your_dms_are_disabled)
    #try:
     #gettraininginfourl = f'https://api-alle-group.com/api/v2/trainings{tmpid}'
     #r = requests.get(gettraininginfourl)
     #data = r.json()
    #for data in data:
      #   embed = discord.Embed(title='Training Informaiton',
       #                        url=f'https://api-alle-group.com/api/v2/trainings{tmpid}', color=0xff0000)
       # embed.add_field(name="Trainee Name",
       #                value=data['traineename'], inline=False)
       #embed.add_field(name='Trained By',
       #                value=data['trainedby'], inline=False)
       #embed.add_field(name='Status of Training',
       #               value=data['status'], inline=False)
       #embed.add_field(name='Date and Time',
       #                value=f"{data['date']} {data['time']}", inline=False)
       #embed.add_field(name='Server', value=data['server'], inline=False)
       #embed.add_field(name='Training Origin and Destination',
       #               value=f"Origin: {data['orgin']} | Destination: {data['destinaton']}", inline=False)
      # try:
       #   await ctx.send(embed=embed)
        #except:
        #   cannot_send_embed = discord.Embed(
           #       title="Moondog Logistics Applications | `checkt` error", description=f"I cant send the results embed :(", color=0xFF0000)
            #  await ctx.send(embed=cannot_send_embed)
                #except:
                             #   cannot_find_training = discord.Embed(
       #      title="Moondog Logistics Applications | `checkt` error", description=f"That training does not appear to exist :(", color=0xFF0000)
               # await ctx.send(embed=cannot_find_training)


@checkt.error
async def checkt_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        cannot_find_training = discord.Embed(
            title="Moondog Logistics Applications | `checkt` error", description=f"Please provide a `TMPID`", color=0xFF0000)
        await ctx.send(embed=cannot_find_training)


#@bot.command()
#async def wtrainings(ctx):
 # await ctx.message.delete()
 # role = discord.utils.get(ctx.guild.roles, id=794865611956158484)
  #if role in ctx.author.roles:
  #  await ctx.author.send("To view all web booked trainings go to this link http://www.staff-alle-group.com/exams/training/staff/training/")
   # await ctx.send("I've sent u a dm :) credit:`truckerbean`")
  #else:
   #   await ctx.author.send("You dont have the right perms to use this command :(. If you think u need these perms then alert yzzoxi")


# get the application status (changing to make sure it it is being used in a application channel)
@bot.command()
async def status(ctx, id):
    await ctx.message.delete()
    getstatusinfourl = f"https://api-alle-group.com/api/v2/applications/checkstatus/{id}"
    r = requests.get(getstatusinfourl)
    data = r.json()
    for data in data:
     em = discord.Embed(title="Your application status is", url=f"https://api-alle-group.com/api/v2/applications/checkstatus/{id}",
                        description=data['status'])
     await ctx.send(embed=em)


#black list a user from applying by there tmpid (BETA)
@bot.command()
async def blacklist(ctx, tmpname, discordid, tmpid=None, *, reason):
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    cursor = mydb.cursor()
    global time_main2
    cursor.execute(
        f"SELECT  discordid FROM blacklist WHERE discordid = '{discordid}'")
    results = cursor.fetchall()
    # gets the number of rows affected by the command executed
    row_count = cursor.rowcount
    if row_count > 0:
        Member_already_blacklisted = discord.Embed(
            title="Moondog Logistics Applications | `blacklist` error", description=f"That person is already blacklisted. DiscordID: {discordid}", color=0xFF0000)
        await ctx.send(embed=Member_already_blacklisted)
    else:
        await ctx.send("Done")
        # the member is not in the server, do something #
        sql = "INSERT INTO blacklist(tmpname, discordid, tmpid, reason) VALUES (%s, %s, %s, %s)"
        val = (f"{tmpname}", f"{discordid}", f"{tmpid}", f"{reason}")
        cursor.execute(sql, val)
        # This will try to commit the above sql statement but if it there already is an entry then it will return an error.
        mydb.commit()
        Blacklisted_message = discord.Embed(title="Moondog Logistics Applications | Blacklist System",
                                            description=f"{ctx.author.mention}, Blacklisted the discord id {discordid} from applying with Moondog Logistics. More Info: TMPID: {tmpid}, Blacklist Reason: {reason}. **This action is irreversible**")
        Blacklisted_message.set_footer(
            text=f'Moondog Logistics Applications |  Blacklist System â€¢ {time_main2}')
        await ctx.send(embed=Blacklisted_message)
    # If there is already a blacklist report in for the member then it will return this error.


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
async def reply(ctx, *, message):
    await ctx.message.delete()
    with open('data.json') as f:
        data = json.load(f)
    # if statement checks if the channel id the command was used in is a application channel or not ONLY WORKS FOR ACTIVE APPLICATION CHANNELS
    if ctx.channel.id in data["ticket-channel-ids"]:
        em = discord.Embed(
            title="Message From Moondog | Admissions  Team", description=f"{message}")
        await ctx.send(embed=em)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Moondog Logistics Applications | `claim` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)


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
            title=f"{member} has been promoted to {roled}", description="")
        hook.send(embed=em2)
        role = f"{roleid}"
        await member.add_roles(role)


# command to allow the instant promotion for drivers currently on probation that are to be upped before the auto system ups them.
@bot.command()
async def finished(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
    if role in ctx.author.roles:
        await ctx.message.delete()
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fv4&4*JT61%8WGj&vwj",
            database="alleapi"
        )
        mycursor = mydb.cursor()
        sql = f"UPDATE applications SET status = 'Driver' WHERE discordname = '{member}'"
        mycursor.execute(sql)
        mydb.commit()
        role3 = discord.utils.get(
            ctx.guild.roles, id=837608034721071104)
        await member.remove_roles(role3)
        role1 = discord.utils.get(ctx.guild.roles, id=837666217413967882)
        await member.add_roles(role1)
        role2 = discord.utils.get(ctx.guild.roles, id=837607050417537045)
        await member.add_roles(role2)
        joined_server = member.joined_at.strftime("%b %d, %Y")
        await member.send(f"Hey, your probation period is up congrats. You have been in Moondog Logisticss Discord server since: {joined_server}")

    else:
        await ctx.send()


@finished.error
async def finished_handler2(ctx, error):
    if isinstance(error, commands.BadArgument):
        cant_find_member = discord.Embed(
            title="Moondog Logistics Applications | `finished` error", description=f"I cant cant find that member in this guild :(", color=0xFF0000)
        await ctx.send(embed=cant_find_member)


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
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.now(
        pytz.timezone("Europe/London")))
    embed.set_footer(text="Moondog Logistics training reminding system credit: truckerbean",
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
    embed.add_field(name='Time conversation system Moondog Logistics',
                    value=f"Your conversation from **{hours}hrs** to **{minutes}mins** credit: Truckerbean")
    await ctx.send("Look in your dms :)")
    await ctx.author.send(embed=embed)


@bot.command()
async def convertd(ctx, ):
    await ctx.message.delete()
    embed = discord.Embed(color=0x55a7f7)
    embed.add_field(name='Time conversation system Moondog Logistics',
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


@bot.command()
async def bug(ctx):
    await ctx.message.delete()
    # this command needs to send data to devs and stuff that has applications in it is to be sent to Bean.
    global bug_id

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    global time_main2
    what_is_the_bug_em = discord.Embed(
        title="Moondog Logistics Applications | Bug Report System ", description=f"Hey, {ctx.author.name} what is the bug?", color=0xFF0000)
    what_is_the_bug_em.set_footer(
        text=f"Moondog Logistics Applications | Bug Report System â€¢ {time_main2}")
    message = await ctx.send(embed=what_is_the_bug_em)
    msg = await bot.wait_for('message', check=check)
    response = (msg.content)

    if 'applications' and 'application' and 'apps' and 'application' in response:
        bug_id += 1
        new_applications_bug_em = discord.Embed(title="Moondog Logistics Applications | New Bug Report Submitted",
                                                description=f"Yo Bean, {ctx.author.name} has submitted the following bug: **`{response}`**", color=0xFF0000)
        new_applications_bug_em.add_field(
            name="Reporting User's ID:", value=f"{ctx.author.id}", inline=False)
        timestamp = datetime.now(pytz.timezone("Europe/London"))
        new_applications_bug_em.add_field(
            name="Report Submitted:", value=timestamp.strftime(r"On: %d/%m/%Y At: %I:%M %p"))
        new_applications_bug_em.add_field(
            name="Bug ID:", value=f"{bug_id}", inline=False)
        test_time = timestamp.strftime(r"%I:%M %p")
        new_applications_bug_em.set_footer(
            text=f"Moondog Logistics Applications | Bug Report System â€¢ {test_time}")

        user = bot.get_user(755493797160288286)
        await user.send(embed=new_applications_bug_em)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fv4&4*JT61%8WGj&vwj",
            database="alleapi"
        )
        mycursor = mydb.cursor()
        timestamp = datetime.now(pytz.timezone("Europe/London"))
        time_and_date = timestamp.strftime(r"On: %d/%m/%Y At: %I:%M %p")
        sql = "INSERT INTO  alle_bugs(bugid, submitedby, fixedby, submitteddate, fixeddate, bug) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (f"{bug_id}",
               f"{ctx.author.id}", f"Not Yet Fixed", f"{time_and_date}", f"Not Yet Fixed", f"{response}")
        mycursor.execute(sql, val)
        mydb.commit()
        await ctx.author.send(f"Thanks for submitting your bug your id is {bug_id}")
    else:
        bug_id += 1
        user1 = discord.utils.get(
            ctx.guild.members, id=755493797160288286)
        user2 = discord.utils.get(
            ctx.guild.members, id=344999742847320064)

        new_applications_bug2_em = discord.Embed(title="Moondog Logistics Applications | New Bug Report Submitted",
                                                 description=f"Yo Devs, {ctx.author.name} has submitted the following bug: **`{response}`**", color=0xFF0000)
        new_applications_bug2_em.add_field(
            name="Reporting User's ID:", value=f"{ctx.author.id}", inline=False)
        timestamp2 = datetime.now(pytz.timezone("Europe/London"))
        new_applications_bug2_em.add_field(
            name="Report Submitted:", value=timestamp2.strftime(r"On: %d/%m/%Y At: %I:%M %p"))
        new_applications_bug2_em.add_field(
            name="Bug ID:", value=f"{bug_id}", inline=False)
        new_applications_bug2_em.set_footer(
            text=f"Moondog Logistics Applications | Bug Report System â€¢ {time_main2}")
        channel = discord.utils.get(ctx.guild.channels, id=837715287092232264)
        await channel.send(f'{user1.mention}')
        await channel.send(f'{user2.mention}')
        await channel.send(embed=new_applications_bug2_em)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fv4&4*JT61%8WGj&vwj",
            database="alleapi"
        )
        mycursor = mydb.cursor()
        timestamp = datetime.now(pytz.timezone("Europe/London"))
        time_and_date = timestamp.strftime(r"On: %d/%m/%Y At: %I:%M %p")
        sql = "INSERT INTO  alle_bugs(bugid, submitedby, fixedby, submitteddate, fixeddate, bug) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (f"{bug_id}",
               f"{ctx.author.id}", f"Not Yet Fixed", f"{time_and_date}", f"Not Yet Fixed", f"{response}")
        mycursor.execute(sql, val)
        mydb.commit()
        await ctx.author.send(f"Thanks for submitting your bug your id is {bug_id}")
    await msg.delete()
    await message.delete()


@bot.command()
async def bugu(ctx, id, *, comment="Thanks for reporting the bug it has been fixed."):
    await ctx.message.delete()
    get_bug_info_url = f'https://api-alle-group.com/api/v2/bugs/{id}'
    r = requests.get(get_bug_info_url)
    data = r.json()
    for data in data:
        embed = discord.Embed(
            title="Moondog Logistics Applications | Bug Report System", description=f"Thanks for submitting bug ID  {data['bugid']}")
        embed.add_field(name="Bug", value=data['bug'], inline=False)
        embed.add_field(name="Submitted Date:",
                        value=data['submitteddate'], inline=False)
        embed.add_field(name="Bug Comment", value=comment, inline=False)
    #user = bot.get_user(data['submitedby'])
    await ctx.send(embed=embed)


@bot.command()
async def report(ctx):
    await ctx.message.delete()

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    global time_main2
    info_driver_report_1 = discord.Embed(
        title="Moondog Logistics Applications | Driver Report System", description=f"Hey, {ctx.author.name} Please provide the drivers name.", color=0xFF0000)
    info_driver_report_1.set_footer(
        text=f"Moondog Logistics Applications | Driver Report System â€¢ {time_main2}")
    message = await ctx.send(embed=info_driver_report_1)
    msg = await bot.wait_for('message', check=check)
    response = (msg.content)

    info_driver_report_2 = discord.Embed(
        title="Moondog Logistics Applications | Driver Report System", description=f"What is the drivers tmpID?", color=0xFF0000)
    info_driver_report_2.set_footer(
        text=f"Moondog Logistics Applications | Driver Report System â€¢ {time_main2}")
    message2 = await ctx.send(embed=info_driver_report_2)
    msg2 = await bot.wait_for('message', check=check)
    response2 = (msg2.content)

    info_driver_report_3 = discord.Embed(
        title="Moondog Logistics Applications | Driver Report System", description=f"Please explain the reason why you have reported this driver today?", color=0xFF0000)
    info_driver_report_3.set_footer(
        text=f"Moondog Logistics Applications | Driver Report System â€¢ {time_main2}")
    message3 = await ctx.send(embed=info_driver_report_3)
    msg3 = await bot.wait_for('message', check=check)
    response3 = (msg3.content)
    timestamp2 = datetime.now(pytz.timezone("Europe/London"))
    driver_reported_for_shit_driving_em = discord.Embed(
        title="Moondog Logistics Applications | New Driver Report In", description=f"", color=0xFF0000)
    driver_reported_for_shit_driving_em.add_field(
        name="Drivers Name:", value=f"{response}", inline=True)
    driver_reported_for_shit_driving_em.add_field(
        name="Drivers tmpID:", value=f"{response2}", inline=True)
    driver_reported_for_shit_driving_em.add_field(
        name="Report Reason:", value=f"{response3}", inline=True)
    driver_reported_for_shit_driving_em.add_field(
        name="Date Report Submitted:", value=timestamp2.strftime(r"On: %d/%m/%Y At: %I:%M %p"), inline=True)
    driver_reported_for_shit_driving_em.add_field(
        name="Reporters Discord Name:", value=f"{ctx.author.name}", inline=True)
    driver_reported_for_shit_driving_em.set_footer(
        text=f"Moondog Logistics Applications | Driver Report System â€¢ {time_main2}")
    channel = discord.utils.get(ctx.guild.channels, id=837714802049679451)
    await channel.send(embed=driver_reported_for_shit_driving_em)

    #embed saying thanks for sending in the report.
    thx_for_reporting = discord.Embed(title="Moondog Logistics Applications | Thanks For Reporting.",
                                      description="We will take whatever action we take fit on your report.", color=0xFF0000)
    thx_for_reporting.set_footer(
        text=f"Moondog Logistics Applications | Driver Report System â€¢ {time_main2}")
    await ctx.send(embed=thx_for_reporting)


@bot.command()
async def apinfo(ctx, tmpid):
    await ctx.message.delete()

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
    #  guild = bot.get_guild(688060261470568567)
    # find ID by right clicking on a user and choosing "copy id" at the bottom
     # if guild.get_member(755493797160288286):
     #   em2.add_field(name="In Discord server?",
      #             value="Yes", inline=True)
     # else:
      #  em2.add_field(name="In Discord server?",
      #                  value="No", inline=True)
    await ctx.send(embed=em2)


async def bot_command_error(self, ctx: commands.Context, error: commands.CommandError):
    await ctx.send('An error occurred: {}'.format(str(error)))


@bot.command()
async def suggest(ctx):
    await ctx.message.delete()

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    what_is_the_suggestion_em = discord.Embed(
        title="Moondog Logistics Suggestions", description="Please write your suggestion. Need help? Here's the [Format](https://discord.com/channels/837600839052689418/849399174289686548/849405042376441886)", color=0x00993C)
    global time_main
    global time_main2
    what_is_the_suggestion_em.set_footer(
        text=f"Moondog Logistics | Suggestions â€¢ {time_main2}")
    message3 = await ctx.send(embed=what_is_the_suggestion_em)
    msg3 = await bot.wait_for('message', check=check)
    response3 = (msg3.content)
    await msg3.delete()
    await message3.delete()
    suggestion_em = discord.Embed(
        title="Moondog Logistics Suggestions", color=0x00993C)
    suggestion_em.add_field(
        name="Name:", value=f"{ctx.author.name}", inline=False)
    suggestion_em.add_field(name="Date:", value=f"{time_main}", inline=False)
    suggestion_em.add_field(
        name="Suggestion:", value=f"{response3}", inline=False)
    suggestion_em.set_footer(text=f"Moondog Logistics | Suggestions â€¢ {time_main2}")
    channel = discord.utils.get(ctx.guild.channels, id=849399174289686548)
    send_embed = await channel.send(embed=suggestion_em)
    await send_embed.add_reaction("âœ”ï¸")
    await send_embed.add_reaction("âŒ")


@bot.command()
async def lookup(ctx, tmpid):
    await ctx.message.delete()
    getapplicationsdataurl = f'https://api-alle-group.com/api/v2/applications/{tmpid}'
    r = requests.get(getapplicationsdataurl)
    data = r.json()
    for data in data:
            embed = discord.Embed(title='User Info',
                                   url=f'https://api-alle-group.com/api/v2/applications/{tmpid}', color=0xff0000)
            embed.add_field(name="Name",
                              value=data['discordname'], inline=False)
            embed.add_field(name='Application ID',
                               value=data['applicationid'], inline=False)
            embed.add_field(name='Status of Applications',
                                value=data['status'], inline=False)
            embed.add_field(name='Date and Time',
                                value=f"{data['applicationdate']}", inline=False)

                #embed.add_field(name="TMPID", value=data[tmpid])

    await ctx.send(embed=embed)



# add events to Alle Local Api from Tmp API.
@bot.command(aliases=['newevent', 'addnewevent', 'checkevent', 'publishevent'])
async def einfo(ctx, tmpeid):
    await ctx.message.delete()
    # require the id from the event link.
    geteventinfo = f'https://api.truckersmp.com/v2/events/{tmpeid}'
    r = requests.get(geteventinfo)
    data = r.json()["response"]
    event_info = discord.Embed(title="Event Info", description=f"The requested {data['event_type']['name']} info for {data['id']}.", color=0x05647)
    event_info.add_field(name="Event Name ", value=f"{data['name']}", inline=False)
    event_info.add_field(name="Game", value=f"{data['game']}", inline=False)
    event_info.add_field(name="Departure City", value=f"{data['departure']['city']}")
    event_info.add_field(name="Arrival City", value=f"{data['arrive']['city']}")
    event_info.add_field(name="Event Page Link", value=f"[Here](https://truckersmp.com/events/{tmpeid})")
    event_info.set_thumbnail(url=f"{data['banner']}")
    event_info.set_image(url=f"{data['map']}")
    event_info.set_footer(text=f"Event Start Time And Date: {data['start_at']}")
    await ctx.send(embed=event_info)
   

    await ctx.send('To publish this event do a/publish [eventinfo] in the format posted.')
    # await ctx.send('reply with yes or no')
    # msg = await bot.wait_for('message', check=check)
    # response = (msg.content)

    # if 'yes' in response:
    #     guild = ctx.message.guild 
    #     new_channel = await guild.create_text_channel(f"{data['name']}-{eventdate}")
    #     print(new_channel.id)
    #     int(new_channel.id)
    #     event_channel = bot.get_channel(id=new_channel.id)
    #     send_event = discord.Embed(
    #         title=f"{data['name']}", description=f"")
    #     await event_channel.send(embed=send_event)
    # else:
    #     pass    



@bot.command()
async def publish(ctx):
    await ctx.message.delete()
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    # removed the having to pre define the convoy info.
    embed_1 = discord.Embed(title="When Is this Event Going To Take Place?", description="Please reply with the time..") 
    await ctx.send(embed=embed_1)
    msg = await bot.wait_for('message', check=check)
    response = (msg.content)
    
    embed_2 = discord.Embed(title="When Is this Event Going To Take Place?", description="Please reply with the date..")
    await ctx.send(embed=embed_2)
    msg2 = await bot.wait_for('message', check=check)
    response2 = (msg2.content)

    embed = discord.Embed(title="What is the Event Name")
    await ctx.send(embed=embed)
    msg1 = await bot.wait_for('message', check=check)
    response1 = (msg1.content) 
    
    
    embed_3 = discord.Embed(title="Event Info In Required Format.")
    await ctx.send(embed=embed_3)
    msg3 = await bot.wait_for('message', check=check)
    response3 = (msg3.content)
    

    final_embed = discord.Embed(title=f"{response1} | {response2} @ {response}", description=f"{response3}", color=0x05647)
    category = discord.utils.get(
        ctx.guild.categories, name="| ð„ð¯ðžð§ð­ð¬ ð‚ðšð¥ðžð§ððžð«")
    new_channel = await ctx.guild.create_text_channel(f"{response1}-{response2}", category=category)   
    int(new_channel.id)
    event_channel = bot.get_channel(id=new_channel.id) 
    await event_channel.send(embed=final_embed)


























# truckers mp traffic / server commands.
#Experimental command for Server List
@bot.command()
async def servers(ctx):
 await ctx.message.delete()
 try:
  getserversURL = "https://api.truckersmp.com/v2/servers"
  r = requests.get(getserversURL)
  data = r.json()["response"]
  embed = discord.Embed(title="TMP Server Status",
                        url="https://traffic.krashnz.com/", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(
      text="Bot code developed by Moondog Devs")
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
 except:
     tmpaiissues = discord.Embed(
         title="TMP Server Status", description="It appears TMP are having API issues this is something that Moondog can not control ðŸ˜¢", color=0xFF0000)
     await ctx.send(embed=tmpaiissues)
 #Commands for Traffic


@bot.command()
async def traffic(ctx):
  getinfoURL = "https://traffic.krashnz.com/api/v2/public/server/ets2/sim1/top.json"
  embed = discord.Embed(title="TMP ETS2 Sim 1 Status", color=0xFF0000)
  embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
  embed.set_footer(
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
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
      text="Bot code developed by Moondog Devs")
  r = requests.get(getSim2TFC)
  data = r.json()['response']
  for top in data['top']:
    name = top['name']
    congestion = top['severity']
    drivers = str(top['players'])
    embed.add_field(name=name, value=congestion + '/' + drivers, inline=True)
  await ctx.send(embed=embed)


# embed command / announce command

@bot.command(aliases=['announce', 'announcement'])
async def embed(ctx):
   await ctx.message.delete()
   def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
   global time_main2 
   embed_content = discord.Embed(title="Moondog Logistics Embed / Announcement Commands", description="Please write the announcement content.", color=0xFF000)
   embed_content.set_footer(
       text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logistics Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embed_content)
   msg = await bot.wait_for('message', check=check)
   response = (msg.content)
    
   embed_channel = discord.Embed(title="Moondog Logistics Embed / Announcement Commands", description="Please mention the channel you wish the embed to be sent in.", color=0xFF000)
   embed_channel.set_footer(
       text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logisticss Embed / Announcement Commands â€¢ {time_main2}")
   await ctx.send(embed=embed_channel)
   msg2 = await bot.wait_for('message', check=check)
   response2 = (msg2.content)
   channel_id = msg2.channel_mentions[0].id
   print(channel_id)
   channelID = int(channel_id)
   channel = discord.utils.get(ctx.guild.text_channels, id=channelID)
   

   embed_color = discord.Embed(title="Moondog Logistics Embed / Announcement Commands", description="Please pick a color you wish your embed to be. The options are **blue**, **green**, **red**. If you want it to be a standard color say `skip`", color=0xFF000)
   embed_color.set_footer(text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logisticss Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embed_color)
   msg3 = await bot.wait_for('message', check=check)
   response3 = (msg3.content)
   if 'blue' in response3:
       color_1 = 0x0055FF
   elif 'green' in response3:
       color_2 = 0xFF000
   elif 'red' in response3:
       color_3 = 0xFF0000
   elif 'skip' in response3:
       pass            
   else:
       await ctx.send("The color you selected is not an option")
   
   
   embed_link = discord.Embed(title="Moondog Logistics Embed / Announcement Commands", description="Please say any links you wish to be within your embed. If you dont have an link then say `skip`.", color=0xFF000)
   embed_link.set_footer(text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logistics Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embed_link)
   msg4 = await bot.wait_for('message', check=check)
   response4 = (msg4.content)
   
   embed_image = discord.Embed(
       title="Moondog Logistics Embed / Announcement Commands", description="Please provide the image link. If you dont want a image say `skip`", color=0xFF000)
   embed_image.set_footer(
       text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logistics Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embed_image)
   msg5 = await bot.wait_for('message', check=check)    
   response5 = (msg5.content)
   
   embed_title = discord.Embed(title="Moondog Logistics Embed / Announcement Commands",
                               description="Please write the embed title.", color=0xFF000)
   embed_title.set_footer(
       text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logistics Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embed_title)
   msg6 = await bot.wait_for('message', check=check)
   response6 = (msg6.content)    
   
   embed_ping = discord.Embed(title="Moondog Logistics Embed / Announcement Commands",
                              description="Which Role should I ping? `everyone` or `Moondog Notified` or `Moondog Logistics` or for no ping say `skip`.", color=0x0055FF)
   embed_ping.set_footer(
       text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logistics Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embed_ping)
   msg7 = await bot.wait_for('message', check=check)
   response7 = (msg7.content)
   print('last embed request works')
   print(channelID)
   if 'blue' in response3:
       anouncement_embed = discord.Embed(title=f"{response6}", description=f"{response}", color=0x0055FF)
       print('blue color')
   elif 'green' in response3:
       anouncement_embed = discord.Embed(
           title=f"{response6}", description=f"{response}", color=0xFF000)
   elif 'red' in response3:
       anouncement_embed = discord.Embed(
           title=f"{response6}", description=f"{response}", color=0xFF0000)
   else: 
       anouncement_embed = discord.Embed(
           title=f"{response6}", description=f"{response}")

   if 'skip' in response4:
       pass
   else:
        anouncement_embed.add_field(name="Link", value=f"[Press Here]({response4})")
   
   if 'skip' in response5:
       pass
   else:
        anouncement_embed.set_image(url=f"{response5}")
   print('embed bit works') 
   if 'everyone' in response7:
       await channel.send("@everyone")
   elif 'here' in response7:
       await channel.send("@here")
   elif 'alle notified' in response7:
       role = discord.utils.get(ctx.guild.roles, id=837608163050127380)   
       await channel.send(f"{role.mention}")
   elif 'Moondog Logistics' in response7:
           role2 = discord.utils.get(ctx.guild.roles, id=849550483914752020)
           await channel.send(f"{role2.mention}")   
   elif 'skip' or 'pass' in response7:
       pass
   
   anouncement_embed.set_thumbnail(url='https://cdn.discordapp.com/icons/855574329509150720/bce5ee1672ec9c20de56d21951d88caf.png?size=128')
   anouncement_embed.set_footer(
       text=f"{response6} Sent By {ctx.author.name} â€¢ {time_main2}")
   embed_message = await channel.send(embed=anouncement_embed)
   
   embeded_message_sent_em = discord.Embed(
       description=f"Your Embed/Announcement Has Been Sent To {channel.mention}. To View The Message Click [**Here**]({embed_message.jump_url})", color=0xFF000)
   embeded_message_sent_em.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
   embeded_message_sent_em.set_thumbnail(url="https://cdn.discordapp.com/icons/855574329509150720/bce5ee1672ec9c20de56d21951d88caf.png?size=128")
   embeded_message_sent_em.set_footer(text=f"Built By bean!!!!!!!#0041 For Moondog Logistics | Moondog Logistics Embed / Announcement Commands  â€¢ {time_main2}")
   await ctx.send(embed=embeded_message_sent_em)





#music

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception): 
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(
            cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(
                'Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(
                    'Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(
            cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError(
                        'Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(
                                   self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_footer(text="Made By: bean!!!!!!!#0041 for Moondog Logistics")
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self, ctx):
      await ctx.voice_state.stop()

    async def disconnect(self):
        await self.voice.disconnect()


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage(
                'This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError(
                'You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    
    
    
    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context):
        if ctx.voice_state.voice:
            ctx.voice_state.songs.clear()
            await ctx.send("cleared")         
        elif not ctx.voice_state.voice :
            await ctx.send('Not connected to a voice channel.')    
        else:
            await ctx.send('No songs to clear.')
    
    
    
    @commands.command(name='leave', aliases=['disconnect'])
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')
        else:
            pass
        ctx.voice_state.songs.clear()
        
        del self.voice_states[ctx.guild.id]
        await ctx.voice_client.disconnect()  
        await ctx.send('Bot Left.')

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if not ctx.voice_state.is_playing:
            await ctx.send("**There is nothing playing or i am not in a voice channel**")
        else:
         if ctx.voice_state.voice.is_paused ():
            await ctx.send(f"**Alle is already paused**")
         else:

          if ctx.voice_state.is_playing:
            bot_nick = 'Moondog'
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('â¯')
        
          else:
            await ctx.send(f"**Moondog is not currently playing**")    
        
    @commands.command(name='resume')
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.voice.is_paused ():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('â¯')
        else:
            await ctx.send("**There is nothing to resume**")
    
    
    @commands.command(name='stop')
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if  ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('â¹')
        else:
            await ctx.send("There is nothing playing")
 
    
    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏩')
            ctx.voice_state.skip()
            await ctx.send('Song skipped playing next track :)')
        elif voter == discord.Permissions.administrator:
            await ctx.send('song skipped')
            ctx.voice_state.skip()

        else:
            await ctx.send('Song Skipped | Tho you did not request that song :(')
            ctx.voice_state.skip()

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(
                i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('âœ…')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('âœ…')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('âœ…')


    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')


bot.add_cog(Music(bot))


@bot.command()
@commands.guild_only()  # We can only access activities from a guild
async def spotify(ctx, user: discord.Member = None):
    user = user or ctx.author  # default to the caller
    spot = next((activity for activity in user.activities if isinstance(
        activity, discord.Spotify)), None)
    if spot is None:
        await ctx.send(f"{user.name} is not listening to Spotify")
        return
    embedspotify = discord.Embed(
        title=f"{user.name}'s Spotify", color=0x1eba10)
    embedspotify.add_field(name="Song", value=spot.title)
    embedspotify.add_field(name="Artist", value=spot.artist)
    embedspotify.add_field(name="Album", value=spot.album)
    embedspotify.set_thumbnail(url=spot.album_cover_url)
    await ctx.send(embed=embedspotify)


@bot.command()
@commands.is_owner()
async def srestart(ctx):
    await ctx.message.delete()
    await ctx.send('`[system] Bot will be restarting in 1 min` ')
    # await asyncio.sleep(60)
    os.execv(sys.argv[0], sys.argv)
    print("restarting")    
    exit()
    await ctx.send('Bot restarted')



# moderation commands
@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.message.author.guild_permissions.ban_members is True:
        await member.send(f'You have been banned for `{reason}`')
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned for the following reason: ```{reason}```')

    else:
        await ctx.send(f'You do not have permission to use this command.')


@bot.command(pass_context=True)
async def unban(ctx, *, member):
    if ctx.message.author.guild_permissions.ban_members is True:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entery in banned_users:
            user = ban_entery.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}. Make sure they behave!')
    else:
        await ctx.send(f'You do not have permission to use this command.')


@bot.command(pass_context=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.kick_members is True:
        await member.send(f"You have been kicked for `{reason}`. Please don't make the same mistake on other servers.")
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked for the following reason: ```{reason}```')

    else:
        await ctx.send(f'You do not have permission to use this command.')


@bot.command(pass_context=True)
async def warn(ctx, member: discord.Member, *, reason):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.manage_messages is True:
        await ctx.send(f'{member.mention} has been warned for `{reason}`, do not do it again')
        await member.send(
            f'You have been warned for `{reason}`, do not do it again. Repeated offences will result in getting kicked or banned from the server. You have been warned')
    else:
        await ctx.send(f'You do not have permission to use this command.')


@bot.command()
async def help(ctx, command='defualt'):
   await ctx.message.delete() 
   embed = discord.Embed(
        title='Command List', description='Because you forgot all the commands.', color=0xFF0000)
   embed.set_thumbnail(
        url='https://cdn.discordapp.com/icons/855574329509150720/bce5ee1672ec9c20de56d21951d88caf.png?size=128')
   embed.add_field(name=f'ETS Traffic Commands',
                    value=f'`Servers`, `Traffic`, `Traffic2`, `Traffic3`, `TrafficARC`, `TrafficUS`, `TrafficPM`, `TrafficPMARC`', inline=False)
   embed.add_field(name=f'ATS Traffic Commands',
                    value=f'`Servers`, `ATSTrafficUS`, `ATSTrafficUSARC`, `ATSTrafficEU`', inline=False)
   embed.add_field(name=f'Music Commands',
                    value=f'`Join`, `Summon`, `Leave`, `Volume`, `Now` (can also use `Current` or `Playing`), `Pause`, `Resume`, `Stop`, `Skip`, `Queue`, `Shuffle`, `Remove`, `Loop`, `Play`',
                    inline=False)
   embed.add_field(name=f'Other Commands',
                    value=f'`Ping`, `Apply`, `Help`, `Convert`, `ConvertD`, `Bug`, `Report`, `Suggest`, `embed` (can also use `announcement` and `announce`)', inline=False)
   embed.add_field(name="Simple Support Commands",
                    value="`unsupportedgv`, `installpromodstmp`, `whatistmpid`", inline=False)
   embed.add_field(name="Fun Commands BETA", value="`meme`, `dodgydave`, `avatar`, `avataru`, `joke`, `dadjoke`", inline=False)
   if ctx.message.author.guild_permissions.administrator:
        embed.add_field(name=f'Admin Commands',
                        value='`ban`, `warn`, `unban`, `claim`, `hire`', inline=False)
         
   else:
        pass
   if 'dodgydave' in command:
           dodgydavehelpembed = discord.Embed(
               title=f'{command} Command Help', description='In case your in need of some help :slight_smile:', color=0xE4003B)
           dodgydavehelpembed.set_thumbnail(
           url='https://cdn.discordapp.com/icons/855574329509150720/bce5ee1672ec9c20de56d21951d88caf.png?size=128')
           dodgydavehelpembed.add_field(name=f"Command Name:", value=f"{command}", inline=False)
           dodgydavehelpembed.add_field(name=f"Help:", value=f"`a/dodgydave` sends image and video link and quote. `a/dodgydave [no]` sends no image. ", inline=False)
           await ctx.send(embed=dodgydavehelpembed)
   elif 'avatar' in command:
           avatarhelpembed = discord.Embed(
               title=f'{command} Command Help', description='In case your in need of some help :slight_smile:', color=0xE4003B)
           avatarhelpembed.set_thumbnail(
           url='https://cdn.discordapp.com/icons/855574329509150720/bce5ee1672ec9c20de56d21951d88caf.png?size=128')
           avatarhelpembed.add_field(name=f"Command Name:", value=f"{command}", inline=False)
           avatarhelpembed.add_field(
               name=f"Help:", value=f"**This command is still in devlopment**", inline=False)
           await ctx.send(embed=avatarhelpembed)
   elif 'embed'  in command:
           embedhelpembed = discord.Embed(
               title=f'{command} Command Help', description='In case your in need of some help :slight_smile:', color=0x0032FF)
           embedhelpembed.set_thumbnail(
           url='https://cdn.discordapp.com/icons/855574329509150720/bce5ee1672ec9c20de56d21951d88caf.png?size=128')
           embedhelpembed.add_field(name=f"Command Name:", value=f"{command}", inline=False)
           embedhelpembed.add_field(
               name=f"Help:", value=f"This Command is very new and may contain some bugs. You can use either `embed` or `announce` or `announcement`", inline=False)
           await ctx.send(embed=embedhelpembed)
   else:
          
           await ctx.send(embed=embed)
  
       



@bot.command(name="volume")
async def volume(ctx, volume: float):
    await ctx.message.delete()
    voice = get(bot.voice_clients, guild=ctx.guild)
    if volume < 0 :
        await ctx.send("The **min** volume is **`0`**") 
    else:
     if volume > 100:
              await ctx.send("The **max** volume is **`100`**.")
     else:  
      if 0 <= volume <= 100:
        if voice.is_playing():  
            new_volume = volume / 100
            voice.source.volume = new_volume
            await ctx.reply(f"Volume Changed To: {volume}")
        else:
            await ctx.reply("The bot is not currently playing any songs.")
      else:
        await ctx.reply("Somethings not right. Report this using `a/bot` quoting **wont change volume**.")


# logging
@bot.event
async def on_message_delete(message):
    if 'a/' in message.content:
        pass
    else:
     embed = discord.Embed(title="Message Delete",
                          color=0xFF0000)
     if 'https://' in message.content:
        embed.add_field(name="Message", value=f"Message Was A [Link]({message.content})")

     else:    
      embed.add_field(name='Message', value=f"{message.content}",
                    inline=False)
     embed.add_field(
        name="Channel", value=f"{message.channel.mention}", inline=False)
     channel = bot.get_channel(858338176379781150)
     embed.set_author(name=f"{message.author}",
                     icon_url=f'{message.author.avatar_url}')
     global time_main
     embed.set_footer(
        text=f"Made By bean!!!!!!!#0041 For Moondog | Message ID: {message.id} â€¢ {time_main3}")
    
     await channel.send(embed=embed)


@bot.event
async def on_message_edit(message_before, message_after):
    if message_after == message_before:
        pass
    else:
    
     embed = discord.Embed(title="Message Edit",
                          description=f"[**Jump To Message**]({message_after.jump_url})", color=0xFF0000)
     embed.add_field(name='Old', value=f"{message_before.content}",
                    inline=False)
     embed.add_field(name="New", value=f"{message_after.content}",
                    inline=False)
     channel = bot.get_channel(858338176379781150)

     embed.set_author(name=f"{message_before.author}",
                     icon_url=f'{message_before.author.avatar_url}')

     global time_main3
     embed.set_footer(
        text=f"Made By bean!!!!!!!#0041 For Moondog | Message ID: {message_before.id} â€¢ {time_main3}")
     await channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
   if len(before.roles) < len(after.roles):
    channel = bot.get_channel(858338176379781150)
    b4_roles = before.roles
    after_roles = after.roles
    global time_main3
    global time_main2
    set_diffrence = set(after.roles) - set(b4_roles)
    list_diffrence = list(set_diffrence)
    role_name = [role.name for role in set_diffrence]
    string = role_name
    newrole = ' '.join([str(elem) for elem in string])
    embed = discord.Embed(
        title=f"{after} was given the `{newrole}` role", color=0xFF0000)
    embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
    embed.set_footer(
        text=f"Made By bean!!!!!!!#0041 For Moondog | ID: {after.id} â€¢ {time_main3} at {time_main2}")
    await channel.send(embed=embed)
   if len(before.roles) > len(after.roles):
    channel = bot.get_channel(858338176379781150)
    b4_roles = before.roles
    after_roles = after.roles
    set_diffrence = set(b4_roles) - set(after_roles)
    list_diffrence = list(set_diffrence)
    role_name = [role.name for role in set_diffrence]
    string = role_name
    newrole = ' '.join([str(elem) for elem in string])
    embed = discord.Embed(
        title=f"{after} lost the `{newrole}` role", color=0xFF0000)
    embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
    embed.set_footer(
        text=f"Made By bean!!!!!!!#0041 For Moondog | ID: {after.id} â€¢ {time_main3} at {time_main2}")
    await channel.send(embed=embed)




# @bot.event
# async def on_member_update(before, after):
#     channel = bot.get_channel(851965794446475274)
#     if str(after.status) == "offline":
#       if str(before.status) == str(after.status):
#        if str(after.name) == 'Sergioâ„¢':
#            pass
#        else: 
#         gone_offline_em = discord.Embed(
#             description=f"**`{after.name} Activity Changed`**", color=0xFF000)
#         await channel.send(embed=gone_offline_em)
#       else:
#         gone_offline_em = discord.Embed(
#             description=f"**`User Status Changed From {before.status}`**", color=0xFF000)
#         gone_offline_em.set_author(
#             name=f"{after.name} Went Offline", icon_url=f"{after.avatar_url}")
#         gone_offline_em.set_footer(text=f"User Status Changes | Moondog Logistics | ID: {after.id}")
#         await channel.send(embed=gone_offline_em)
    
#     if str(after.status) == "online":
#       if str(before.status) == str(after.status):
#        if str(after.name) == 'Sergioâ„¢':
#            pass
#        if str(after.name) in tracked_users:
#             gone_online_em_tracked = discord.Embed(
#             description=f"**`{after.name} is being tracked and came online`**", color=0xFF000)
#             await channel.send(embed=gone_online_em_tracked)     
#        else: 
        
#          gone_online_em = discord.Embed(
#             description=f"**`{after.name} Activity Changed`**", color=0xFF000)
#          await channel.send(embed=gone_online_em)
#       else:
#         gone_online_em = discord.Embed(
#             description=f"**`User Status Changed From {before.status}`**", color=0xFF000)
#         gone_online_em.set_author(name=f"{after.name} Came Online", icon_url=f"{after.avatar_url}")
#         gone_online_em.set_footer(text=f"User Status Changes | Moondog Logistics | ID: {after.id}")
#         await channel.send(embed=gone_online_em)
       
#     if str(after.status) == "dnd":
#       if str(before.status) == str(after.status):
#         gone_dnd_em = discord.Embed(
#             description=f"**`{after.name} Activity Changed`**", color=0xFF000)
#         await channel.send(embed=gone_dnd_em)    
#       else:
#         gone_dnd_em = discord.Embed(
#             description=f"**`User Status Changed From {before.status}`**", color=0xFF000)
#         gone_dnd_em.set_author(name=f"{after.name} Went DND", icon_url=f"{after.avatar_url}")
#         gone_dnd_em.set_footer(text=f"User Status Changes | Moondog Logistics | ID: {after.id}")
#         await channel.send(embed=gone_dnd_em)
    
    
#     if str(after.status) == "idle":
#       if str(before.status) == str(after.status):
#         gone_idle_em = discord.Embed(
#             description=f"**`{after.name} Activity Changed`**", color=0xFF000)
#         await channel.send(embed=gone_idle_em)
#       else:
#         gone_idle_em = discord.Embed(
#             description=f"**`User Status Changed From {before.status}`**", color=0xFF000)
#         gone_idle_em.set_author(
#             name=f"{after.name} Went Idle", icon_url=f"{after.avatar_url}")
#         gone_idle_em.set_footer(
#             text=f"User Status Changes | Moondog Logistics | ID: {after.id}")
#         await channel.send(embed=gone_idle_em)

#     # if str(after.status) == "online":
#     #  if 'Yzzoxi' in str(after.name):
#     #     bean = bot.get_user(755493797160288286)
#     #     await bean.send("Hey bean Yzxxoi came online")


# @bot.event
# async def on_message(message):
#      if message.content == '':
#          pass
#      else:    
#       channel = bot.get_channel(851965794446475274)
#       message_sent_em = discord.Embed(title="New Message Sent", color=0xFF000)
#       message_sent_em.add_field(
#           name="The Message:", value=f"`{message.content}` was sent by **`{message.author.name}`** in ***{message.channel.mention}***")
#       await channel.send(embed=message_sent_em)
#       await bot.process_commands(message)
#       if message.author == bot.user:
#         return

#       if message.content.startswith('hello'):
#         msg = 'Hi {0.author.mention}'.format(message)
#         await message.channel.send(msg)
#       if message.content.startswith('bye'):
#         msg = 'Bye {0.author.mention}'.format(message)
#         await message.channel.send(msg)
#       if message.content.startswith('bean'):
#         await message.delete()
#         msg2 = f"Message From Bean: You mentioned my name WHY??"
#         msg = f'Hey Bean, {message.author.mention} mentioned your name'
#         bean = bot.get_user(755493797160288286)
#         await bean.send(msg)
#         await message.channel.send(f"**{msg2}**") 
#       if message.content.startswith('trucker bean'):
#         await message.delete()
#         msg2 = f"Message From Bean: You mentioned my name WHY??"
#         msg = f'Hey Bean, {message.author.mention} mentioned your name'
#         bean = bot.get_user(755493797160288286)
#         await bean.send(msg)  
#         await message.channel.send(f"**{msg2}**") 

# fun commands e.g meme etc..python3 
@bot.command(pass_context=True)
async def meme(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Meme", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/rising.json') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children']
                            [random.randint(0, 30)]['data']['url'])
            await ctx.send(embed=embed)


@bot.command()
async def dodgydave(ctx, video="yes"):
        await ctx.message.delete()
        embed = discord.Embed(
            title="Dennis Skinner", description="`I Didn't receive a proper answer then. Maybe Dodgy Dave will answer it now.`", color=0xE4003B)
        if video == 'yes':
            pick = random.randint(1, 10)
            if pick < 5:
             embed.set_image(url="https://static.independent.co.uk/s3fs-public/thumbnails/image/2016/04/11/19/web-dennis-skinner-afp.jpg?width=1200")
            elif pick > 5:
                embed.set_image(
                    url="https://www.thetimes.co.uk/imageserver/image/%2Fmethode%2Ftimes%2Fprod%2Fweb%2Fbin%2F8ff0d1f2-93d9-11e7-a2ce-ce94682a575d.jpg?crop=2529%2C1423%2C52%2C21&resize=1180")
            elif pick == '5':
                embed.set_image(url="https://static.independent.co.uk/s3fs-public/thumbnails/image/2016/04/11/19/web-dennis-skinner-afp.jpg?width=1200")
            embed.add_field(name="Watch The Video ", value=f"[Here](https://www.youtube.com/watch?v=qvIUa47x_Oc)")
            print(pick)
        await ctx.send(embed=embed)        


@bot.command()
async def avatar(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title=f"Your Avatar Is Below. Enjoy :slight_smile:", color=0xFF000)
    embed.set_image(url=f"{ctx.author.avatar_url}")  
    await ctx.send(embed=embed)



@bot.command()
async def dadjoke(ctx):
    await ctx.message.delete()
    url = "https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes"
    r = requests.get(url)
    data = r.json()
    for setup in data:
         
     dad_joke_em = discord.Embed(
         title=f"Dad Jokes", description=f"Joke = ***`{data['setup']}`***", color=0xFF000)
     dad_joke_em.add_field(name=f"Punchline", value=f"**`{data['punchline']}`**", inline=False)
     dad_joke_em.add_field(name=f"Joke Type", value=f"{data['type']}", inline=False)
     dad_joke_em.add_field(
         name=f"Joke Author:", value="`KegenGuyll`. View there [Github Profile.](https://github.com/KegenGuyll/)", inline=False)
     dad_joke_em.set_footer(text=f"Dad Jokes by KegenGuyll | Joke Requested By: {ctx.author.name}")
    await ctx.send(embed=dad_joke_em)


@bot.command()
async def joke(ctx):
    await ctx.message.delete()
    url = 'https://official-joke-api.appspot.com/random_joke'
    r = requests.get(url)
    data = r.json()
    for setup in data:
       joke_em = discord.Embed(title="Jokes", description=f"Joke = ***`{data['setup']}`***", color=0x00C5FF) 
       joke_em.add_field(
           name=f"Punchline", value=f"**`{data['punchline']}`**", inline=False)
       joke_em.add_field(name=f"Joke Type", value=f"{data['type']}", inline=False)
       joke_em.add_field(
           name="Joke Author", value="`15Dkatz`. View there [Github Profile.](https://github.com/15Dkatz/)")
       joke_em.set_footer(
           text=f"Jokes by 15Dkatz | Joke Requested By: {ctx.author.name}")
    await ctx.send(embed=joke_em)


@bot.command()
async def unsupportedgv(ctx):
    await ctx.message.delete()
    getplayerinfourl = f"https://api.truckersmp.com/v2/version"
    r = requests.get(getplayerinfourl)
    data = r.json()
    for server in data:
     embed = discord.Embed(title="Basic Tmp Support Help Commands",
                           description="To find out how to change your game version for `TMP` visit [Here](https://truckersmp.com/knowledge-base/article/26).", color=0x00993C)
     embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
     embed.set_footer(
         text=f"Made By bean!!!!!!!#0041 For Moondog | Current Supported Version: " + data['supported_game_version'])
    await ctx.send(embed=embed)


@bot.command()
async def installpromodstmp(ctx):
    await ctx.message.delete()
    getplayerinfourl = f"https://api.truckersmp.com/v2/version"
    r = requests.get(getplayerinfourl)
    data = r.json()
    for server in data:
     embed = discord.Embed(title="Basic Tmp Support Help Commands",
                           description=" For help installing Promods Europe for `TMP` visit [Here](https://truckersmp.com/knowledge-base/article/26).", color=0x00993C)
     embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
     embed.set_footer(
         text=f"Made By bean!!!!!!!#0041 For Moondog | For more help contact ProMods Support.")
    embed.set_footer(
        text=f"Made By bean!!!!!!!#0041 For Moondog | For more help contact a member of **staff**.")
    await ctx.send(embed=embed)


@bot.command()
async def whatistmpid(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Basic Tmp Support Help Commands",
                          description="Your TMP ID is the ID on your profile it will look something like this. (look at image below)", color=0x00993C)
    embed.set_thumbnail(url='https://truckersmp.com/assets/img/avatar.png')
    embed.set_image(
        url="https://i.gyazo.com/ac91fdb0fc5f124be1d8e5ab757a4c75.png")
    await ctx.send(embed=embed)



# new admin commands and user montioring system
@bot.command()
async def track(ctx, user: discord.Member):
    await ctx.message.delete()
    global tracked_users
    tracked_users.append(f"{user.name}",)
    print(tracked_users)

@bot.command()
async def currenttrackedusers(ctx):
    await ctx.message.delete()
    sys.modules.clear()
    global tracked_users
    if tracked_users == []:
       await ctx.send('The Tracked Users List Is Currently Empty')
    listToStr = ' '.join([str(elem) for elem in tracked_users])
    await ctx.send(listToStr)

# test system for getting role hex colors 
@bot.command()
async def roles_colors(ctx):
    for role in ctx.guild.roles:
      if '@everone' in role.name:
          pass  
      await ctx.send(f"`{role.name}`")
      await ctx.send(role.color)




# new upates around job logging 
company_ID = int(10927)

@bot.command()
async def company_info(ctx, all='no'):
      await ctx.message.delete()
      global company_ID
      if all == 'yes':
          # do something
          company_info_url = f'https://api.vtlog.net/v3/companies/10927'
          r = requests.get(company_info_url)
          data = r.json()
          for response in data:
              data_em = discord.Embed(title=f"{data['response']['name']}'s Info", color=0xFF000)
              data_em.add_field(name="Subdomain:", value=f"[Link](https://allegroup.vtlog.net/)")
              data_em.add_field(
                  name="Website:", value=f"[Link](https://alle-group.com/)")
              data_em.set_thumbnail(url=f"{data['response']['avatar']}")
          await ctx.send(embed=data_em) 

      elif all == 'no':
          # do something
          
          await ctx.send(f"You have selected `No` so we will only send the company ID: {company_ID}")
      else:
          await ctx.send(f"{all} is not an option")      



@bot.command()
async def view_jobs(ctx):
    await ctx.message.delete()
    global company_ID
    company_jobs_info_url = 'https://api.vtlog.net/v3/companies/10927/jobs'
    r = requests.get(company_jobs_info_url)
    data = r.json()
    for response in data:    
        jobs_em = discord.Embed(title="Moondog Logistics Jobs", color=0xFF000)
        jobs_em.add_field(name='UserName:', value=f"{data['response']['jobs']['username']}")
    await ctx.send(embed=jobs_em)    








# owner only commands
# @bot.commands(pass_context=True)
# async def bean_afk(ctx):
#     await ctx.message.delete()


# @bot.commands(pass_context=True)
# async def bean_not_afk(ctx):
#     await ctx.message.delete()


# start the bot
bot.run(token, bot=True)

