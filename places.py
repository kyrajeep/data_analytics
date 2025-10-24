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
 
    params = {
        "$where": "measureid='STROKE'",
        "$limit": 50000,
        "$offset": 0
    }
    
    data = []
    offset = 0
    while True:
        current_params = {
            "$where": "measureid='STROKE'",
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


def analyze_stroke_data(df):
    '''
    Analyze stroke-related data from the places DataFrame.
    Returns a DataFrame with stroke prevalence by state.
    '''
    # Convert data_value to numeric
    df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')

    # Filter for stroke-related health outcomes
    stroke_df = df[(df['category'] == 'Health Outcomes') & 
                   (df['measure'].str.contains('Stroke', case=False, na=False))]

    # Aggregate by state
    stroke_state = stroke_df.groupby('stateabbr')['data_value'].mean().reset_index()
    stroke_state = stroke_state.sort_values('data_value', ascending=False)
    
    print("Top 5 states with highest stroke prevalence:")
    print(stroke_state.head())
    return stroke_state

def analyze_risk_factors(df):
    '''
    Analyze correlation between stroke rates and other health factors.
    Returns a dictionary with correlation coefficients.
    '''
    df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')
    
    # Get stroke rates by state
    stroke_rates = df[
        (df['category'] == 'Health Outcomes') & 
        (df['measure'].str.contains('Stroke', case=False))
    ].groupby('stateabbr')['data_value'].mean()
    
    # Analyze correlation with other health factors
    correlations = {}
    health_factors = df[df['category'] == 'Health Outcomes']
    
    for measure in health_factors['measure'].unique():
        if 'Stroke' not in measure:
            factor_rates = health_factors[
                health_factors['measure'] == measure
            ].groupby('stateabbr')['data_value'].mean()
            
            # Calculate correlation where we have both stroke and factor data
            common_states = stroke_rates.index.intersection(factor_rates.index)
            if len(common_states) > 0:
                correlation = stroke_rates[common_states].corr(factor_rates[common_states])
                correlations[measure] = correlation
    
    # Print top correlations
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    print("\nTop health factors correlated with stroke rates:")
    for measure, corr in sorted_correlations[:5]:
        print(f"{measure}: {corr:.3f}")
    
    return correlations

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

def analyze_risk_factors(df: pd.DataFrame) -> dict:
    '''
    Analyze potential risk factors for stroke across states.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing PLACES data
        
    Returns:
        dict: Dictionary containing correlation results for different risk factors
    '''
    # Convert data values to numeric
    df['data_value'] = pd.to_numeric(df['data_value'], errors='coerce')
    
    # Get base stroke data by state
    stroke_data = df[
        (df['category'] == 'Health Outcomes') & 
        (df['measure'].str.contains('Stroke', case=False, na=False))
    ].groupby('stateabbr')['data_value'].mean()
    
    # Risk factors to analyze
    risk_factors = [
        'High Blood Pressure',
        'Diabetes',
        'Physical Inactivity',
        'Obesity',
        'Smoking'
    ]
    
    correlations = {}
    for factor in risk_factors:
        factor_data = df[
            df['measure'].str.contains(factor, case=False, na=False)
        ].groupby('stateabbr')['data_value'].mean()
        
        # Calculate correlation with stroke data
        correlation = stroke_data.corr(factor_data)
        correlations[factor] = correlation
        
        print(f"\nCorrelation between Stroke and {factor}: {correlation:.3f}")
    
    return correlations

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
    places_df = load_places_data()
    
    print("\nAnalyzing stroke prevalence by state...")
    stroke_by_state = analyze_stroke_data(places_df)
    
    print("\nAnalyzing risk factors...")
    risk_correlations = analyze_risk_factors(places_df)
    
    print("\nAnalyzing prevention measures...")
    prevention_analysis = analyze_prevention_measures(places_df)
    
    # You can add visualization code here later
    return {
        'stroke_data': stroke_by_state,
        'risk_correlations': risk_correlations,
        'prevention_data': prevention_analysis
    }

if __name__ == '__main__':
    main()  