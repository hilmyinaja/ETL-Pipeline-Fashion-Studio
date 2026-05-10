import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_postgres, load_to_google_sheets

class TestLoad(unittest.TestCase):
    def setUp(self):
        # DataFrame bersih tiruan
        self.df = pd.DataFrame({
            'Title': ['T-shirt'], 
            'Price': [160000.0], 
            'Rating': [4.5], 
            'Colors': [3], 
            'Size': ['M'], 
            'Gender': ['Men'], 
            'Timestamp': ['2026-05-10T12:00:00']
        })

    # --- 1. UJI LOAD CSV ---
    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv_success(self, mock_to_csv):
        load_to_csv(self.df, 'test.csv')
        mock_to_csv.assert_called_once_with('test.csv', index=False)

    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv_error(self, mock_to_csv):
        mock_to_csv.side_effect = Exception("Gagal tulis CSV")
        load_to_csv(self.df, 'test.csv') # Harusnya tidak crash karena ada try-except

    # --- 2. UJI LOAD POSTGRESQL ---
    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_load_to_postgres_success(self, mock_to_sql, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        load_to_postgres(self.df, 'postgresql://dummy_url', 'dummy_table')
        mock_to_sql.assert_called_once_with('dummy_table', mock_engine, if_exists='replace', index=False)

    @patch('utils.load.create_engine')
    def test_load_to_postgres_error(self, mock_create_engine):
        mock_create_engine.side_effect = Exception("Database error")
        load_to_postgres(self.df, 'postgresql://dummy_url')

    # --- 3. UJI LOAD GOOGLE SHEETS ---
    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_load_to_google_sheets_success(self, mock_creds, mock_build):
        # Menyiapkan rantai objek tiruan (mock) untuk merespons API Sheets
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        mock_spreadsheets = MagicMock()
        mock_service.spreadsheets.return_value = mock_spreadsheets
        
        mock_values = MagicMock()
        mock_spreadsheets.values.return_value = mock_values
        
        mock_update = MagicMock()
        mock_values.update.return_value = mock_update
        
        mock_update.execute.return_value = {'updatedCells': 7}
        
        load_to_google_sheets(self.df, 'dummy_sheet_id', 'Sheet1!A1', 'dummy.json')
        
        mock_creds.assert_called_once()
        mock_update.execute.assert_called_once()

    @patch('utils.load.Credentials.from_service_account_file')
    def test_load_to_google_sheets_error(self, mock_creds):
        mock_creds.side_effect = Exception("Kredensial error")
        load_to_google_sheets(self.df, 'dummy_sheet_id', 'Sheet1!A1', 'dummy.json')

if __name__ == '__main__':
    unittest.main()