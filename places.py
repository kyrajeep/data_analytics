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
    
    # Define health measures to analyze (excluding metadata and derived columns)
    health_measures = [
        'blood_pressure', 'diabetes', 'obesity', 'current_smoking',
        'physical_inactivity', 'heart_disease', 'poor_physical_health',
        'poor_mental_health', 'binge_drinking'
    ]
    
    correlations = {}
    for factor in health_measures:
        if factor in df_wide.columns:
            correlation = df_wide['stroke_rate'].corr(df_wide[factor])
            correlations[factor] = correlation
    
    # Sort correlations by absolute value
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print("\nCorrelations with Stroke Rate:")
    for factor, corr in sorted_correlations:
        print(f"{factor:20} Correlation: {corr:6.3f}")
        
        # Print top 3 states for each factor
        top_states = df_wide.nlargest(3, factor)[['state_name', factor, 'stroke_rate', 'region']]
        print(f"  Top 3 states with highest {factor}:")
        for _, row in top_states.iterrows():
            print(f"    {row['state_name']} ({row['region']}): {row[factor]:.1f}% (Stroke Rate: {row['stroke_rate']:.1f}%)")
    
    # Create summary statistics for numeric columns only
    numeric_cols = df_wide.select_dtypes(include=['float64', 'int64']).columns
    summary_stats = df_wide[numeric_cols].describe()
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

    

def prepare_tableau_data(df_wide):
    """
    Prepare data for Tableau visualization by adding state names, regions,
    rankings, and risk categories.
    
    Args:
        df_wide (pd.DataFrame): Wide format DataFrame with health measures
    
    Returns:
        pd.DataFrame: Enhanced DataFrame ready for Tableau
    """
    # Add state names
    state_names = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    
    # Add geographic regions
    state_regions = {
        'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast', 'NH': 'Northeast',
        'RI': 'Northeast', 'VT': 'Northeast', 'NJ': 'Northeast', 'NY': 'Northeast',
        'PA': 'Northeast', 'IL': 'Midwest', 'IN': 'Midwest', 'MI': 'Midwest',
        'OH': 'Midwest', 'WI': 'Midwest', 'IA': 'Midwest', 'KS': 'Midwest',
        'MN': 'Midwest', 'MO': 'Midwest', 'NE': 'Midwest', 'ND': 'Midwest',
        'SD': 'Midwest', 'DE': 'South', 'FL': 'South', 'GA': 'South',
        'MD': 'South', 'NC': 'South', 'SC': 'South', 'VA': 'South',
        'WV': 'South', 'AL': 'South', 'KY': 'South', 'MS': 'South',
        'TN': 'South', 'AR': 'South', 'LA': 'South', 'OK': 'South',
        'TX': 'South', 'AZ': 'West', 'CO': 'West', 'ID': 'West',
        'MT': 'West', 'NV': 'West', 'NM': 'West', 'UT': 'West',
        'WY': 'West', 'AK': 'West', 'CA': 'West', 'HI': 'West',
        'OR': 'West', 'WA': 'West'
    }
    
    # Create a copy to avoid modifying the original
    tableau_df = df_wide.copy()
    
    # Add state names and regions
    tableau_df['state_name'] = tableau_df['stateabbr'].map(state_names)
    tableau_df['region'] = tableau_df['stateabbr'].map(state_regions)
    
    # Add rankings for each measure
    for col in tableau_df.columns:
        if col not in ['stateabbr', 'state_name', 'region']:
            tableau_df[f'{col}_rank'] = tableau_df[col].rank(ascending=False)
    
    # Create risk categories based on percentiles
    risk_measures = ['stroke_rate', 'blood_pressure', 'diabetes', 'obesity', 
                    'current_smoking', 'physical_inactivity']
    
    for measure in risk_measures:
        tableau_df[f'{measure}_category'] = pd.qcut(
            tableau_df[measure], 
            q=5, 
            labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High']
        )
    
    # Calculate composite risk score
    risk_columns = [col for col in tableau_df.columns 
                   if col in risk_measures]
    
    # Normalize each risk factor and calculate mean
    normalized_risks = tableau_df[risk_columns].apply(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )
    tableau_df['composite_risk_score'] = normalized_risks.mean(axis=1)
    
    # Add composite risk category
    tableau_df['risk_category'] = pd.qcut(
        tableau_df['composite_risk_score'],
        q=5,
        labels=['Very Low Risk', 'Low Risk', 'Moderate Risk', 'High Risk', 'Very High Risk']
    )
    
    print("\nTableau data preparation complete:")
    print(f"Number of states: {len(tableau_df)}")
    print("Added columns:", 
          "\n - State names and regions",
          "\n - Rankings for all measures",
          "\n - Risk categories for key measures",
          "\n - Composite risk score and category")
    
    return tableau_df

def main():
    """
    Main function to run the stroke data analysis pipeline.
    """
    # Load the data
    print("Loading PLACES data...")
    places_df_long, places_df_wide = load_places_data()
    
    # Prepare data for Tableau
    tableau_ready_df = prepare_tableau_data(places_df_wide)
    
    print("\nAnalyzing stroke prevalence by state...")
    stroke_by_state = analyze_stroke_data(tableau_ready_df)
    
    print("\nAnalyzing risk factors...")
    risk_correlations, risk_data = analyze_risk_factors(places_df_long, tableau_ready_df)
    
    print("\nAnalyzing prevention measures...")
    prevention_analysis = analyze_prevention_measures(places_df_long)
    
    # Save the Tableau-ready data to CSV
    output_path = 'stroke_analysis_tableau.csv'
    tableau_ready_df.to_csv(output_path, index=False)
    print(f"\nSaved Tableau-ready data to {output_path}")
    
    print("\nSuggested Tableau Visualizations:")
    print("1. State-Level Risk Map:")
    print("   - Use composite_risk_score for choropleth coloring")
    print("   - Use risk_category for filtering")
    
    print("\n2. Regional Analysis Dashboard:")
    print("   - Compare health measures by region")
    print("   - Show regional averages vs state values")
    
    print("\n3. Correlation Matrix:")
    print("   - Create scatter plots of stroke_rate vs risk factors")
    print("   - Use different colors for regions")
    
    print("\n4. Risk Factor Rankings:")
    print("   - Create bar charts showing state rankings for each measure")
    print("   - Enable measure selection via parameter")
    
    return {
        'stroke_data': stroke_by_state,
        'risk_correlations': risk_correlations,
        'risk_data': risk_data,
        'prevention_data': prevention_analysis,
        'tableau_data': tableau_ready_df
    }

if __name__ == '__main__':
    main()  