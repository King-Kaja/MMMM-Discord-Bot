import discord
from dotenv import load_dotenv
import os
from discord import app_commands
import gsheet_integration as gs

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="user-initializer", description="Initializes user into the list")
async def nameInit(interaction: discord.Interaction, member: discord.Member):

    await interaction.response.defer()
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
async def fundTransfer(
    interaction: discord.Interaction,
    member: discord.Member,
    amount: float,
    description: str = "",
):
    await interaction.response.defer()
    # rmbr to add code to check for nonnumeral
    gs.transaction(interaction.user, member, amount, description)
    await interaction.followup.send(
        f"name: {member.name} display name: {member.display_name}"
    )


@tree.command(name="net-loan", description="net loan of a user")
async def fundTransfer(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    # rmbr to add code to check for nonnumeral
    embed = gs.loanTable(member)
    await interaction.followup.send(embed=embed)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(os.getenv("DISCORD_APP_API_KEY"))
