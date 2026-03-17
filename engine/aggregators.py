import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")
BIZ_DATA = os.path.join(PROJECT_ROOT, "data", "processed", "combined_nyc_businesses.csv")
RENT_DATA = os.path.join(PROJECT_ROOT, "data", "processed", "zillow_rent_cleaned.csv")

def calculate_survival_metrics():
    df_biz = pd.read_csv(BIZ_DATA)
    df_rent = pd.read_csv(RENT_DATA)
    
    # Calculate zip health (stability)
    
    df_biz['license_creation_date'] = pd.to_datetime(df_biz['license_creation_date'])
    current_date = pd.to_datetime('today')
    df_biz['age_years'] = (current_date - pd.to_datetime(df_biz['license_creation_date'])).dt.days / 365.25    
    
    # calculate category density and velocity 
    zip_stats = df_biz.groupby('address_zip')['age_years'].agg(['mean', 'count']).reset_index()
    zip_stats.columns = ['address_zip', 'neighborhood_avg_age', 'total_biz_in_zip']
        
    one_year_ago = current_date - pd.Timedelta(days=365)
    recent = df_biz[df_biz['license_creation_date'] > one_year_ago]
    # Group businesses by ZIP and Category (category count)    
    density = df_biz.groupby(['address_zip', 'business_category']).size().reset_index(name='biz_count')
    
    # Openings in last year (velocity)
    
    
    velocity = recent.groupby(['address_zip', 'business_category']).size().reset_index(name='recent_openings')
    
    # Merge 
    final = pd.merge(density, df_rent, on='address_zip')
    final = pd.merge(final, zip_stats, on='address_zip')
    final = pd.merge(final, velocity, on=['address_zip', 'business_category'], how='left').fillna(0)
        
    # Metrics    
    # Calculate opportunity score (low score is better for newcomers)
    # More businesses - more competition; if rent is high - higher risk
    final['saturation_pct'] = (final['biz_count'] / final['total_biz_in_zip']) * 100
    
    final['opportunity_score'] = (final['neighborhood_avg_age']) / (final['avg_rent'] * (final['biz_count'] + 1))
    return final
    
def generate_neighborhood_summary(final_report):
    
    #Group to get avg health per area
    neighborhoods = final_report.groupby('address_zip').agg({
        'avg_rent': 'first',
        'neighborhood_avg_age': 'first',
        'recent_openings': 'sum',
        'biz_count': 'sum',
    }).reset_index()
    
    # Labels
    def label_neighborhood(row):
        # The gold mine - low rent, high stability, high velocity
        if row['avg_rent'] < 3000 and row['neighborhood_avg_age'] > 7 and row['recent_openings'] > 20:
            return "Gold Mine (Emerging & Stable)"
        
        # The Churn zone - high velocity but low stability
        if row['recent_openings'] > 30 and row['neighborhood_avg_age'] < 4:
            return "Churn Zone (High Turnover)"
        
        # The stronghold - high rent, high stability 
        if row['avg_rent'] > 4500 and row['neighborhood_avg_age'] > 10:
            return "Stronghold (Expensive but Proven)"
            
        return "Steady Market"   
    
    neighborhoods['neighborhood_type'] = neighborhoods.apply(label_neighborhood, axis=1)     
    
    # Top in industry per zip
    top_bets = final_report.sort_values('opportunity_score', ascending=False).groupby('address_zip').head(1)
    top_bets = top_bets[['address_zip', 'business_category']].rename(columns={'business_category': 'top_recommended_biz'})
    
    neighborhoods = pd.merge(neighborhoods, top_bets, on='address_zip', how='left')
    
    return neighborhoods


if __name__ == "__main__":
    master_data = calculate_survival_metrics()
    
    neighborhood_summary = generate_neighborhood_summary(master_data)
    
    # save to JSON
    master_data.to_json('../data/processed/industry_data.json', orient='records')
    neighborhood_summary.to_json('../data/processed/neighborhood_summary.json', orient='records')
    
    print("SUCCESS: Engine has generated the Full Intelligence Suite.")
    print(f"Top Neighborhood by Score: \n{neighborhood_summary.sort_values(by='neighborhood_avg_age', ascending=False).head(1)}")
    