import gspread
from google.oauth2.service_account import Credentials
import csv
import json


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

    def apply_bulk_formatting(self, cell_range, color=None, bold=None,
                              font_size=None):
        cell_list = self.sheet.range(cell_range)

        requests = []
        if color:
            requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': self.sheet.id,
                        'startRowIndex': cell_list[0].row - 1,
                        'endRowIndex': cell_list[-1].row,
                        'startColumnIndex': cell_list[0].col - 1,
                        'endColumnIndex': cell_list[-1].col,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': color
                        }
                    },
                    'fields': 'userEnteredFormat.backgroundColor'
                }
            })
        if bold or font_size:
            cell_format = {}
            if bold is not None:
                cell_format['bold'] = bold
            if font_size is not None:
                cell_format['font_size'] = font_size
            requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': self.sheet.id,
                        'startRowIndex': cell_list[0].row - 1,
                        'endRowIndex': cell_list[-1].row,
                        'startColumnIndex': cell_list[0].col - 1,
                        'endColumnIndex': cell_list[-1].col
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': cell_format
                        }
                    },
                    'fields': 'userEnteredFormat.textFormat'
                }
            })

        if requests:
            body = {
                'requests': requests
            }
            self.client.request(
                'POST',
                f'''https://sheets.googleapis.com/v4/spreadsheets/{self.sheet.id}
                :batchUpdate''',
                json=body
            )

    def export_to_csv(self, sheet_name, filename):
        worksheet = self.sheet.worksheet(sheet_name)
        data = worksheet.get_all_values()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def export_to_json(self, sheet_name, filename):
        worksheet = self.sheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
