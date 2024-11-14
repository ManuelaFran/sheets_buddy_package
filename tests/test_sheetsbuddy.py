import unittest
from sheetsbuddy import SheetsBuddy
import json


class TestSheetsBuddy(unittest.TestCase):
    def setUp(self):
        self.buddy = SheetsBuddy('path/to/credentials.json',
                                 '''https://docs.google.com/spreadsheets/d/
                                 your_sheet_id''')

    def test_add_formula(self):
        self.buddy.add_formula('A1', 'SUM(B1:B10)')
        cell_value = self.buddy.sheet.acell('A1').value
        self.assertEqual(cell_value, '=SUM(B1:B10)')

    def test_export_to_csv(self):
        self.buddy.export_to_csv('Sheet1', 'test.csv')
        with open('test.csv', 'r') as f:
            content = f.read()
            self.assertIn('Expected Value', content)

    def test_export_to_json(self):
        self.buddy.export_to_json('Sheet1', 'test.json')
        with open('test.json', 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()
