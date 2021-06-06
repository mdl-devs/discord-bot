from dhooks import Webhook
from discord.ext.commands import CommandNotFound
from discord import Client
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

#Token Command
token = "ODIxMzY2NDg2NDUzOTc3MTA5.YFCrJg.voB8yvcVVx0IgUtbBR7kotIk-PQ"
#Bot Starting Command
bot = commands.Bot(command_prefix='sa/')
#Removing Help Command Again
bot.remove_command('help')
#Global Veriable (webhook for now)
hook = Webhook('https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')

@bot.command()
async def apply(ctx, *, args=None):
    await ctx.message.delete()
    await bot.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"

    else:
        message_content = "".join(args)

    with open("data3.json") as f:
        data = json.load(f)

    ticket_number = data["staff-ticket-counter"]
    ticket_number += 1
    category = discord.utils.get(ctx.guild.categories, name="Applications")
    ticket_channel = await ctx.guild.create_text_channel("staff-application-{}".format(ticket_number), category=category)
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=True)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New Staff application from {}#{}".format(ctx.author.name, ctx.author.discriminator), description="{}".format(message_content), color=0x00a8ff)
    await ticket_channel.send(embed=em)
    em2 = discord.Embed(title="Welcome to Alle Groups Applications System",
                        description="To become apart of the staff team here at Alle Group, we ask you to submit an applicaiton. To do this, reply to this message answering in this template ```Your TMP name = ________  Your TMP ID = _________ Your Steam ID = _________ What department are you applying for (e.g Development) = ________ what country/timezone are you from = ________ Your age = _________``` Once you have completed this, A member of the Upper Staff Team will reply and take your application further. **It could take awhile for you application to be viewed and processed.**")
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

    data["ticket-channel-ids"].append(ticket_channel)

    data["ticket-counter"] = int(ticket_number)
    
    created_em = discord.Embed(title="Alle Group Applications", description="Your application ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)

    await ctx.send(embed=created_em)

@bot.command()
async def close(ctx):
    with open("data3.json") as f:
        data = json.load(f)

    if ctx.channel.id in data['ticket-channel-ids']:
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

          except asyncio.TimeoutError:
              em = discord.Embed(
                  title="Alle Group Applications", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
              await asyncio.sleep(60)
              await ctx.send(embed=em)

@bot.command()
async def accept(ctx):
    await ctx.message.delete()
    with open('data3.json') as f:
        data = json.load(f)
    if ctx.channel.id is data['ticket-channel-ids']:
        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "yes"
        try:
            em = discord.Embed(
                title="Alle Group Applications", description="Are you sure you want to accept this staff applicaiton? Reply with `yes` if you are sure.", color=0x00a8ff)
            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            

            with open("data3.json", 'w') as f:
                json.dump(data, f)
            role = discord.utils.get(ctx.guild.roles, name="Trainee Staff")
            
            await member.send(f"{ctx.author} just updated your Staff Application to `Accepted`")
            await member.send("Welcome to the Alle Staff Team! Your role is now `Trainee Staff`")
            await member.send("A member will inform you about the Staff Discord link and more information that will be necessary.")
            em2 = discord.Embed(
                title=f'{member.mention} has been promoted to Trainee Staff!')
            await hook.send(embed=em2)
            await ctx.send("New Trainee Staff member has been informed and Trainee Role Added")
            await asyncio.sleep(40)
            await ctx.channel.delete()
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Alle Group Applications", description="The Apply command has expired. Please try again.", color=0x00a8ff)
            await ctx.send(embed=em)

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
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} just claimed your application request! Said person will respond soon!")
    channel1 = bot.get_channel(794888270923300884)
    await channel1.send(f"{ctx.author.mention} just claimed staff application {id}.")

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
async def decline(ctx, *, reason):
    em = discord.Embed(
        title="Alle Group Applications", description=f"Your application for staff has been declineded for provided reason `{reason}`. Please try again another time!")
    await ctx.send(embed=em)
    em2 = discord.Embed(
        title=f"{ctx.author} has denied a staff application", description=f"Mention: {ctx.author.mention}")
    channel1 = bot.get_channel(794888270923300884)
    await channel1.send(embed=em2)

@bot.command()
async def reply(ctx, *, reply):
    await ctx.message.send()
    em = discord.Embed(
        title="New reply from staff", description=reply)
    await ctx.send(embed=em)

#Ping Command
@bot.command()
async def ping(ctx):
  await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')

#Bot Run Command (do not mess)
bot.run(token, bot=True)

