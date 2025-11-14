import pandas as pd
import numpy as np

def load_tableau_data(filepath='stroke_analysis_tableau.csv'):
    """
    Load the Tableau-ready data and analyze missing values.
    
    Args:
        filepath (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: The loaded dataframe
    """
    df = pd.read_csv(filepath)
    print(f"Data loaded: {filepath}")
    print(f"Shape: {df.shape}\n")
    return df

def analyze_missing_values(df):
    """
    Analyze and visualize missing values in the dataframe.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    """
    print("=" * 80)
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
    print(missing_df.to_string(index=False))
    
    if len(missing_df) == 0:
        print("\nNo missing values found!")
    else:
        print(f"\nTotal columns with missing values: {len(missing_df)}")
        print(f"Total missing cells: {df.isnull().sum().sum()}")
    
    return missing_df

def analyze_missing_by_column(df):
    """
    Provide detailed analysis of missing values by column type.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    """
    print("\n" + "=" * 80)
    print("DETAILED MISSING VALUES BY COLUMN")
    print("=" * 80)
    
    missing_cols = df.columns[df.isnull().any()].tolist()
    
    for col in missing_cols:
        null_count = df[col].isnull().sum()
        null_percent = (null_count / len(df)) * 100
        
        print(f"\n{col}:")
        print(f"  Missing: {null_count} out of {len(df)} ({null_percent:.2f}%)")
        print(f"  Data type: {df[col].dtype}")
        
        # Show sample of non-null values
        non_null_samples = df[col].dropna().head(3).tolist()
        print(f"  Sample non-null values: {non_null_samples}")

def check_state_coverage(df):
    """
    Check which states have missing data.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    """
    print("\n" + "=" * 80)
    print("STATE COVERAGE ANALYSIS")
    print("=" * 80)
    
    if 'state_name' in df.columns:
        missing_states = df[df.isnull().any(axis=1)]['state_name'].tolist()
        
        if missing_states:
            print(f"\nStates with missing values:")
            for state in missing_states:
                missing_in_state = df[df['state_name'] == state].isnull().sum()
                print(f"  {state}: {missing_in_state[missing_in_state > 0].to_dict()}")
        else:
            print("\nAll states have complete data!")
    
    # Check for rows that are completely empty
    print(f"\nRows with all missing values: {df.isnull().all(axis=1).sum()}")
    print(f"Rows with at least one missing value: {df.isnull().any(axis=1).sum()}")

def identify_na_patterns(df):
    """
    Identify patterns in missing data (e.g., which fields are often missing together).
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    """
    print("\n" + "=" * 80)
    print("MISSING DATA PATTERNS")
    print("=" * 80)
    
    # Find rows with missing data
    rows_with_missing = df[df.isnull().any(axis=1)]
    
    if len(rows_with_missing) > 0:
        print(f"\nRows with missing data: {len(rows_with_missing)}")
        print("\nMissing data patterns:")
        print(rows_with_missing.to_string())
    else:
        print("\nNo missing data patterns found!")

