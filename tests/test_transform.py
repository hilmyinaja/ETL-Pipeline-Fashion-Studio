import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    def setUp(self):
        # Data dummy kotor untuk skenario sukses (Happy Path)
        self.raw_data = [{
            'Title': 'T-shirt 2',
            'Price': '$10.00',
            'Rating': '4.0 / 5',
            'Colors': '3 Colors',
            'Size': 'Size: M',
            'Gender': 'Gender: Men'
        }, {
            'Title': 'Unknown Product', 
            'Price': 'Price Unavailable',
            'Rating': 'Invalid',
            'Colors': '1 Color',
            'Size': 'Size: S',
            'Gender': 'Gender: Women'
        }]

    def test_transformation_logic_success(self):
        df = transform_data(self.raw_data)
        
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['Price'], 160000.0)
        self.assertIsInstance(df.iloc[0]['Rating'], float)
        self.assertEqual(df.iloc[0]['Size'], 'M')

    # --- MISI 2: Uji Error (Negative Testing) ---
    def test_transform_error(self):
        # Sengaja mengirim integer untuk memicu Exception di Pandas
        bad_data = 123
        result = transform_data(bad_data)
        
        # Memastikan blok except tertangkap dan mengembalikan None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()