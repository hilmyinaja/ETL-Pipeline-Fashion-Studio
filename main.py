import os
from utils.extract import scrape_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_postgres, load_to_google_sheets

def run_pipeline():
    print("Memulai ETL Pipeline Fashion Studio")
    
    # Extract
    print("\n[1/3] Ekstraksi: Mengambil data dari website")
    raw_data = scrape_data(max_pages=50)
    
    if not raw_data:
        print("Gagal di tahap ekstraksi. Menghentikan pipeline.")
        return

    # Transform
    print(f"\n[2/3] Transformasi: Membersihkan {len(raw_data)} data...")
    clean_df = transform_data(raw_data)
    
    if clean_df is None or clean_df.empty:
        print("Gagal di tahap transformasi. Menghentikan pipeline.")
        return
    
    print(f"Transformasi selesai. Sisa data bersih: {len(clean_df)} baris.")

    # Load
    print("\n[3/3] Loading: Menyimpan data ke repositori...")
    
    load_to_csv(clean_df, 'products.csv')

    db_url = "postgresql://postgres:admin123@localhost:5432/fashion_db"
    load_to_postgres(clean_df, db_url)
    
    spreadsheet_id = "1IrqlGA1auFZ-1oUUytBx0eWiKkgjKfaoLxam5knaEwY"
    load_to_google_sheets(clean_df, spreadsheet_id, "Sheet1!A1")

    print("\nPipeline Berhasil Dijalankan!")

if __name__ == "__main__":
    run_pipeline()