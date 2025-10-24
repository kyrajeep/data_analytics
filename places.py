import requests
import pandas as pd

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
    print(f"Total rows: {len(df)}")
    
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


def analyze_stroke_data(df_wide):
    '''
    Analyze stroke-related data from the places DataFrame.
    Args:
        df_wide: DataFrame in wide format with states as rows and health measures as columns
    Returns:
        DataFrame with stroke prevalence by state
    '''
    # Sort states by stroke rate
    stroke_by_state = df_wide[['stateabbr', 'stroke_rate']].sort_values('stroke_rate', ascending=False)
    
    print("Top 5 states with highest stroke prevalence:")
    print(stroke_by_state.head())
    
    print("\nBottom 5 states with lowest stroke prevalence:")
    print(stroke_by_state.tail())
    
    return stroke_by_state

def analyze_risk_factors(df_long, df_wide):
    '''
    Analyze correlation between stroke rates and other health factors using wide-format data.
    Returns correlation analysis and state-level statistics.
    '''
    print("\n=== Risk Factor Analysis Results ===")
    
    # Calculate correlations with stroke rate
    risk_factors = [col for col in df_wide.columns 
                   if col not in ['stateabbr', 'stroke_rate']]
    
    correlations = {}
    for factor in risk_factors:
        correlation = df_wide['stroke_rate'].corr(df_wide[factor])
        correlations[factor] = correlation
    
    # Sort correlations by absolute value
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print("\nCorrelations with Stroke Rate:")
    for factor, corr in sorted_correlations:
        print(f"{factor:20} Correlation: {corr:6.3f}")
        
        # Print top 3 states for each factor
        top_states = df_wide.nlargest(3, factor)[['stateabbr', factor, 'stroke_rate']]
        print(f"  Top 3 states with highest {factor}:")
        for _, row in top_states.iterrows():
            print(f"    {row['stateabbr']}: {row[factor]:.1f}% (Stroke Rate: {row['stroke_rate']:.1f}%)")
    
    # Create summary statistics
    summary_stats = df_wide.describe()
    print("\nSummary Statistics:")
    print(summary_stats)
    
    return correlations, df_wide

def analyze_prevention_measures(df):
    '''
    Analyze prevention measures and their potential impact on stroke rates.
    Returns a DataFrame with prevention measures by state.
    '''
    df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')
    
    # Get prevention measures
    prevention_df = df[df['category'] == 'Prevention'].copy()
    
    # Calculate average prevention measure values by state
    prevention_state = prevention_df.groupby(['stateabbr', 'measure'])['data_value'].mean().reset_index()
    
    # Get stroke rates for comparison
    stroke_rates = analyze_stroke_data(df)
    
    # Merge prevention measures with stroke rates
    prevention_state = prevention_state.merge(
        stroke_rates, 
        on='stateabbr', 
        suffixes=('_prevention', '_stroke')
    )
    
    print("\nPrevention measures summary:")
    print(prevention_state.groupby('measure')['data_value_prevention'].describe())
    
    return prevention_state



def analyze_prevention_measures(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Analyze the relationship between prevention measures and stroke rates.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing PLACES data
        
    Returns:
        pd.DataFrame: Analysis of prevention measures
    '''
    # Convert to numeric
    df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')
    
    # Filter for prevention-related measures
    prevention_df = df[
        (df['category'] == 'Prevention') | 
        (df['category'] == 'Health Risk Behaviors')
    ]
    
    # Group by state and measure
    prevention_state = prevention_df.groupby(['stateabbr', 'measure'])['data_value'].mean().reset_index()
    
    print("\nSample of prevention measures by state:")
    print(prevention_state.head(10))
    return prevention_state

    

def main():
    """
    Main function to run the stroke data analysis pipeline.
    """
    # Load the data
    print("Loading PLACES data...")
    places_df_long, places_df_wide = load_places_data()
    
    print("\nAnalyzing stroke prevalence by state...")
    stroke_by_state = analyze_stroke_data(places_df_wide)
    
    print("\nAnalyzing risk factors...")
    risk_correlations, risk_data = analyze_risk_factors(places_df_long, places_df_wide)
    
    print("\nAnalyzing prevention measures...")
    prevention_analysis = analyze_prevention_measures(places_df_long)
    
    # You can add visualization code here later
    return {
        'stroke_data': stroke_by_state,
        'risk_correlations': risk_correlations,
        'risk_data': risk_data,
        'prevention_data': prevention_analysis
    }

if __name__ == '__main__':
    main()  