def suggest_cleaning_strategies(df, missing_df):
    """
    Suggest cleaning strategies based on missing value analysis.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
        missing_df (pd.DataFrame): Missing values summary dataframe
    """
    print("\n" + "=" * 80)
    print("SUGGESTED CLEANING STRATEGIES")
    print("=" * 80)
    
    if len(missing_df) == 0:
        print("\nNo cleaning needed - data is complete!")
        return
    
    print("\nBased on your missing values, here are recommended strategies:\n")
    
    for idx, row in missing_df.iterrows():
        col = row['Column']
        missing_pct = row['Missing_Percentage']
        
        print(f"{col} ({missing_pct:.2f}% missing):")
        
        if missing_pct > 50:
            print(f"  → DROP column (>50% missing)")
        elif missing_pct > 20:
            print(f"  → Consider DROPPING or use FORWARD/BACKWARD FILL")
        elif missing_pct > 5:
            print(f"  → Use FORWARD/BACKWARD FILL or INTERPOLATION")
        else:
            print(f"  → FILL with median/mean or use mode")
        
        # Check data type for specific strategies
        if df[col].dtype == 'object':
            print(f"  → Since it's categorical: use MODE or forward fill")
        elif df[col].dtype in ['float64', 'int64']:
            print(f"  → Since it's numeric: use MEDIAN/MEAN or interpolation")

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
    
    # 1. Fix state abbreviation and name for DC
    print("\n1. Fixing District of Columbia (DC) data:")
    dc_mask = df_clean['stateabbr'] == 'DC'
    if dc_mask.any():
        df_clean.loc[dc_mask, 'state_name'] = 'District of Columbia'
        df_clean.loc[dc_mask, 'region'] = 'Northeast'
        print(f"   ✓ Set state_name='District of Columbia' and region='Northeast' for DC")
    
    # 2. Fill Florida's blood pressure with median
    print("\n2. Filling Florida's missing blood pressure data:")
    bp_median = df_clean['blood_pressure'].median()
    fl_mask = df_clean['state_name'] == 'Florida'
    if fl_mask.any() and df_clean.loc[fl_mask, 'blood_pressure'].isnull().any():
        df_clean.loc[fl_mask, 'blood_pressure'] = bp_median
        print(f"   ✓ Filled with median value: {bp_median:.2f}%")
    
    # 3. Fill Florida's cholesterol screening with median
    print("\n3. Filling Florida's missing cholesterol screening data:")
    chol_median = df_clean['cholesterol_screening'].median()
    if fl_mask.any() and df_clean.loc[fl_mask, 'cholesterol_screening'].isnull().any():
        df_clean.loc[fl_mask, 'cholesterol_screening'] = chol_median
        print(f"   ✓ Filled with median value: {chol_median:.2f}%")
    
    # 4. Recalculate ranks for affected columns
    print("\n4. Recalculating affected ranks:")
    df_clean['blood_pressure_rank'] = df_clean['blood_pressure'].rank(ascending=False)
    df_clean['cholesterol_screening_rank'] = df_clean['cholesterol_screening'].rank(ascending=False)
    print("   ✓ Recalculated blood_pressure_rank")
    print("   ✓ Recalculated cholesterol_screening_rank")
    
    # 5. Recategorize blood pressure for affected rows
    print("\n5. Recategorizing blood pressure risk:")
    df_clean['blood_pressure_category'] = pd.qcut(
        df_clean['blood_pressure'],
        q=5,
        labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High'],
        duplicates='drop'
    )
    print("   ✓ Recategorized blood_pressure_category")
    
    return df_clean

def validate_cleaning(df_original, df_cleaned):
    """
    Validate that cleaning was successful.
    
    Args:
        df_original (pd.DataFrame): Original dataframe
        df_cleaned (pd.DataFrame): Cleaned dataframe
    """
    print("\n" + "=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    
    print("\nBefore cleaning:")
    print(f"  Missing values: {df_original.isnull().sum().sum()}")
    print(f"  Rows with missing data: {df_original.isnull().any(axis=1).sum()}")
    
    print("\nAfter cleaning:")
    print(f"  Missing values: {df_cleaned.isnull().sum().sum()}")
    print(f"  Rows with missing data: {df_cleaned.isnull().any(axis=1).sum()}")
    
    if df_cleaned.isnull().sum().sum() == 0:
        print("\n✓ SUCCESS: All missing values have been cleaned!")
    else:
        print("\n✗ WARNING: Some missing values remain")
        print(df_cleaned.isnull().sum()[df_cleaned.isnull().sum() > 0])

def save_cleaned_data(df, output_path='stroke_analysis_tableau_cleaned.csv'):
    """
    Save the cleaned dataframe to a new CSV file.
    
    Args:
        df (pd.DataFrame): The cleaned dataframe
        output_path (str): Path to save the file
    """
    df.to_csv(output_path, index=False)
    print(f"\n✓ Cleaned data saved to: {output_path}")

def main():
    """
    Main function to run the complete data cleaning analysis and cleaning process.
    """
    # Load the data
    df = load_tableau_data()
    
    # Analyze missing values
    missing_df = analyze_missing_values(df)
    
    # Detailed analysis
    if len(missing_df) > 0:
        analyze_missing_by_column(df)
        check_state_coverage(df)
        identify_na_patterns(df)
        suggest_cleaning_strategies(df, missing_df)
        
        # Clean the data
        df_cleaned = clean_missing_values(df)
        
        # Validate the cleaning
        validate_cleaning(df, df_cleaned)
        
        # Save the cleaned data
        save_cleaned_data(df_cleaned)
    else:
        print("\n✓ No missing values found - no cleaning needed!")
        df_cleaned = df
    
    print("\n" + "=" * 80)
    print("PROCESS COMPLETE")
    print("=" * 80)
    
    return df, df_cleaned, missing_df

if __name__ == '__main__':
    df_original, df_clean, missing_summary = main()
