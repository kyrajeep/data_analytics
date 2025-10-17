import requests
import pandas as pd

def load_places_data():
    """
    Load places data from all states for stroke measure.
    """
    # Load the CSV file into a DataFrame
    base_url = "https://chronicdata.cdc.gov/resource/cwsq-ngmh.json"
    states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN',
          'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV',
          'NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN',
          'TX','UT','VT','VA','WA','WV','WI','WY']

    """all_data = []
    for s in states:
        params = {"$where": "measureid='STROKE'", "stateabbr": s, "$limit": 50000, "$offset": 0}
        r = requests.get(base_url, params=params)
    data = r.json()
    if data:
        all_data.extend(data)
    print(f"{s}: {len(data)} rows")

    df = pd.DataFrame(all_data)
    print(f"Total rows: {len(df)}")
    """
    #df = pd.read_csv(file_path)
    #df = pd.DataFrame(df)
    base_url = "https://chronicdata.cdc.gov/resource/cwsq-ngmh.json"
    params = {
        "$where": "measureid='STROKE'",
        "$limit": 50000,
        "$offset": 0
    }

    data = []
    while True:
        r = requests.get(base_url, params=params)
        batch = r.json()
        if not batch:
            break
    data.extend(batch)
    params["$offset"] += 50000
    print(f"Fetched {len(batch)} rows...")

    df = pd.DataFrame(data)
    print(f"Total rows: {len(df)}")
    return df

def separate_category_features(df):
    '''
    Separate the Category column health outcomes, prevention factors, health
    risk behaviors etc into different features
    '''
    unique_category_count = df['category'].nunique()
    health_outcome = df.groupby('category')['Health Outcome']
    num_health_outcome = len(health_outcome)
    print('Number of health outcomes:', num_health_outcome, 'Unique categories:', unique_category_count)
    return 

def analyze_stroke_data(df):
    '''
    Analyze stroke-related data from the places DataFrame.
    '''
    # Convert to numeric
    #df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')

    # Filter example: only 'Health Outcomes'
    stroke_df = df[(df['category'] == 'Health Outcomes') & (df['measure'].str.contains('Stroke', case=False, na=False))]

    # Aggregate by state
    stroke_state = stroke_df.groupby('stateabbr')['data_value'].mean().reset_index()
    print(stroke_state.head())
    return stroke_state

    

def main():
    # Example usage
    #places_file_path = "https://chronicdata.cdc.gov/resource/cwsq-ngmh.json?$where=measureid='STROKE'&$limit=50000&$offset=50000"

    #'https://chronicdata.cdc.gov/resource/cwsq-ngmh.json?$limit=5000'
    #requires the API key, todo later
    # 'https://data.cdc.gov/api/v3/views/swc5-untb/query.json'  # Replace with your actual file path
    places_gdf = load_places_data()
    print(places_gdf.columns.tolist())
    places_gdf.info()
    places_gdf.head()
    #separate_category_features(places_gdf)
    #analyze_stroke_data(places_gdf)

if __name__ == '__main__':
    main()  