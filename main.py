import discord
import os
import asyncio
import keep_alive
import urllib.parse
import giphypop
from discord.ext import commands
import requests
import json
import random
from itertools import cycle

client = discord.Client()

prefix = "/"

BotPresence = ["the BlackSun Castle.", "Toto by Africa", "The Lion Sleeps Tonight by The Tokens"]
BotPresenceType = ["type=3", "type=2", "type=2"]

async def change_status():
    await client.wait_until_ready()
    BotPmsg = cycle(BotPresence)
    BotPtype = cycle(BotPresenceType)

    while not Client.is_closed:
        current_status = next(BotPmsg)
        current_type = next(BotPtype)
        await client.change_presence(game=discord.Game(name=current_status, current_type))
        await asyncio.sleep(5)

@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    if message.content.startswith(prefix + "say"):
        args = message.content.split("say ",1)[1]
        await client.delete_message(message)
        await client.send_message(message.channel, args)
    else:
        if message.content.startswith(prefix + "gif"):
            GIPHY_TOKEN = os.environ.get("GIPHY_BOT_TOKEN")
            query = message.content.split("gif ",1)[1]
            index = 0
            giphy = giphypop.Giphy() if GIPHY_TOKEN == "" else giphypop.Giphy(api_key=GIPHY_TOKEN)
            gif = [x for x in giphy.search(query)][index]
            if gif:
                await client.delete_message(message)
                await client.send_message(message.channel, gif)
            else:
                await client.delete_message(message)

@client.event
async def on_member_join(member):
    memberid = member.mention
    #Mentions the joining member
    newMemMsg = ["The Grand Council welcomes you to BlackSun, " + memberid + ". I've called our <@&557738566017351690> to provide you with the necessary roles.", "Praise the Black Sun!" + memberid + "! On behalf of the Grand Council, I welcome you. Our @Deacon will provide you with your necessary role later.", "Welcome to BlackSun! " + memberid + "! Our hardworking <@&557738566017351690> will provide you with your necessary role. Praise the Grand Council! Praise the Black Sun!", "<@&551943300530044929> wishes you a warm welcome, " + memberid + ". <@&557738566017351690> , please provide our Visitor their necessary role. Praise the Black Sun!", "<@&552092427331305472> wishes you a warm welcome, " + memberid + ". <@&557738566017351690> , please provide our Visitor their necessary role. Praise the Black Sun!", "<@&552103644137390081>  wishes you a warm welcome, " + memberid + ". <@&557738566017351690> , please provide our Visitor their necessary role. Praise the Black Sun!", "The Grand Council wishes you a warm welcome, " + memberid + ". <@&557738566017351690> , please provide our Visitor their necessary role. Praise the Black Sun!", "On behalf of the Grand Council, I welcome you, " + memberid + ". Our <@&557738566017351690>  will provide you with your necessary role.", "The Black Sun welcomes you, " + memberid + ". Our <@&557738566017351690>  will provide you with your necessary role."]
    # <@&557738566017351690> @Deacons
    # <@&551943300530044929> @Grand Master
    # <@&552092427331305472> @Grand Marshal
    # <@&552103644137390081> @Grand Steward
    newMemMsgRand = random.choice(newMemMsg)
    newMemMsgLinks = """

In the meantime, please fill out this form:
https://forms.gle/ucakenwLAo36qPHX7
"""
    reception = member.server.get_channel("557712167869087746")
    logs = member.server.get_channel("564975917797998603")
    role = discord.utils.get(member.server.roles, id="552094477154779157")
    await client.send_message(reception, (newMemMsgRand) + newMemMsgLinks)
    await client.send_message(logs, newMemMsgRand)
    await client.add_roles(member, role)

@client.event
async def on_member_remove(member):
    memberuser = member.name
    leaveMsg = "The member " + memberuser + " has left the Black Sun, they are now alone in their journey."
    logs = member.server.get_channel("564975917797998603")
    await client.send_message(logs, leaveMsg)

client.loop.create_task(change_status())
client.loop.create_task(change_presence())
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
