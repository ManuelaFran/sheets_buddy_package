import gspread
from google.oauth2.service_account import Credentials


class SheetsBuddy:
    def __init__(self, creds_json, sheet_url):
        self.creds_json = creds_json
        self.sheet_url = sheet_url
        self.client = self.authenticate()
        self.sheet = self.open_sheet()

    def authenticate(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(self.creds_json,
                                                      scopes=scopes)
        client = gspread.authorize(creds)
        return client

    def open_sheet(self):
        return self.client.open_by_url(self.sheet_url)

    def add_formula(self, cell, formula):
        formatted_formula = formula.replace(',', ';')
        self.sheet.update(cell, f'={formatted_formula}')
