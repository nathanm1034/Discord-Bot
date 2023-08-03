import os
import discord
import mysql.connector
from dotenv import load_dotenv
from commands.economy import Economy
from commands.job import Job

class Bot(discord.Bot):
    def __init__(self):
        super().__init__()
        load_dotenv()
        
        self.bank = mysql.connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE')
        )
        self.bankCursor = self.bank.cursor(dictionary=True)
        self.loadCommands()
        
    def loadCommands(self):
        self.add_cog(Economy(self, self.bank, self.bankCursor))
        self.add_cog(Job(self, self.bank, self.bankCursor))
        
    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        self.add_view(View())
        
    def run(self):
        super().run(os.getenv('TOKEN'))