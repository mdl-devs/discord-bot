import datetime
import time.time
import discord
from discord import user
import requests

getserversURL = "https://api.truckersmp.com/v2/servers"
gettimeURL = "https://api.truckersmp.com/v2/game_time"

client = discord.Client()

def transformTime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%c')
r = requests.get(getserversURL)
rt = requests.get(gettimeURL)

data = r.json()["response"]
for server in data:
    serverid = server["id"]
    game = server["game"]
    name = server["name"]
    players = str(server["players"])
    queue = str(server["queue"])
    maxplayers = str(server["maxplayers"])
    online = (server["online"])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bootup'):
        await message.channel.send('Booting up........Boot up complete! Welcome User!')
        await message.channel.send('..................')
        await message.channel.send('Boot up Complete! Welcome User!')
    
    if message.content.startswith('$serverstats'):
        if online:
            online = "Online"
        else:
            online = "Offline"


client.run('Nzk3NjE4MTQzMTczMjc5NzU0.X_pFyA.N75wby0uAALjGP-rFUCjIDYVSo0')