'''
API Field Name: license_nbr	What it represents: Unique ID	Why we need it: To ensure we don't count the same business twice.
API Field Name: business_name	What it represents: Name	Why we need it: To identify the business.
API Field Name: industry_name	What it represents: Category	Why we need it: Crucial: To filter (e.g., "Restaurant" vs "Garage").
API Field Name: address_zip	What it represents: ZIP Code	Why we need it: The "Join Key" to link with Zillow and Census data.
API Field Name: address_borough	What it represents: Borough	Why we need it: For high-level dashboard filtering (Brooklyn, Queens, etc).
API Field Name: license_status	What it represents: Status	Why we need it: To filter for "Active" businesses only.
API Field Name: license_creation_date What it represents: Start Date	Why we need it: To calculate the "New Business Growth" over time.
API Field Name: latitude / longitude What it represents: Coordinates	Why we need it: For your JS Map.
'''

import pandas as pd
from sodapy import Socrata
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..", "..")
SAVE_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "combined_nyc_businesses.csv")


DATASET_ID = "w7w3-xahh"
DATASET_HEALTH = "43nn-pn8j"
'''
def get_nyc_data():
    client = Socrata("data.cityofnewyork.us", None)
    print("Connecting to NYC Open Data...")
    
    # This fetches just ONE row so we can look at the labels
    sample = client.get(DATASET_ID, limit=1)
    
    # This prints all the actual "API keys" for that row
    print("The actual column names are:")
    print(sample[0].keys())
    
    return None

'''

def get_nyc_dcwp_data():
    client = Socrata("data.cityofnewyork.us", None)
    
    print("Connecting to NYC Open Data...")
    
    # Fetching 2000 rows to start. 
    
    results = client.get(
        DATASET_ID, 
        limit=50000,        
        select="license_nbr, business_name, business_category, address_zip, license_status, license_creation_date"
    )
    
    # Turn the JSON results into a Pandas table (DataFrame)
    df = pd.DataFrame.from_records(results)
    
    # --- NEW CLEANING STEPS ---
    
    # Convert date string to datetime obj
    df['license_creation_date'] = pd.to_datetime(df['license_creation_date'])
    
    # Get only active businesses
    df = df[df['license_status'] == 'Active']
    
    #Remove rows with missing ZIP code    
    df = df.dropna(subset=['address_zip'])
    
    #Change ZIP to string
    df['address_zip'] = df['address_zip'].astype(str).str[:5]
    
    print(f"Success! Filtered down to {len(df)} active businesses.")
    #print(df['business_category'].value_counts().head(10))
    
    return df

def get_nyc_health_data():
    client = Socrata("data.cityofnewyork.us", None)
    print("Connecting to NYC Open Data...")
    
    results = client.get(
        DATASET_HEALTH, 
        limit=50000, 
        select="dba, cuisine_description, zipcode, inspection_date"
    )
    
    df = pd.DataFrame.from_records(results)

    # RENAME columns to match our first dataset
    df = df.rename(columns={
        'dba': 'business_name',
        'cuisine_description': 'business_category',
        'zipcode': 'address_zip',
        'inspection_date': 'license_creation_date'
    })

    # Cleaning
    df['license_creation_date'] = pd.to_datetime(df['license_creation_date'])
    df['address_zip'] = df['address_zip'].astype(str).str[:5]
    
    print(f"Health Data Success! Imported {len(df)} restaurants.")
    return df    
    
    

if __name__ == "__main__":
    df_general = get_nyc_dcwp_data()
    df_health = get_nyc_health_data()
    
    combined_df = pd.concat([df_general, df_health], ignore_index=True)

    combined_df.to_csv(SAVE_PATH, index=False)
    print("File saved to data/processed/combined_nyc_businesses.csv")
    