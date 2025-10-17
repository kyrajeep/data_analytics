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
    unique_category_count = df['Category'].nunique()
    health_outcome = df.groupby('Category')['Health Outcome']
    num_health_outcome = len(health_outcome)
    print('Number of health outcomes:', num_health_outcome, 'Unique categories:', unique_category_count)
    return 
    
    
    
    
    
    
    

  
  

def main():
    # Example usage
    places_file_path = 'https://data.cdc.gov/resource/swc5-untb.json'
    #requires the API key, todo later
    # 'https://data.cdc.gov/api/v3/views/swc5-untb/query.json'  # Replace with your actual file path
    places_gdf = load_places_data(places_file_path)
    print(places_gdf.head())
    #separate_category_features(places_gdf)


if __name__ == '__main__':
    main()  