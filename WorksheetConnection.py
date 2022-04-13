from google.oauth2.service_account import Credentials
import gspread


class WorksheetConnectionException(Exception):
    pass


class AuthenticationFailed(WorksheetConnectionException):
    pass


class WorksheetConnection:
    def __init__(self, credential_file_path):
        self.file_name = self.sheet_name = None
        self.active_file = self.active_sheet = None

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_file(
            credential_file_path,
            scopes=scopes)

        try:
            self.gc = gspread.authorize(credentials)
        except AuthenticationFailed as e:
            print(f'Authentication failed: {e}')
            raise AuthenticationFailed
        else:
            print('Authenticated successfully.')

    def open_sheet(self, workbook, sheet):
        self.file_name = workbook
        self.sheet_name = sheet

        self.active_file = self.gc.open(workbook)
        try:
            self.active_sheet = self.active_file.worksheet(sheet)
        except TypeError:
            self.active_sheet = self.active_file.sheet1

        print(f'{self.file_name} is open for editing.')

    def get_cell_value(self, row, column):
        return self.active_sheet.cell(row, column).value

    def update_cell_value(self, row, column, value):
        self.active_sheet.update_cell(row, column, value)
