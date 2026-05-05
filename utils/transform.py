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

if __name__ == "__main__":
    from extract import scrape_data
    
    print("Mengekstrak data untuk testing transformasi...")
    raw_data = scrape_data(max_pages=5)
    
    if raw_data:
        print("Data mentah berhasil didapat. Memulai transformasi...")
        clean_df = transform_data(raw_data)
        
        if clean_df is not None:
            print(f"Transformasi selesai. Sisa data bersih: {len(clean_df)} baris.")
            print(clean_df.head())
            print("\n--- Info DataFrame (Tipe Data) ---")
            clean_df.info()
        else:
            print("Gagal melakukan transformasi.")