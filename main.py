import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    
@client.event
async def on_message(message):
    if message.content.startswidth('$hello'):
        await message.channel.send("Hello World")
        
client.run()