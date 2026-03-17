import pandas as pd

def get_rent_data():
    df = pd.read_csv('../../data/raw/zillow_rent.csv')
    print(df.head())
    

if __name__ == "__main__":
    get_rent_data()