import pandas as pd

def load_places_data(file_path):
    """
    Load places data from a CSV file and convert it to a GeoDataFrame.

    Parameters:
    file_path (str): The path to the CSV file containing places data.

    Returns:
    gpd.GeoDataFrame: A GeoDataFrame with geometry column created from latitude and longitude.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    df = pd.DataFrame(df)
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
    places_file_path = "https://chronicdata.cdc.gov/resource/cwsq-ngmh.json?$where=measureid='STROKE'"

    #'https://chronicdata.cdc.gov/resource/cwsq-ngmh.json?$limit=5000'
    #requires the API key, todo later
    # 'https://data.cdc.gov/api/v3/views/swc5-untb/query.json'  # Replace with your actual file path
    places_gdf = load_places_data(places_file_path)
    print(places_gdf.columns.tolist())
    places_gdf.info()
    #separate_category_features(places_gdf)
    #analyze_stroke_data(places_gdf)

if __name__ == '__main__':
    main()  