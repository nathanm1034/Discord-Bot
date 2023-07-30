import discord
import mysql.connector
import pytz
import os

from discord import option
from datetime import datetime
from pytz import timezone
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

# db = bot.create_group(name="db", guild_ids=guild)

async def createAccount(user):
    query = f"INSERT INTO `Bank` (ID, Name, Wallet, Bank, LastDaily, DailyStreak) VALUES ({user.id}, '{user.name}', 100.00, 0.00, NULL, 0)"
    bankCursor.execute(query)
    bank.commit()
    return

async def retrieveUserData(user):
    query = f"SELECT * FROM `Bank` WHERE ID = {user.id}"
    bankCursor.execute(query)
    data = bankCursor.fetchone()
    
    if data is None:
        await createAccount(user)
        bankCursor.execute(query)
        return bankCursor.fetchone()
    else:
        return data

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")   
  
@bot.command(description="See someone's bank balance.", guild_ids=guild)
@option(
    "user",
    description="See the balance of a specific user.",
    required=False,
    default=None
)
async def balance(ctx, user: discord.Member):
    if user is None:
        user = ctx.author
    data = await retrieveUserData(user)
    userWallet = data['Wallet']
    userBank = data['Bank']
    
    embed = discord.Embed(title=f"{user.name}'s Balance")
    embed.add_field(name="Wallet", value=f"${userWallet:.2f}")
    embed.add_field(name="Bank", value=f"${userBank:.2f}")
    await ctx.respond(embed=embed)
    
@bot.command(description="Withdraw money from your bank to your wallet.", guild_ids=guild)
@option(
    "amount",
    description="The amount you want to withdraw. Valid inputs are '1.23', '12.5%', 'max', 'half', etc.",
    required=True
)
async def withdraw(ctx, amount: str):
    user = ctx.author
    data = await retrieveUserData(user)
    userWallet = data['Wallet']
    userBank = data['Bank']
    
    if userBank == 0.00:
        await ctx.respond("You have nothing in your bank.")
        return
    
    amount = amount.strip()
    
    if amount.lower() in ["max", "all", "everything", "total", "whole", "full", "entire", "complete"]:
        amount = userBank
    elif amount.lower() in ["half", "mid", "halfway"]:
        amount = userBank * 100 // 2
        remainder = userBank * 100 % 2
        amount = (amount + remainder) / 100
    elif "%" in amount and amount.index("%") == len(amount) - 1 and amount.count("%") == 1:
        percentage = float(amount.strip("%"))
        if percentage <= 0:
            await ctx.respond("You must withdraw more than 0%.")
            return
        elif percentage > 100:
            await ctx.respond("You can't withdraw more than 100%.")
            return
        else:
            amount = round(percentage / 100 * userBank, 2)
    else:
        try:
            amount = float(amount)
        except: 
            await ctx.respond("Please enter a valid amount.")
            return
        
        if amount <= 0.00:
            await ctx.respond("You must withdraw more than $0.00.")
            return
        if amount > userBank:
            await ctx.respond("You don't have that much money in your bank.")
            return
    
    newWallet = userWallet + amount
    newBank = userBank - amount
    
    query = f"UPDATE `Bank` SET Wallet = {newWallet}, Bank = {newBank} WHERE ID = {data['ID']}"
    bankCursor.execute(query)
    bank.commit()
    
    await ctx.respond(f"Successfully withdrew ${amount:.2f} from your bank!")
    await ctx.send(f"Your new bank balance is ${newBank:.2f} and you new wallet balance is ${(newWallet):.2f}.")
    
@bot.command(description="Deposit money to your bank from your wallet.", guild_ids=guild)
@option(
    "amount",
    description="The amount you want to deposit. Valid inputs are '1.23', '12.5%', 'max', 'half', etc.",
    require=True
)
async def deposit(ctx, amount: str):
    user = ctx.author
    data = await retrieveUserData(user)
    userWallet = data['Wallet']
    userBank = data['Bank']
    
    if userWallet == 0.00:
        await ctx.respond("You have nothing in your wallet.")
        return
    
    amount = amount.strip()
    
    if amount.lower() in ["max", "all", "everything", "total", "whole", "full", "entire", "complete"]:
        amount = userWallet
    elif amount.lower() in ["half", "mid", "halfway"]:
        amount = userWallet * 100 // 2
        remainder = userWallet * 100 % 2
        amount = (amount + remainder) / 100
    elif "%" in amount and amount.index("%") == len(amount) - 1 and amount.count("%") == 1:
        percentage = float(amount.strip("%"))
        if percentage <= 0:
            await ctx.respond("You must deposit more than 0%.")
            return
        elif percentage > 100:
            await ctx.respond("You can't deposit more than 100%.")
            return
        else:
            amount = round(percentage / 100 * userWallet, 2)
    else:
        try:
            amount = float(amount)
        except:
            await ctx.respond("Please enter a valid amount.")
            return
    
        if amount <= 0.00:
            await ctx.respond("You must deposit more than $0.00.")
            return
        if amount > userWallet:
            await ctx.respond("You don't have that much money in your wallet")
            return
    
    newWallet = userWallet - amount
    newBank = userBank + amount
    
    query = f"UPDATE `Bank` SET Wallet = {newWallet}, Bank = {newBank} WHERE ID = {data['ID']}"
    bankCursor.execute(query)
    bank.commit()
    
    await ctx.respond(f"Successfully deposited ${amount:.2f} from your wallet!")
    await ctx.send(f"Your new bank balance is ${newBank:.2f} and you new wallet balance is ${(newWallet):.2f}.")
    
@bot.command(description="Claim some money once a day.  Claim several times in a row for a streak.", guild_ids=guild)
async def daily(ctx):
    user = ctx.author
    data = await retrieveUserData(user)
    lastDaily = data['LastDaily']
    dailyStreak = data['DailyStreak']
    centralTime = datetime.now().astimezone(timezone('US/Central'))
    
    if lastDaily is None or lastDaily.astimezone(timezone('US/central')).date() < centralTime.date():
        if lastDaily is not None and (centralTime.date() - lastDaily.astimezone(timezone('US/central')).date()).days == 1:
            dailyStreak += 1
        else:
            dailyStreak = 1
        
        formattedCentralTime = centralTime.strftime('%Y-%m-%d %H:%M:%S')
        query = f"UPDATE `Bank` SET LastDaily = '{formattedCentralTime}', DailyStreak = {dailyStreak} WHERE ID = {data['ID']}"
        bankCursor.execute(query)
        bank.commit()
        await ctx.respond(f"Congrats you claimed your daily reward! Your current streak is {dailyStreak}.")
    else:
        await ctx.respond("You have already claimed your daily reward today.")
   
bot.run(os.getenv('TOKEN'))

