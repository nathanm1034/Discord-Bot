import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import option

from commands.ui import Button, View

class Job(commands.Cog):
    def __init__(self, bot, bank, bankCursor):
        self.bot = bot
        self.bank = bank
        self.bankCursor = bankCursor
        self.jobs = {
            "Fast Food Cashier": "Salary per shift: TBD \nRequired to unlock: None",
            "Job 2": "Salary: Temp \nUnlock: Temp",
            "Job 3": "Salary: Temp \nUnlock: Temp",
            "Job 4": "Salary: Temp \nUnlock: Temp",
            "Job 5": "Salary: Temp \nUnlock: Temp",
            "Job 6": "Salary: Temp \nUnlock: Temp"
        }
        
    job = SlashCommandGroup("job", guild_ids=[1131313562162319481])
         
    @job.command(description="Displays a list of jobs.")
    async def list(self, ctx):
        left = Button("<")
        right = Button(">")
        view = View()
        view.add_item(left)
        view.add_item(right)
        left.disabled = True
        counter = [0]
        
        async def leftCallback(interaction):
            if counter[0] > 0:
                counter[0] -= 2
                embed = discord.Embed(title=f"List of Jobs")
                for name, value in list(self.jobs.items())[counter[0]:counter[0]+2]:
                    embed.add_field(name=name, value=value, inline=False)
                
            if counter[0] == 0:
                left.disabled = True
            if view.children[1].disabled:
                view.children[1].disabled = False
                
            await interaction.response.edit_message(embed=embed, view=view)
        
        async def rightCallback(interaction):
            if counter[0] < len(self.jobs) - 2:
                counter[0] += 2
                embed = discord.Embed(title=f"List of Jobs")
                for name, value in list(self.jobs.items())[counter[0]:counter[0]+2]:
                    embed.add_field(name=name, value=value, inline=False)
                
            if counter[0] >= len(self.jobs) - 2:
                right.disabled = True
            if view.children[0].disabled:
                view.children[0].disabled = False
            
            await interaction.response.edit_message(embed=embed, view=view)
            
        left.callback = leftCallback
        right.callback = rightCallback
        
        embed = discord.Embed(title=f"List of Jobs")
        for name, value in list(self.jobs.items())[:2]:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.respond(embed=embed, view=view)
        
    @job.command(description="test apply")
    async def apply(self, ctx):
        await ctx.respond("Test apply")
        
    @job.command(description="test work")
    async def work(self, ctx):
        await ctx.respond("Test work")
    
    @job.command(description="test resign")
    async def resign(self, ctx):
        await ctx.respond("Test resign")
    