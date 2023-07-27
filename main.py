import discord
import mysql.connector
import os
from discord import option
from dotenv import load_dotenv # for local hosting

bank = mysql.connector.connect(
    host="212.192.29.151",
    user="u102097_5FSL20P3iS",
    password="PoE12YLUwKBYj4ZCnh5@@UVy",
    database="s102097_Bank"
)

bankCursor = bank.cursor(dictionary=True)

guild = [1131313562162319481]
bot = discord.Bot(guild_ids=guild)
load_dotenv() # for local hosting

db = bot.create_group(name="db", guild_ids=guild)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")   
  
@db.command(description="Create Account")
async def create(ctx):
    userID = ctx.author.id
    bankCursor.execute(f"SELECT * FROM `Bank Test` WHERE ID = {userID}")
    user = bankCursor.fetchone()
    
    if user is None:
        query = f"INSERT INTO `Bank Test` (ID, Balance) VALUES ({userID}, 0)"
        bankCursor.execute(query)
        bank.commit()
        await ctx.respond("Account created")
    else:
        await ctx.respond("Account already exist")
    
    
@db.command(description="Add Money")
@option(
    "amount",
    description="Enter balance",
    required=False,
    default=500
)
async def insert(ctx, amount: int):
    userID = ctx.author.id
    bankCursor.execute(f"SELECT * FROM `Bank Test` WHERE ID = {userID}")
    user = bankCursor.fetchone()
    
    if user is not None:
        newBalance = user['Balance'] + amount
        query = f"UPDATE `Bank Test` SET Balance = {newBalance} WHERE ID = {userID}"
        bankCursor.execute(query)
        bank.commit()
        await ctx.respond(f"Your new balance is {newBalance}")
    else:
        await ctx.respond(f"Create an account first")
    
@db.command()
async def fetch(ctx):
    userID = ctx.author.id
    bankCursor.execute(f"SELECT * FROM `Bank Test` WHERE ID = {userID}")
    user = bankCursor.fetchone()
    
    if user is not None:
        currentBalance = user['Balance']
        await ctx.respond(f"Your current balance is {currentBalance}")
    else:
        await ctx.respond(f"Create an account first")

@db.command()
async def delete(ctx):
    userID = ctx.author.id
    bankCursor.execute(f"SELECT * FROM `Bank Test` WHERE ID = {userID}")
    user = bankCursor.fetchone()
    
    if user is not None:
        query = f"DELETE FROM `Bank Test` WHERE ID = {userID}"
        bankCursor.execute(query)
        bank.commit()
        await ctx.respond("Account deleted")
    else:
        await ctx.respond(f"Nothing to delete")

bot.run(os.getenv('TOKEN'))