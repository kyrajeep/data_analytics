import requests
import pandas as pd
import numpy as np

def load_places_data():
    """
    Load places data from all states including health outcomes and risk factors.
    Returns:
        tuple: (df_long, df_wide) containing the data in both formats
    """
    # Load the CSV file into a DataFrame
    base_url = "https://chronicdata.cdc.gov/resource/cwsq-ngmh.json"
    states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN',
          'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV',
          'NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN',
          'TX','UT','VT','VA','WA','WV','WI','WY']

    # Define measures we're interested in
    measures_of_interest = [
        'STROKE',          # Stroke
        'BPHIGH',         # High Blood Pressure
        'DIABETES',       # Diabetes
        'OBESITY',        # Obesity
        'CSMOKING',       # Current Smoking
        'PHLTH',          # Poor Physical Health
        'MHLTH',          # Poor Mental Health
        'BINGE',          # Binge Drinking
        'LPA',            # Physical Inactivity
        'CHOLSCREEN',     # Cholesterol Screening
        'CHD'             # Coronary Heart Disease
    ]
    
    # Create WHERE clause for multiple measures
    measures_clause = " OR ".join([f"measureid='{m}'" for m in measures_of_interest])
    
    data = []
    offset = 0
    while True:
        current_params = {
            "$where": f"({measures_clause})",
            "$limit": 50000,
            "$offset": offset
        }
        r = requests.get(base_url, params=current_params)
        batch = r.json()
        # Break the loop if no more data is returned
        if not batch:
            break
        
        data.extend(batch)
        # Increment the offset for the next batch
        offset += 50000
        print(f"Fetched {len(batch)} rows...")

    # Convert to DataFrame
    df = pd.DataFrame(data)
    print(f"Total rows before deduplication: {len(df)}")
    
    # Convert data_value to numeric
    df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')
    
    # Create wide format DataFrame
    df_wide = df.pivot_table(
        index='stateabbr',
        columns='measureid',
        values='data_value',
        aggfunc='mean'
    ).reset_index()
    
    # Rename columns to be more descriptive
    measure_names = {
        'STROKE': 'stroke_rate',
        'BPHIGH': 'blood_pressure',
        'DIABETES': 'diabetes',
        'OBESITY': 'obesity',
        'CSMOKING': 'current_smoking',
        'PHLTH': 'poor_physical_health',
        'MHLTH': 'poor_mental_health',
        'BINGE': 'binge_drinking',
        'LPA': 'physical_inactivity',
        'CHOLSCREEN': 'cholesterol_screening',
        'CHD': 'heart_disease'
    }
    df_wide.rename(columns=measure_names, inplace=True)
    
    # Check for missing states
    missing_states = set(states) - set(df['stateabbr'].unique())
    if missing_states:
        print(f"Warning: Missing data from states: {missing_states}")
        print("States and their record counts:")
        print(df['stateabbr'].value_counts())
    
    print(f"Number of states in data: {df['stateabbr'].nunique()}")
    print(f"Total records: {len(df)}")
    print("\nWide format data shape:", df_wide.shape)
    print("Available measures:", list(df_wide.columns))
    
    return df, df_wide

def detect_duplicates(df):
    """
    Detect duplicate rows in the dataframe.
    
    Args:
        df (pd.DataFrame): The input dataframe
    
    Returns:
        pd.DataFrame: DataFrame containing only duplicate rows
    """
    print("\n" + "=" * 80)
    print("DUPLICATE DETECTION ANALYSIS")
    print("=" * 80)
    
    total_rows = len(df)
    duplicated_mask = df.duplicated(keep=False)
    duplicates = df[duplicated_mask]
    
    print(f"\nTotal rows: {total_rows}")
    print(f"Duplicate rows found: {len(duplicates)}")
    print(f"Duplicate percentage: {(len(duplicates) / total_rows * 100):.2f}%")
    
    if len(duplicates) > 0:
        print("\nDuplicate rows:")
        print(duplicates.sort_values(by=list(df.columns[:-1])).to_string())
    
    return duplicates

def remove_duplicates(df):
    """
    Remove duplicate rows from the dataframe, keeping the first occurrence.
    
    Args:
        df (pd.DataFrame): The input dataframe
    
    Returns:
        pd.DataFrame: Dataframe with duplicates removed
    """
    before_count = len(df)
    df_deduplicated = df.drop_duplicates(keep='first')
    after_count = len(df_deduplicated)
    removed_count = before_count - after_count
    
    print(f"\nRemoved {removed_count} duplicate rows")
    print(f"Before: {before_count} rows, After: {after_count} rows")
    
    return df_deduplicated

