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
  
  
  

def main():
    # Example usage
    file_path = 'https://data.cdc.gov/resource/swc5-untb.json'
    #requires the API key, todo later
    # 'https://data.cdc.gov/api/v3/views/swc5-untb/query.json'  # Replace with your actual file path
    places_gdf = load_places_data(file_path)
    print(places_gdf.head())


if __name__ == '__main__':
    main()  