import discord
from discord import app_commands
from discord.ext import commands
from query import get_techid, create_ticket


# TODO: create persistant button to generate TicketModal


# Contains slash commands
class slash_cmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Creates a form to submit a new ticket
    @app_commands.command(name='create_ticket', description='Creates a to submit a new ticket')
    async def create_ticket(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(TicketModal())


# Returns the channel from where the interaction was sent
async def get_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel or None:
    for channel in guild.channels:
        if channel.name == channel_name:
            return channel
    return None


# Ticket submission form
class TicketModal(discord.ui.Modal, title='Submit a new ticket'):
    subject = discord.ui.TextInput(label='Subject', style=discord.TextStyle.short)
    description = discord.ui.TextInput(label='Description', style=discord.TextStyle.paragraph)
    severity = discord.ui.TextInput(label='Severity (High, Medium, Low)', style=discord.TextStyle.short)

    # Casts severity to enumerated values in database
    def enumerate_severity(self):
        severity = str(self.severity).capitalize()[0]
        if severity == 'H':
            self.severity = 'High'
        elif severity == 'M':
            self.severity = 'Medium'
        elif severity == 'L':
            self.severity = 'Low'
        else:
            self.severity = None

    # Called when modal is submitted
    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.enumerate_severity()
        channel = await get_channel(interaction.guild, 'customer-tickets')
        # Checks edge cases
        if channel is None:
            print('ERROR: Missing text channel: "customer-ticket"')
            await interaction.response.send_message(content='Your ticket can not be submitted at this time')
        elif self.severity is None:
            await interaction.response.send_message(content='Your ticket could not be submitted, please try again')
        else:
            user = interaction.user
            # Creates embed with information about file and sends it to the customer-tickets channel
            embed = discord.Embed(title='Customer Support Ticket', color=discord.Color.green(), timestamp=interaction.created_at)
            embed.set_thumbnail(url=user.display_avatar)
            embed.add_field(name='User', value=user.mention)
            embed.add_field(name='Subject', value=self.subject)
            embed.add_field(name='Severity', value=self.severity)
            embed.add_field(name='Description', value=self.description)
            # Gets technician id and technician as Member object
            tech_id = get_techid()
            tech = interaction.guild.get_member(int(tech_id))
            await user.send(content='You have created a new ticket', embed=embed)
            await tech.send(content='You have been assigned a new ticket', embed=embed)
            await interaction.response.send_message(content='Your ticket has been successfully created')
            # Creates the ticket in the database
            create_ticket(user, tech_id, str(self.subject), str(self.description), self.severity)


# Called by Bot.setup_hook()
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(slash_cmd(bot))
