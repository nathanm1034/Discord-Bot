import discord
import os
# from discord.ext import commands
from dotenv import load_dotenv


bot = discord.Bot()
guild = [1131313562162319481]
load_dotenv()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")  
    
@bot.slash_command(name="ping", description="Test Ping", guild_ids=guild)
async def ping2(ctx):
    await ctx.respond("Pong!")
        
bot.run(os.getenv('TOKEN'))