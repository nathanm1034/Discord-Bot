import discord

class Button(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)