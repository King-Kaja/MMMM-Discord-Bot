import pygsheets
import discord
from dotenv import load_dotenv
import os

load_dotenv()

gc = pygsheets.authorize(client_secret=os.getenv("GOOGLE_SHEET_SECRET_KEY"))

# Open spreadsheet and then worksheet
sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1wyD3Vs2y8V-BgMssBtY9KKhJvMRUWNUVhGzUj73U63s/edit?usp=sharing"
)
idSh = sh[0]
transSh = sh[1]
finanSh = sh[2]


def nameInit(user):
    """
    User is intialized into MMMM spreadsheet table

    Parameters
    ----------
    user : discord.Member
        The user
    """
    # initializes id List
    idSh.append_table([str(user.id)])
    index = idSh.find(str(user.id))[0].row

    # initalizes table with zero values
    zero_row = [0] * index
    finanSh.update_row(index, zero_row)
    finanSh.update_col(index, zero_row)
    # adds user's name to the table
    finanSh.update_value((1, index), user.name)
    finanSh.update_value((index, 1), user.name)


def checkInit(id):
    """
    Checks if user's ID number has already been initialized

    Parameters
    ----------
    id : str
        The user's id number

    Returns
    -------
    bool
        returns true if id is not intialized.
    """
    return idSh.find(id) == []


def transaction(lender, lendee, amount, description):
    """
    User is intialized into MMMM spreadsheet table

    Parameters
    ----------
    lender : discord.Member
        The user transfering the funds

    lendee: discord.Member
        The user that is being transferred the funds

    amount: float
        amount being transferred

    description: str
        optional description for purpose of transfer
    """
    lenderID = str(lender.id)
    lendeeID = str(lendee.id)
    lenderIndex = idSh.find(lenderID)[0].row
    lendeeIndex = idSh.find(lendeeID)[0].row

    # adds transaction to transaction log
    transSh.append_table([lenderID, lendeeID, amount, description])

    # updates values on table
    finanSh.update_value(
        (lenderIndex, lendeeIndex),
        float(finanSh.cell((lenderIndex, lendeeIndex)).value) + -1 * amount,
    )
    finanSh.update_value(
        (lendeeIndex, lenderIndex),
        float(finanSh.cell((lendeeIndex, lenderIndex)).value) + amount,
    )


def loanTable(member):
    """
    Returns a table with the net loan of a user

    Parameters
    ----------
    member : discord.Member
        The user

    Returns
    -------
    embed : discord.Ember
        returns embed with table of data
    """
    embed = discord.Embed(title="Net Loan")

    memberID = str(member.id)
    memberIndex = idSh.find(memberID)[0].row

    # removes the user's name from the entries
    nameList = finanSh.get_row(1, include_tailing_empty=False)[1:]
    valueList = finanSh.get_row(memberIndex, include_tailing_empty=False)[1:]

    # removes the user's loan to their self
    del nameList[memberIndex - 2]
    del valueList[memberIndex - 2]

    nameList = "\n".join(nameList)  # Joining the list with newline as the delimiter
    embed.add_field(name="users", value=nameList)

    valueList = "\n".join(valueList)  # Joining the list with newline as the delimiter
    embed.add_field(name="amount owed", value=valueList)

    return embed
