import pandas as pd

def transform_data(raw_data):
    try:
        if isinstance(raw_data, list):
            df = pd.DataFrame(raw_data)
        else:
            df = raw_data.copy()

        df = df.drop_duplicates()

        df = df.dropna()

        df = df[
            (df['Title'] != 'Unknown Product') & 
            (df['Price'] != 'Price Unavailable') & 
            (~df['Rating'].str.contains('Invalid|Not', na=False))
        ]

        df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float) * 16000 # Asumsi 1 USD = 16,000 IDR

        df['Rating'] = df['Rating'].str.replace(' / 5', '', regex=False).astype(float)

        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)

        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False).str.strip()

        return df

    except Exception as e:
        print(f"Terjadi kesalahan saat transformasi data: {e}")
        return None