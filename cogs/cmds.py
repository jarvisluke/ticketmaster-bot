import discord
from discord import app_commands
from discord.ext import commands


# Ticket submission form
class TicketForm(discord.ui.Modal, title='Submit a new ticket'):
    subject = discord.ui.TextInput(label='Subject', style=discord.TextStyle.short)
    description = discord.ui.TextInput(label='Description', style=discord.TextStyle.paragraph)
    severity = discord.ui.TextInput(label='Severity (High, Medium, Low)', style=discord.TextStyle.short)

    # Called when modal is sent
    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        # Create ticket with provided data in database
        await interaction.response().send_message(content='Your ticket has been successfully created', ephemeral=True)


# Contains slash commands
class cmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Creates a form to submit a new ticket
    @app_commands.command(name='create_ticket', description='Creates a to submit a new ticket')
    async def create_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketForm())


# Called by Bot.setup_hook()
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(cmds(bot))
