import discord

# module for env variabls
from dotenv import load_dotenv
import os
from discord import app_commands

# access to google sheets functions
import gsheet_integration as gs

# loads env variables
load_dotenv()
#  initializes bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="user-initializer", description="Initializes user into the list")
async def nameInit(interaction: discord.Interaction, member: discord.Member):
    """
    Adds ID of user and intializes them into finances table.

    Parameters
    ----------
    member : discord.Member
        The user
    """
    await interaction.response.defer()
    # checks if cmember is already in list before adding
    if gs.checkInit(str(member.id)):
        gs.nameInit(member)
    else:
        await interaction.followup.send(
            f"{member.display_name} is already in the MMMMM group"
        )

    await interaction.followup.send(
        f"{member.display_name} has been added into the MMMMM group."
    )


@tree.command(name="fund-transfer", description="transfers funds to user")
async def fundTransferSplit(
    interaction: discord.Interaction,
    member: discord.Member,
    amount: float,
    description: str = "",
):
    """
    User that calls command ransfers funds to a user

    Parameters
    ----------
    member : discord.Member
        The user

    amount : float
        The amount that is owed by the user

    description: str
        Optional description for reason for transfer
    """
    await interaction.response.defer()
    # rmbr to add code to check for nonnumeral
    gs.transaction(interaction.user, member, amount, description)
    await interaction.followup.send(
        f"name: {member.name} display name: {member.display_name}"
    )


@tree.command(
    name="fund-transfer-split",
    description="splits funds and transfers to multiple users",
)
async def fundTransferSplit(
    interaction: discord.Interaction,
    member: discord.Member,
    amount: float,
    description: str = "",
):
    """
    User that calls command ransfers funds to a user

    Parameters
    ----------
    member : discord.Member
        The user

    amount : float
        The amount that is owed by the user

    description: str
        Optional description for reason for transfer
    """
    await interaction.response.defer()
    # rmbr to add code to check for nonnumeral
    gs.transaction(interaction.user, member, amount, description)
    await interaction.followup.send(
        f"name: {member.name} display name: {member.display_name}"
    )


@tree.command(name="net-loan", description="net loan of a user")
async def netLoan(interaction: discord.Interaction, member: discord.Member):
    """
    User that calls command ransfers funds to a user

    Parameters
    ----------
    member : discord.Member
        The user

    amount : float
        The amount that is owed by the user

    description: str
        Optional description for reason for transfer
    """
    await interaction.response.defer()
    # makes embed from table
    embed = gs.loanTable(member)
    await interaction.followup.send(embed=embed)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(os.getenv("DISCORD_APP_API_KEY"))
