import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..","..")
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", 'raw', "zillow_rent.csv")

def get_rent_data():
    
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: Could not find {RAW_DATA_PATH}")
        return None
    df = pd.read_csv(RAW_DATA_PATH)
    #print(df.columns)
    
    #get NYC
    df_nyc = df[df['City'] == 'New York'].copy()
    
    # Get RegionName (zip code) and last column (rent)
    df_final = df_nyc.iloc[:, [2, -1]]
    
    # Rename columns
    df_final.columns = ['address_zip', 'avg_rent']
    
    # Turn zip codes into str
    df_final['address_zip'] = df_final['address_zip'].astype(str)
    
    # Remove rows without rent $$$
    df_final = df_final.dropna(subset=['avg_rent'])
    
    print(f"Zillow Data Success! Found rent for {len(df_final)} NYC ZIP codes.")
    print(df_final.head())
    return df_final

if __name__ == "__main__":
    rent_df = get_rent_data()
    if rent_df is not None:
        save_path = os.path.join(PROJECT_ROOT, "data", "processed", "zillow_rent_cleaned.csv")
        rent_df.to_csv(save_path, index=False)
        print(f"Saved to {save_path}")