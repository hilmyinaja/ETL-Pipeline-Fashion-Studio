import unittest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_data

class TestExtract(unittest.TestCase):
    @patch('utils.extract.requests.get')
    def test_scrape_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<div class="collection-card"><h3 class="product-title">T-shirt Test</h3></div>'
        mock_get.return_value = mock_response

        # Tes hanya 1 halaman agar cepat
        result = scrape_data(max_pages=1)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Title'], 'T-shirt Test')

    @patch('utils.extract.requests.get')
    def test_scrape_data_failure(self, mock_get):
        # Simulasi error koneksi
        mock_get.side_effect = Exception("Connection Error")
        result = scrape_data(max_pages=1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()