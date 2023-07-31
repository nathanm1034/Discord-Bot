import os
import discord
import mysql.connector
from dotenv import load_dotenv
from commands.economy import Economy

class Bot(discord.Bot):
    def __init__(self):
        super().__init__()
        self.bank = mysql.connector.connect(
            host="212.192.29.151",
            user="u102097_5FSL20P3iS",
            password="PoE12YLUwKBYj4ZCnh5@@UVy",
            database="s102097_Bank"
        )
        self.bankCursor = self.bank.cursor(dictionary=True)
        
        self.loadCommands()
        load_dotenv()
        
    def loadCommands(self):
        self.add_cog(Economy(self, self.bank, self.bankCursor))
        
    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        
    def run(self):
        super().run(os.getenv('TOKEN'))