import pandas as pd

def transform_data(raw_data):

    try:
        if isinstance(raw_data, list):
            df = pd.DataFrame(raw_data)
        else:
            df = raw_data.copy()

        df["Title"] = df["Title"].replace("Unknown Product", "Product Item")

        df["Price"] = (
            df["Price"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace("Price Unavailable", "NaN", regex=False)
        )
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce") * 16000 # Asumsi 1 USD = 16.000 IDR

        df["Rating"] = (
            df["Rating"]
            .astype(str)
            .str.replace(" / 5", "", regex=False)
            .str.replace("Invalid Rating", "NaN", regex=False)
            .str.replace("Not Rated", "NaN", regex=False)
        )
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        df["Colors"] = (
            df["Colors"].astype(str).str.extract(r"(\d+)").astype("Int64")
        )

        df["Size"] = (
            df["Size"]
            .astype(str)
            .str.replace("Size: ", "", regex=False)
            .str.strip()
        )
        df["Gender"] = (
            df["Gender"]
            .astype(str)
            .str.replace("Gender: ", "", regex=False)
            .str.strip()
        )

        df = df.dropna(subset=["Price", "Rating"])
        df = df.drop_duplicates(subset=["Title", "Price", "Rating", "Colors", "Size", "Gender"])

        df["Price"] = df["Price"].astype(float)
        df["Rating"] = df["Rating"].astype(float)
        df["Colors"] = df["Colors"].astype(int)

        return df

    except Exception as e:
        print(f"Terjadi kesalahan saat transformasi data: {e}")
        return None