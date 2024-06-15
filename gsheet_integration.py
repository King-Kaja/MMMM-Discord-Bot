import pygsheets
import discord
from dotenv import load_dotenv
import os

load_dotenv()

gc = pygsheets.authorize(
    client_secret=os.getenv("GOOGLE_SHEET_SECRET_KEY")
)

# Open spreadsheet and then worksheet
sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1wyD3Vs2y8V-BgMssBtY9KKhJvMRUWNUVhGzUj73U63s/edit?usp=sharing"
)
idSh = sh[0]
transSh = sh[1]
finanSh = sh[2]


def test():
    print(idSh.find("allya2643")[0].row)


# intializes account
def nameInit(user):

    # initializes id List
    idSh.append_table([str(user.id)])
    index = idSh.find(str(user.id))[0].row

    zero_row = [0] * index
    finanSh.update_row(index, zero_row)
    finanSh.update_col(index, zero_row)
    finanSh.update_value((1, index), user.name)
    finanSh.update_value((index, 1), user.name)


# checks if id is in accounts
def checkInit(id):
    return idSh.find(id) == []


def transaction(lender, lendee, amount, description):
    lenderID = str(lender.id)
    lendeeID = str(lendee.id)
    lenderIndex = idSh.find(lenderID)[0].row
    lendeeIndex = idSh.find(lendeeID)[0].row

    transSh.append_table([lenderID, lendeeID, amount, description])

    finanSh.update_value(
        (lenderIndex, lendeeIndex),
        float(finanSh.cell((lenderIndex, lendeeIndex)).value) + -1 * amount,
    )
    finanSh.update_value(
        (lendeeIndex, lenderIndex),
        float(finanSh.cell((lendeeIndex, lenderIndex)).value) + amount,
    )


def loanTable(member):
    embed = discord.Embed(title="Net Loan")

    memberID = str(member.id)
    memberIndex = idSh.find(memberID)[0].row

    nameList = finanSh.get_row(1, include_tailing_empty=False)[1:]
    valueList = finanSh.get_row(memberIndex, include_tailing_empty=False)[1:]

    del nameList[memberIndex - 2]
    del valueList[memberIndex - 2]

    nameList = "\n".join(nameList)  # Joining the list with newline as the delimiter
    embed.add_field(name="users", value=nameList)

    valueList = "\n".join(valueList)  # Joining the list with newline as the delimiter
    embed.add_field(name="amount owed", value=valueList)

    return embed
