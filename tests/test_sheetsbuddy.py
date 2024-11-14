import unittest
from unittest.mock import patch, MagicMock
from sheetsbuddy.sheetsbuddy import SheetsBuddy
import json


class TestSheetsBuddy(unittest.TestCase):
    def setUp(self):
        # Mock da autenticação e cliente do Google Sheets
        with patch('sheetsbuddy.sheetsbuddy.SheetsBuddy.authenticate',
                   return_value=MagicMock()) as mock_auth:
            self.mock_client = mock_auth.return_value
            self.mock_sheet = MagicMock()
            self.mock_client.open_by_url.return_value = self.mock_sheet

            # Mock para os métodos de retorno de valores
            self.mock_sheet.get_all_records.return_value = [{"Header": "Data"}]
            self.mock_sheet.get_all_values.return_value = [
                ["Header", "Data"], ["Value1", "Value2"]]

            self.buddy = SheetsBuddy('dummy/path/to/credentials.json',
                                     'dummy_sheet_url')

    def test_add_formula(self):
        # Mock do comportamento de adicionar fórmula
        self.mock_sheet.acell.return_value = MagicMock(value="=SUM(B1:B10)")
        self.buddy.add_formula("A1", "SUM(B1:B10)")
        cell_value = self.mock_sheet.acell("A1").value
        self.assertEqual(cell_value, "=SUM(B1:B10)")

    def test_export_to_csv(self):
        # Exportação simulada para CSV
        self.buddy.export_to_csv("Sheet1", "test.csv")
        with open("test.csv", "r") as f:
            content = f.read()
            self.assertIn("Header,Data", content)
            self.assertIn("Value1,Value2", content)

    def test_export_to_json(self):
        # Exportação simulada para JSON
        self.buddy.export_to_json("Sheet1", "test.json")
        with open("test.json", "r") as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(data[0]["Header"], "Data")


if __name__ == "__main__":
    unittest.main()
