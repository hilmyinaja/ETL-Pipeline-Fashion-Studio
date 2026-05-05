import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def load_to_csv(df, file_name='products.csv'):
    try:
        df.to_csv(file_name, index=False)
        print(f"Data berhasil disimpan ke CSV: {file_name}")
    except Exception as e:
        print(f"Error menyimpan ke CSV: {e}")

def load_to_postgres(df, db_url, table_name='fashion_products'):
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL (Tabel: {table_name})")
    except Exception as e:
        print(f"Error menyimpan ke PostgreSQL: {e}")

def load_to_google_sheets(df, spreadsheet_id, range_name, credentials_file='google-sheets-api.json'):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        
        df_string = df.astype(str)
        values = [df_string.columns.values.tolist()] + df_string.values.tolist()
        body = {'values': values}
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, 
            range=range_name,
            valueInputOption='RAW', 
            body=body
        ).execute()
        
        print(f"Data berhasil disimpan ke Google Sheets ({result.get('updatedCells')} sel terupdate)")
    except Exception as e:
        print(f"Error menyimpan ke Google Sheets: {e}")

if __name__ == "__main__":
    from extract import scrape_data
    from transform import transform_data
    
    print("Menyiapkan data dummy dari pipeline...")
    raw_data = scrape_data(max_pages=2)
    clean_df = transform_data(raw_data)
    
    if clean_df is not None:
        print("\n--- Memulai Tahap Load ---")
        
        load_to_csv(clean_df, file_name='products.csv')
        # Format URL: postgresql://username:password@host:port/database_name
        # db_url = "postgresql://postgres:password@localhost:5432/fashion_db"
        # load_to_postgres(clean_df, db_url)
        
        # 3. Test ke Google Sheets (Butuh ID Spreadsheet dan file JSON)
        # SPREADSHEET_ID bisa didapat dari URL Google Sheets Anda
        # SHEET_RANGE = "Sheet1!A1"
        # load_to_google_sheets(clean_df, spreadsheet_id="ISI_DENGAN_ID_SHEET_ANDA", range_name="Sheet1!A1")