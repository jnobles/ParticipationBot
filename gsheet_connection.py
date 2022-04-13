from google.oauth2.service_account import Credentials
import gspread

# authenticate and connect with Google api
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'participationbot-6278614d1e9c.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

# open spreadsheet for usage
sheet = gc.open('Aeth Participation Log')
worksheet = sheet.sheet1

sheetData = worksheet.get_all_values()


def add_participation(playerName, leads=0, events=0):
    if leads < 0 or events < 0:
        message = 'Cannot deduct point with this function, for safety'
        return message

    playerFound = False
    row = 1
    for row in range(1, len(sheetData)+1):
        if sheetData[row-1][0] == playerName:
            playerFound = True
            worksheet.update_cell(row, 3, int(sheetData[row-1][2]) + leads)
            worksheet.update_cell(row, 4, int(sheetData[row-1][3]) + events)
            break

    if playerFound:
        message = f'{playerName} gained {leads} point(s) for leading and {events} point(s) for participating.'
    else:
        message = f'{playerName} not found.  Failed to add {leads} point(s) for leading and {events} ' \
                  f'point(s) for participating.'

    return message


print(add_participation("inforussle.3817", 1, 2))