def analyze_missing_values(df):
    """
    Analyze and visualize missing values in the dataframe.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    
    Returns:
        pd.DataFrame: DataFrame summarizing missing values
    """
    print("\n" + "=" * 80)
    print("MISSING VALUES ANALYSIS")
    print("=" * 80)
    
    # Calculate missing values
    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    # Create a dataframe for better visualization
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_count.values,
        'Missing_Percentage': missing_percent.values
    })
    
    # Filter only columns with missing values
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    
    print("\nMissing Values Summary:")
    if len(missing_df) == 0:
        print("No missing values found!")
    else:
        print(missing_df.to_string(index=False))
        print(f"\nTotal columns with missing values: {len(missing_df)}")
        print(f"Total missing cells: {df.isnull().sum().sum()}")
    
    return missing_df

def check_state_coverage(df):
    """
    Check which states have missing data.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    """
    print("\n" + "=" * 80)
    print("STATE COVERAGE ANALYSIS")
    print("=" * 80)
    
    if 'stateabbr' in df.columns:
        states_in_data = df['stateabbr'].unique()
        print(f"\nNumber of unique states: {len(states_in_data)}")
        print(f"States found: {sorted(states_in_data)}")

def clean_missing_values(df):
    """
    Clean missing values using appropriate strategies.
    
    Args:
        df (pd.DataFrame): The dataframe to clean
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print("\n" + "=" * 80)
    print("DATA CLEANING")
    print("=" * 80)
    
    df_clean = df.copy()
    
    # Fill numeric columns with median by state
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            if 'stateabbr' in df_clean.columns:
                # Fill by state median
                df_clean[col] = df_clean.groupby('stateabbr')[col].transform(
                    lambda x: x.fillna(x.median())
                )
                print(f"✓ Filled {col} with state median")
            else:
                # Fill with overall median
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                print(f"✓ Filled {col} with overall median: {median_val:.2f}")
    
    # Fill categorical columns with mode
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any():
            mode_val = df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown'
            df_clean[col].fillna(mode_val, inplace=True)
            print(f"✓ Filled {col} with mode: {mode_val}")
    
    return df_clean

def validate_data_quality(df):
    """
    Validate data quality after cleaning.
    
    Args:
        df (pd.DataFrame): The dataframe to validate
    
    Returns:
        dict: Quality metrics
    """
    print("\n" + "=" * 80)
    print("DATA QUALITY VALIDATION")
    print("=" * 80)
    
    quality_metrics = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'complete_rows': len(df[~df.isnull().any(axis=1)])
    }
    
    print(f"\nTotal rows: {quality_metrics['total_rows']}")
    print(f"Total columns: {quality_metrics['total_columns']}")
    print(f"Missing values: {quality_metrics['missing_values']}")
    print(f"Duplicate rows: {quality_metrics['duplicate_rows']}")
    print(f"Complete rows (no missing values): {quality_metrics['complete_rows']}")
    
    if quality_metrics['missing_values'] == 0:
        print("\n✓ No missing values!")
    if quality_metrics['duplicate_rows'] == 0:
        print("✓ No duplicate rows!")
    
    return quality_metrics

def main():
    """
    Main function to run the complete data loading and cleaning process.
    """
    # Load the data
    print("Loading PLACES data from CDC API...")
    df_long, df_wide = load_places_data()
    
    # Detect duplicates in long format
    duplicates = detect_duplicates(df_long)
    
    # Remove duplicates
    if len(duplicates) > 0:
        df_long = remove_duplicates(df_long)
    
    # Analyze missing values
    missing_df = analyze_missing_values(df_wide)
    
    # Check state coverage
    check_state_coverage(df_wide)
    
    # Clean missing values
    df_wide_cleaned = clean_missing_values(df_wide)
    
    # Validate data quality
    quality_metrics = validate_data_quality(df_wide_cleaned)
    
    # Save cleaned data
    output_path = 'places_data_cleaned.csv'
    df_wide_cleaned.to_csv(output_path, index=False)
    print(f"\n✓ Cleaned data saved to: {output_path}")
    
    return df_long, df_wide_cleaned, quality_metrics

if __name__ == '__main__':
    df_long, df_wide_cleaned, quality_metrics = main()
