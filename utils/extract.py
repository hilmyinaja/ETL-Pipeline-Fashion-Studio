import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_data(base_url="https://fashion-studio.dicoding.dev", max_pages=50):
    products = []
    try:
        for page in range(1, max_pages + 1):
            url = f"{base_url}/?page={page}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_cards = soup.find_all('div', class_='collection-card')
            
            for card in product_cards:
                # Title
                title_elem = card.find('h3', class_='product-title')
                title = title_elem.text.strip() if title_elem else None
                
                # Price
                price_container = card.find('div', class_='price-container')
                if price_container:
                    price_elem = price_container.find('span', class_='price')
                    price = price_elem.text.strip() if price_elem else None
                else:
                    price_elem = card.find('p', class_='price')
                    price = price_elem.text.strip() if price_elem else None
                
                details = card.find_all('p', style=lambda value: value and 'color: #777' in value)
                rating, colors, size, gender = None, None, None, None
                
                for detail in details:
                    text = detail.text.strip()
                    if 'Rating:' in text:
                        rating = text.replace('Rating:', '').replace('⭐', '').strip()
                    elif 'Colors' in text:
                        colors = text
                    elif 'Size:' in text:
                        size = text
                    elif 'Gender:' in text:
                        gender = text
                        
                scraped_at = datetime.now().isoformat()
                
                products.append({
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Colors': colors,
                    'Size': size,
                    'Gender': gender,
                    'Timestamp': scraped_at
                })
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None
        
    return products

if __name__ == "__main__":
    print("Memulai proses ekstraksi data")
    
    raw_data = scrape_data(max_pages=50) 
    
    if raw_data:
        print(f"Ekstraksi selesai. Berhasil mengambil {len(raw_data)} data.")
        
        df_preview = pd.DataFrame(raw_data)
        print(df_preview.head())
    else:
        print("Gagal mengekstrak data.")