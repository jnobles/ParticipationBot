from google.oauth2.service_account import Credentials
import gspread


class WorksheetConnectionException(Exception):
    pass


class AuthenticationFailed(WorksheetConnectionException):
    pass


class WorksheetConnection:
    def __init__(self, credential_file_path):
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
        else:
            print('Authenticated with Google successfully.')

    def open_sheet(self, file, sheet=None):
        message = ''
        try:
            self.active_file = self.gc.open(file)
        except gspread.exceptions.SpreadsheetNotFound:
            message = f'{file} not found.'
        else:
            if sheet is None:
                self.active_sheet = self.active_file.sheet1
                message = f'{self.active_file.title} > {self.active_sheet.title} ' \
                          f'successfully opened for editing.'
            else:
                try:
                    self.active_sheet = self.active_file.worksheet(sheet)
                except gspread.exceptions.WorksheetNotFound:
                    message = f'{sheet} not found in {self.active_file.title}'
                else:
                    message = f'{self.active_file.title} > {self.active_sheet.title} ' \
                              f'successfully opened for editing.'
        return message

    def get_cell_value(self, row, column):
        return self.active_sheet.cell(row, column).value

    def update_cell_value(self, row, column, value):
        self.active_sheet.update_cell(row, column, value)
