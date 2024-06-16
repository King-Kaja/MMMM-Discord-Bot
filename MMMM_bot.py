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
    # checks if member is already in list before adding
    if gs.checkInit(str(member.id)):
        gs.nameInit(member)
    else:
        await interaction.followup.send(
            f"{member.mention} is already in the MMMMM group"
        )

    await interaction.followup.send(
        f"{member.mention} has been added into the MMMMM group."
    )


@tree.command(name="fund-transfer", description="transfers funds to user")
async def fundTransfer(
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

    # checks if member has already been intialized
    if gs.checkInit(str(interaction.user.id)):
        await interaction.followup.send(
            f"{interaction.mention} needs to be initialized into the MMMMM group"
        )
    elif gs.checkInit(str(member.id)):
        await interaction.followup.send(
            f"{member.mention} needs to be initialized into the MMMMM group"
        )
    # checks if amount is valid
    elif (amount * 100) % 1 != 0:
        await interaction.followup.send(
            f"{amount} is not valid. Amount must have at most 2 digits after the decimal point."
        )
    elif amount <= 0:
        await interaction.followup.send(
            f"{amount:.2f} is not valid. Amount must be greater than zero"
        )
    else:
        # adds transaction to sheet
        gs.transaction(interaction.user, member, amount, description)
        await interaction.followup.send(
            f"{interaction.user.mention} has transferred {amount} to {member.mention}"
        )


@tree.command(
    name="fund-transfer-split", description="splits funds and transfers them to user"
)
async def fundTransferSplit(
    interaction: discord.Interaction,
    members: str,
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

    # checks if member has already been intialized
    if gs.checkInit(str(interaction.user.id)):
        await interaction.followup.send(
            f"{interaction.mention} needs to be initialized into the MMMMM group"
        )
    # checks if amount is valid
    elif (amount * 100) % 1 != 0:
        await interaction.followup.send(
            f"{amount} is not valid. Amount must have at most 2 digits after the decimal point."
        )
    elif amount <= 0:
        await interaction.followup.send(
            f"{amount:.2f} is not valid. Amount must be greater than zero"
        )
    else:
        valid = True
        # splits and decrypts string into member ids
        memberList = members.split(" ")
        # splits amount
        amount = round(amount / len(memberList), 2)
        # checks if ids in list are valid
        for member in memberList:
            member_id = int(member.strip("<@!>"))
            if gs.checkInit(str(member_id)):
                await interaction.followup.send(
                    f"{interaction.mention} needs to be initialized into the MMMMM group"
                )
                valid = False
                break
        if valid:
            for member in memberList:
                # decrypts and adds transactions to sheet
                member_id = int(member.strip("<@!>"))
                member = await client.fetch_user(member_id)
                gs.transaction(interaction.user, member, amount, description)

            await interaction.followup.send(
                f"{interaction.user.mention} has transferred {amount} to {memberList}"
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
