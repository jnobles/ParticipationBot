from google.oauth2.service_account import Credentials
import gspread


# expects worksheet with headers
class WorksheetConnection:
    def __init__(self, file_name, sheet_name=0):
        self.file_name = file_name
        self.sheet_name = sheet_name
        # authenticate and connect with Google api
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_file(
            'participationbot-6278614d1e9c.json',
            scopes=scopes)

        gc = gspread.authorize(credentials)
        print('Authorized successfully.')

        self.open_file = gc.open(file_name)
        self.active_sheet = self.open_file.get_worksheet(0)
        print(f'{self.file_name} is open for editing.')

        self.column_headings = self.active_sheet.row_values(1)
        print(f'Available columns are: {self.column_headings}')

    def get_cell_value(self, row, column):
        column = self.column_headings.index(column) + 1
        row = row + 1
        return self.active_sheet.cell(row, column).value

    def update_cell_value(self, row, column, value):
        column = self.column_headings.index(column) + 1
        row = row + 1
        self.active_sheet.update_cell(row, column, value)
