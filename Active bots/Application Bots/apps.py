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

intents = intents = discord.Intents.all()


# Bots token
token = 'ODM3ODAwNjk4MDY2MTA4NDM2.YIx0tA.QbeQPybTciQBMh69wiTmrUl9KhQ'

# Bots prefix
bot = commands.Bot(command_prefix=('a/'), intents=intents)
slash = SlashCommand(bot)
#global variables go here (if any)


# sending startup message to server
@bot.event
async def on_ready():
    startup_msg = bot.get_channel(844657769822945310)
    message = await startup_msg.send('Alle Applications Bot has started.')
    await asyncio.sleep(60)
    await message.delete()


#send a dm to every user new user.
@bot.event
async def on_member_join(member):
    bot_commands_channel = bot.get_channel(837712738636922920)
    await member.send(f'Welcome to Alle Group | If you would like to join our vtc do `a/apply` in {bot_commands_channel.mention}')


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
        ctx.guild.categories, name="| 𝐀𝐝𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐓𝐞𝐚𝐦")
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
                        description="To Become a driver at Alle Group we ask u submit an application. To do this, reply to all the messages the bot will send you one at a time **It could take up to 1 - 2 days for a application to be viewed.**")
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
    
    # checks to see if the user is a Diretor if they are then they will not be allowed to apply
    Diretor_role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
    if Diretor_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role = discord.Embed(
            title="Alle Group Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `director role` so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role.set_footer(
            text="Alle Group Applications | Apply Error Message • 2021")
        await ctx.author.send(embed=Member_has_too_high_role)
    # sends a embed message logging to staff-logs stating that they tried to apply 
        channel3 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_1 = discord.Embed(
            ttitle="Alle Group Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Director`**", color=0xFF0000)
        staff_log_messageing_1.set_footer(
            text="Alle Group Applications | Apply Logging Message • 2021")
        await channel3.send(embed=staff_log_messageing_1)
    
    # checks to see if the user is already a driver and then they dont need to apply / cant apply. If they are abusing the system then it will flag to the staff team.
    Drivers_role = discord.utils.get(ctx.guild.roles, id=837666217413967882)
    if Drivers_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role_2 = discord.Embed(
            title="Alle Group Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `drivers role` so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role_2.set_footer(
            text="Alle Group Applications | Apply Error Message • 2021")
        await ctx.author.send(embed=Member_has_too_high_role_2)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel2 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_2 = discord.Embed(
            title="Alle Group Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Driver`**", color=0xFF0000)
        staff_log_messageing_1.set_footer(
            text="Alle Group Applications | Apply Logging Message • 2021")
        await channel2.send(embed=staff_log_messageing_2)
    
    # checks to see if the user is a member of lower staff, however they should have the above role anyway :) 
    lower_staff_role = discord.utils.get(ctx.guild.roles, id=837606669830848523)
    if lower_staff_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role_3 = discord.Embed(
            title="Alle Group Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `lower staff` role so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role_3.set_footer(
            text="Alle Group Applications | Apply Error Message • 2021")
        await ctx.author.send(embed=Member_has_too_high_role_3)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel1 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_3 = discord.Embed(
            title="Alle Group Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Staff Team`**", color=0xFF0000)
        staff_log_messageing_3.set_footer(
            text="Alle Group Applications | Apply Logging Message • 2021")
        await channel1.send(embed=staff_log_messageing_3)
    
    
    await asyncio.sleep(20)

    def check(message):
        return message.author == ctx.author and message.channel == ticket_channel
    await ticket_channel.send(f"{ctx.author.mention}")
    question1_em = discord.Embed(
        title="Alle Group Applications | Question 1 ", description=f"Hey, {ctx.author.name} what is your name?", color=0xFF0000)
    question1_em.set_footer(
        text="Alle Group Applications | Question 1 • 2021")
    await ticket_channel.send(embed=question1_em)    
    msg = await bot.wait_for('message', check=check)
    response = (msg.content)
    question2_em = discord.Embed(
        title="Alle Group Applications | Question 2 ", description=f"Hey, {ctx.author.name} what is your TMPID?", color=0xFF0000)
    question2_em.set_footer(
        text="Alle Group Applications | Question 2 • 2021")
    await ticket_channel.send(embed=question2_em)
    msg2 = await bot.wait_for('message', check=check)
    response2 = (msg2.content)
    # question 3 removed due to no longer being needed
    question3_em = discord.Embed(
        title="Alle Group Applications | Question 3 ", description=f"Hey, {ctx.author.name} what country are you from?", color=0xFF0000)
    question3_em.set_footer(
        text="Alle Group Applications | Question 3 • 2021")
    await ticket_channel.send(embed=question3_em)
    msg4 = await bot.wait_for('message', check=check)
    response4 = (msg4.content)
    question4_em = discord.Embed(
        title="Alle Group Applications | Question 4 ", description=f"Hey, {ctx.author.name} what is your age?", color=0xFF0000)
    question4_em.set_footer(
        text="Alle Group Applications | Question 4 • 2021")
    await ticket_channel.send(embed=question4_em)
    msg5 = await bot.wait_for('message', check=check)
    response5 = (msg5.content)
    
     #checks if they are older then 
    #if msg5.content < 16: 
        #your_not_old_enough = discord.Embed(
          #  title="Alle Group Applications | Age Check ", description=f"Hey, {ctx.author.name} your application has been **`Automatically Denied`** as you are under the age of 16.", color=0xFF0000)
        #your_not_old_enough.set_footer(
        #text="Alle Group Applications | Age Check • 2021")
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




    await ticket_channel.send("Thanks for answering all questions :)")
    questionr = discord.Embed(title="Alle Group Applications",
                              description=f"Name = {response}, TMPID = {response2},  Country = {response4}, Age = {response5}")
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
            title="Alle Group Applications | `blacklist` error", description=f"That person is already blacklisted. DiscordID: {ctx.author.id}", color=0xFF0000)
        await ticket_channel.send(embed=Member_already_blacklisted)
        you_are_blacklisted = discord.Embed(
            title="Alle Group Applications | Blacklist System", description=f"Your application with Alle Group has been **Automatically Denied** because  you are **blacklisted** from applying. If you attempt to evade this then you will be banned.", color=0xFF0000)
        you_are_blacklisted.set_footer(
            text=f"Alle Group Applications | Blacklist System • 2021")
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
     hook.send(embed=em2)
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
        em34 = discord.Embed(title=f":warning: DRIVER IS PERM BANNED :warning:", description=f"Someone has tired to apply when they are perm banned on TMP this was dected by Alles auto ban detection system. Drivers info TMP Name:" +
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
        userapplyed = discord.Embed(title="Alle Group Applications",
                                    description=f"Updated Mysql applications to 'closed'.")
        hook1.send(embed=userapplyed)
        hook1.send(
            f"{ticket_channel.mention} has been removed as the user had 5 bans.")
        ctx.author.send("Your application with Alle Group has been canceled. Reason: `5 bans or more` **This is a auto system action if this is wrong please contact a member of the upper staff team**")
        # Checks if user is already blacklisted (checks by discordID)

     else:
         pass
         print("channel not removed")

    except:
        em3 = discord.Embed(title="Player lookup (tmp) Error",
                            description="we could not lookup this user", color=0xFF0000)
        hook.send(embed=em3)
        error34 = discord.Embed(title="Alle Group Applications",
                                description=f"The TMPID you gave does not seem to exist or belongs to a diffrent user. TMPID = {response2}")
        await ticket_channel.send(embed=error34)

    warningmsg = discord.Embed(title="Alle Group Applications",
                               description=f"To see the status of your application do `a/status id` your Application ID is {ticket_number}")
    await asyncio.sleep(60)
    await ticket_channel.send(embed=warningmsg)



@apply.error
async def apply_handler_command_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}")
        # sends error if the command has not be used in a application ticket channel.
        apply_on_cooldown = discord.Embed(title="Alle Group Applications | `apply` error",
                                     description=f"Im sorry but at this time this command is on a cooldown please try again in {error.retry_after:.2f}s", color=0xFF0000)
        apply_on_cooldown.set_footer(
            text="Alle Group Applications |  apply error message • 2021")
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
                title="Alle Group Applications", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)

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
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Alle Group Applications | `close` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)


