#discord locker bot by René Van Der Schueren

import discord
from datetime import datetime
from datetime import timedelta
import asyncio
import time

client = discord.Client()

log = ""

timeinput = float(input("duur in minuten?"))
timestamp = datetime.now() + timedelta(minutes=timeinput)
start = True
sendmessages = []

@client.event
async def on_ready():
    print('Lock started for {} minutes'.format(timeinput))
    text_channel_list = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    for i in text_channel_list:
        embed = discord.Embed(title="Locker", description="This channel is in lockdown for {} minutes.".format(timeinput), color=0xffff00)
        sendmessages.append(await i.send(embed=embed))


@client.event
async def on_message(message):
    global sendmessages
    global log
    global start
    if message.author != client.user and start:
        await message.delete()
        log += str(message.author) + "\n\n" + message.content + "\n------------\n"


async def timer(timing):
    global start
    global sendmessages
    while True:
        if datetime.now() > timing:
            start = False
            with open("log{}.txt".format(time.strftime("%Y%m%d-%H%M%S")), "w+") as f:
                f.write(log)
            text_channel_list = []
            for guild in client.guilds:
                for channel in guild.text_channels:
                    text_channel_list.append(channel)
            for i in text_channel_list:
                embed = discord.Embed(title="Locker",
                                      description="This channel is no longer in lockdown!".format(timeinput),
                                      color=0xffff00)
                sendmessages.append(await i.send(embed=embed))
            await asyncio.sleep(60)
            for i in sendmessages:
                await i.delete()
            client.close()
            exit(0)
        await asyncio.sleep(0.1)

client.loop.create_task(timer(timestamp))
client.run('token here')