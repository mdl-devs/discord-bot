    def transformTime(timestamp):
     return datetime.datetime.fromtimestamp(timestamp).strftime('%c')
getserversURL = "https://api.truckersmp.com/v2/servers"
gettimeURL = "https://api.truckersmp.com/v2/game_time"
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
    if online:
      online = "Online"
    else:
      online = "Offline"
@bot.command()
async def servers(ctx):
  await ctx.message.delete()
  await ctx.send("---------")
  await ctx.send(name + " (" + game + ") - Status: " + online )
  await ctx.send("Drivers online: " , players + "/" + maxplayers)
  await ctx.send("Players in queue: " + queue)@bot.command()