@close.error
async def close_handler_missing_arg(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # sends error if the command has not be used in a application ticket channel.
        provide_args = discord.Embed(title="Alle Group Applications | `close` error",
                                     description="Please include `id` and `member` at the end of the command `a/close`", color=0xFF0000)
        await ctx.send(embed=provide_args)


@close.error
async def close_handler(ctx, error):
    if isinstance(error, commands.BadArgument):
        no_member = discord.Embed(title="Alle Group Applications | `close` error",
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
                title="Alle Group Applications", description="Are you sure you want to hire this driver? Reply with `yes` if you are sure.", color=0x00a8ff)
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
            info1 = discord.Embed(title="Alle Group Applications",
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
            await member.send(f"{ctx.author} just updated your application at Alle Group to `Hired`")
            await member.send("Welcome to Alle Group Your role is `Probationary Driver`")
            channel1 = bot.get_channel(797186729232433193)
            #await channel1.send(f"Welcome to alle group {member.mention}. Please Book your training here https://alle-group.com/book-training/")
            hook = Webhook(
                'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
            em2 = discord.Embed(
                title=f"{member} has been promoted to Probationary Driver", description="")
            #hook.send(embed=em2)
            userapplyed = discord.Embed(title="Alle Group Applications",
                                        description=f"{ctx.author.mention} Hired {member.mention}")
            hook.send(embed=userapplyed)
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
                await asyncio.sleep(1008 * hours)
                await member.remove_roles(role3)
                await member.add_roles(role1)
                await member.add_roles(role2)
                joined_server = member.joined_at.strftime("%b %d, %Y")
                await member.send(f"Hey, your probation period is up congrats. You have been in Alle Groups Discord server since: {joined_server}")
            except:
                await ctx.send("oh it did not work")

            # Adding in #staff-logs logging for this bot!
            try:
                hire_log_msg = discord.Embed(
                    title="Alle | Applications", description=f"New driver hired by {ctx.author.mention} | Addded to the company api and database | Please add to the staff hub (coming soon!!)")
                staff_logs_channel = bot.get_channel(837715287092232264)
                await staff_logs_channel.send(embed=hire_log_msg)

            except:
                hire_log_err_msg = discord.Embed(
                    title="Alle | Applications | Error", descrition=f"Error could not send the log message to {staff_logs_channel.mention}.")
                await ctx.author.send(embed=hire_log_err_msg)

            # Add to staff hub message (send in dms).
            try:
                advice_msg = discord.Embed(
                    title="Alle | Applications", descrition=f"{member} | has been hired. | Please add them to the staff hub.")
                await ctx.author.send(embed=advice_msg)

            except:
                advice_msg_error = discord.Embed(
                    title="Alle | Applications", descrition=f"{ctx.author.mention} I tried to send you a msg in dms but i could not. pepesad")
                main_chat_channel = bot.get_channel(837713193672900688)
                await ctx.main_chat_channel.send(embed=advice_msg_error)

         #this will happen if it times out after 60 secs
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Alle Group Applications", description="You have run out of time to hire this driver. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Alle Group Applications | `hire` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)
  else:
      errormsg = discord.Embed(
          title="Alle Group applications", description="You do not have the correct roles or perms to use the command `hire`", color=0xFF0000
      )
      await ctx.send(embed=errormsg)


@hire.error
async def hire_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
       forgotiderr = discord.Embed(
           title="Alle Group Applications | `hire` error", description=f"This command requires the following arguments `id` `tmpid` `member` one of these are not present in your command `(a/hire application-id, tmpid, member(discord ping))`", color=0xFF0000)
    await ctx.send(embed=forgotiderr)


@hire.error
async def hire_handler2(ctx, error):
    if isinstance(error, commands.BadArgument):
        no_member = discord.Embed(title="Alle Group Applications | `close` error",
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
         does_not_have_role = discord.Embed(title="Alle Group Applications | `claim` error",
                                            description=f"This command can only be used by people with the `Director` Role", color=0xFF0000)
         await ctx.send(embed=does_not_have_role)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Alle Group Applications | `claim` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)


# send error if they do not provide a application id.
@claim.error
async def claim_handler2(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        forgotiderr = discord.Embed(
            title="Alle Group Applications | `claim` error", description=f"Please provide a `id`", color=0xFF0000)
    await ctx.send(embed=forgotiderr)


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
async def confirm(ctx, tmpid, status, date, time, server, orgin, destination, videourl):
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
     sql = "INSERT INTO trainings(tmpid, steamid, trainedby, videoevidence, traineename, status, date, time, server, orgin, destinaton) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
     val = (f"{tmpid}", data["steamID64"], f"{ctx.author}",
            f"{videourl}", data["name"],  f"{status}", f"{date}", f"{time}", f"{server}", f"{orgin}", f"{destination}")
    mycursor.execute(sql, val)
    mydb.commit()
    hook = Webhook(
        'https://discord.com/api/webhooks/825683286428483594/nQbl4rw8fBcD_Q1Ig9ceNgUsHy9lQ-EOtTwCCyYTges0W8J2OIPVpXNQl6rLCWrj4JhF')
    em2 = discord.Embed(
        title=data["name"], description=f"You have {status} your training", color=0x00FF00)
    hook.send(embed=em2)
    hook2 = webhook(
        'https: // discord.com/api/webhooks/833366266332708894/xoL7IBrAFGRpcUaIi2NMbLgEpQJqQ8nB-ogQe9AYEuJG2Tt9JQ8qOFBF1qvFtEHxLlq2'
    )
    em3 = discord.Embed(
        title=data["name"], description=f"Has passed there training. Trained by:{ctx.author}", color=0x00FF00)
    hook2.send(embed=em3)


# allows anyone to view a training that has been added to the DB.
@bot.command()
async def checkt(ctx, tmpid):
   try:
    gettraininginfourl = f'https://api-alle-group.com/api/v2/trainings{tmpid}'
    r = requests.get(gettraininginfourl)
    data = r.json()
    for data in data:
        embed = discord.Embed(title='Training Informaiton',
                              url=f'https://api-alle-group.com/api/v2/trainings{tmpid}', color=0xff0000)
        embed.add_field(name="Trainee Name",
                        value=data['traineename'], inline=False)
        embed.add_field(name='Trained By',
                        value=data['trainedby'], inline=False)
        embed.add_field(name='Status of Training',
                        value=data['status'], inline=False)
        embed.add_field(name='Date and Time',
                        value=f"{data['date']} {data['time']}", inline=False)
        embed.add_field(name='Server', value=data['server'], inline=False)
        embed.add_field(name='Training Origin and Destination',
                        value=f"Origin: {data['orgin']} | Destination: {data['destinaton']}", inline=False)
    try:
      await ctx.send(embed=embed)
    except:
        cannot_send_embed = discord.Embed(
            title="Alle Group Applications | `checkt` error", description=f"I cant send the results embed :(", color=0xFF0000)
        await ctx.send(embed=cannot_send_embed)
   except:
       cannot_find_training = discord.Embed(
           title="Alle Group Applications | `checkt` error", description=f"That training does not appear to exist :(", color=0xFF0000)
       await ctx.send(embed=cannot_find_training)


@checkt.error
async def checkt_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        cannot_find_training = discord.Embed(
            title="Alle Group Applications | `checkt` error", description=f"Please provide a `TMPID`", color=0xFF0000)
        await ctx.send(embed=cannot_find_training)


@bot.command()
async def wtrainings(ctx):
  await ctx.message.delete()
  role = discord.utils.get(ctx.guild.roles, id=794865611956158484)
  if role in ctx.author.roles:
    await ctx.author.send("To view all web booked trainings go to this link http://www.staff-alle-group.com/exams/training/staff/training/")
    await ctx.send("I've sent u a dm :) credit:`truckerbean`")
  else:
      await ctx.author.send("You dont have the right perms to use this command :(. If you think u need these perms then alert yzzoxi")


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

    cursor.execute(
        f"SELECT  discordid FROM blacklist WHERE discordid = '{discordid}'")
    results = cursor.fetchall()
    # gets the number of rows affected by the command executed
    row_count = cursor.rowcount
    if row_count > 0:
        Member_already_blacklisted = discord.Embed(
            title="Alle Group Applications | `blacklist` error", description=f"That person is already blacklisted. DiscordID: {discordid}", color=0xFF0000)
        await ctx.send(embed=Member_already_blacklisted)
    else:
        await ctx.send("Done")
        sql = "INSERT INTO blacklist(tmpname, discordid, tmpid, reason) VALUES (%s, %s, %s, %s)"
        val = (f"{tmpname}", f"{discordid}", f"{tmpid}", f"{reason}")
        cursor.execute(sql, val)
        # This will try to commit the above sql statement but if it there already is an entry then it will return an error.
        mydb.commit()
        Blacklisted_message = discord.Embed(title="Alle Group Applications | Blacklist System",
                            description=f"{ctx.author.mention}, Blacklisted the discord id {discord.id} from applying with Alle Group. More Info: TMPID: {tmpid}, Blacklist Reason: {reason}. **This action is irreversible**")
        Blacklisted_message.set_footer(text='Alle Group Applications |  Blacklist System • 2021')
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
    em = discord.Embed(
        title="Message From Alle | Admissions  Team", description=f"{message}")
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
        await member.send(f"Hey, your probation period is up congrats. You have been in Alle Groups Discord server since: {joined_server}")

    else:
        await ctx.send()


@finished.error
async def finished_handler2(ctx, error):
    if isinstance(error, commands.BadArgument):
        cant_find_member = discord.Embed(
            title="Alle Group Applications | `finished` error", description=f"I cant cant find that member in this guild :(", color=0xFF0000)
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


# start the bot
bot.run(token, bot=True)
