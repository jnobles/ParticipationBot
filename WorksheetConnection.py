from google.oauth2.service_account import Credentials
import numpy as np
import gspread


class PlayerNotFound(Exception):
    pass


class WorksheetConnection:
    def __init__(self, credential_file_path):
        self.active_file = self.active_sheet = None
        self.active_file_name = self.active_sheet_name = None
        self.sheet_values = None

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_file(
            credential_file_path,
            scopes=scopes)

        try:
            self.gc = gspread.authorize(credentials)
        except gspread.exceptions.GSpreadException:
            print(f'Authentication with Google failed.  Check that your key file is correctly defined.')
        else:
            print('Authenticated with Google successfully.')

    def open_sheet(self, file, sheet=None):
        message = ''
        try:
            self.active_file = self.gc.open(file)
            self.active_file_name = self.active_file.title
        except gspread.exceptions.SpreadsheetNotFound:
            message = f'{file} not found.'
        else:
            if sheet is None:
                self.active_sheet = self.active_file.sheet1
                self.active_sheet_name = self.active_sheet.title
                self.pull_sheet_values()
                message = f'{self.active_file_name} > {self.active_sheet_name} ' \
                          f'successfully opened for editing.'
            else:
                try:
                    self.active_sheet = self.active_file.worksheet(sheet)
                    self.active_sheet_name = self.active_sheet.title
                    self.pull_sheet_values()
                    message = f'{self.active_file_name} > {self.active_sheet_name} ' \
                              f'successfully opened for editing.'
                except gspread.exceptions.WorksheetNotFound:
                    message = f'{sheet} not found in {self.active_file_name}'
        return message

    def pull_sheet_values(self):
        self.sheet_values = np.array(self.active_sheet.get_all_values())

    def get_cell_value(self, row, column):
        return self.active_sheet.cell(row, column).value

    def update_cell_value(self, row, column, value):
        self.active_sheet.update_cell(row, column, value)

    def get_player_row_index(self, player_name):
        # todo: remove these magic numbers
        player_list = self.sheet_values[1::, [0, 1, 4]]
        row = 1
        for player in player_list:
            row += 1
            temp = []
            for item in player:
                for name in item.split('|'):
                    temp.append(name.strip())
            if player_name in temp:
                return row

        raise PlayerNotFound()
