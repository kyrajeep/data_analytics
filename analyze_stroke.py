import pandas as pd
import numpy as np

def analyze_stroke_data(df_wide):
    """
    Analyze stroke-related data from the places DataFrame.
    
    Args:
        df_wide (pd.DataFrame): DataFrame in wide format with states as rows and health measures as columns
    
    Returns:
        pd.DataFrame: DataFrame with stroke prevalence by state
    """
    # Sort states by stroke rate
    if 'stateabbr' not in df_wide.columns:
        raise ValueError("DataFrame must contain 'stateabbr' column")
    
    if 'stroke_rate' not in df_wide.columns:
        raise ValueError("DataFrame must contain 'stroke_rate' column")
    
    stroke_by_state = df_wide[['stateabbr', 'stroke_rate']].sort_values('stroke_rate', ascending=False)
    
    print("Top 5 states with highest stroke prevalence:")
    print(stroke_by_state.head())
    
    print("\nBottom 5 states with lowest stroke prevalence:")
    print(stroke_by_state.tail())
    
    return stroke_by_state


def analyze_risk_factors(df_wide):
    """
    Analyze correlation between stroke rates and other health factors using wide-format data.
    
    Args:
        df_wide (pd.DataFrame): DataFrame in wide format with health measures
    
    Returns:
        dict: Correlation analysis of risk factors with stroke rate
    """
    print("\n" + "=" * 80)
    print("=== Risk Factor Analysis Results ===")
    print("=" * 80)
    
    if 'stroke_rate' not in df_wide.columns:
        raise ValueError("DataFrame must contain 'stroke_rate' column")
    
    # Define health measures to analyze (excluding metadata and derived columns)
    health_measures = [
        'blood_pressure', 'diabetes', 'obesity', 'current_smoking',
        'physical_inactivity', 'heart_disease', 'poor_physical_health',
        'poor_mental_health', 'binge_drinking'
    ]
    
    correlations = {}
    for factor in health_measures:
        if factor in df_wide.columns:
            # Remove NaN values for correlation calculation
            valid_data = df_wide[['stroke_rate', factor]].dropna()
            if len(valid_data) > 1:
                correlation = valid_data['stroke_rate'].corr(valid_data[factor])
                correlations[factor] = correlation
    
    # Sort correlations by absolute value
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print("\nCorrelations with Stroke Rate:")
    for factor, corr in sorted_correlations:
        print(f"{factor:30} Correlation: {corr:7.3f}")
    
    # Create summary statistics for numeric columns only
    numeric_cols = df_wide.select_dtypes(include=['float64', 'int64']).columns
    summary_stats = df_wide[numeric_cols].describe()
    print("\nSummary Statistics:")
    print(summary_stats)
    
    return correlations


def analyze_prevention_measures(df_long):
    """
    Analyze the relationship between prevention measures and stroke rates.
    
    Args:
        df_long (pd.DataFrame): The input DataFrame containing PLACES data in long format
        
    Returns:
        pd.DataFrame: Analysis of prevention measures
    """
    print("\n" + "=" * 80)
    print("=== Prevention Measures Analysis ===")
    print("=" * 80)
    
    if 'data_value' not in df_long.columns:
        raise ValueError("DataFrame must contain 'data_value' column")
    
    # Convert to numeric
    df_long['data_value'] = pd.to_numeric(df_long['data_value'], errors='coerce')
    
    # Filter for prevention-related measures
    prevention_df = df_long[
        (df_long['category'] == 'Prevention') | 
        (df_long['category'] == 'Health Risk Behaviors')
    ].copy()
    
    if len(prevention_df) == 0:
        print("No prevention measures found in data")
        return pd.DataFrame()
    
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
    print("\n" + "=" * 80)
    print("=== Preparing Data for Tableau ===")
    print("=" * 80)
    
    if 'stateabbr' not in df_wide.columns:
        raise ValueError("DataFrame must contain 'stateabbr' column")
    
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
    
    # Add rankings for each numeric measure
    numeric_cols = tableau_df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if col != 'stateabbr':
            tableau_df[f'{col}_rank'] = tableau_df[col].rank(ascending=False)
    
    # Create risk categories based on percentiles
    risk_measures = ['stroke_rate', 'blood_pressure', 'diabetes', 'obesity', 
                    'current_smoking', 'physical_inactivity']
    
    for measure in risk_measures:
        if measure in tableau_df.columns:
            try:
                tableau_df[f'{measure}_category'] = pd.qcut(
                    tableau_df[measure], 
                    q=5, 
                    labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High'],
                    duplicates='drop'
                )
            except Exception as e:
                print(f"Warning: Could not categorize {measure}: {e}")
    
    # Calculate composite risk score
    risk_columns = [col for col in risk_measures if col in tableau_df.columns]
    
    if len(risk_columns) > 0:
        # Normalize each risk factor and calculate mean
        normalized_risks = tableau_df[risk_columns].apply(
            lambda x: (x - x.min()) / (x.max() - x.min()) if (x.max() - x.min()) > 0 else 0
        )
        tableau_df['composite_risk_score'] = normalized_risks.mean(axis=1)
        
        # Add composite risk category
        try:
            tableau_df['risk_category'] = pd.qcut(
                tableau_df['composite_risk_score'],
                q=5,
                labels=['Very Low Risk', 'Low Risk', 'Moderate Risk', 'High Risk', 'Very High Risk'],
                duplicates='drop'
            )
        except Exception as e:
            print(f"Warning: Could not categorize composite risk: {e}")
    
    print(f"\n✓ Tableau data preparation complete:")
    print(f"  Number of states: {len(tableau_df)}")
    print("  Added columns:")
    print("    - State names and regions")
    print("    - Rankings for all measures")
    print("    - Risk categories for key measures")
    print("    - Composite risk score and category")
    
    return tableau_df


def main():
    """
    Main function to run the analysis pipeline.
    Note: This assumes data has already been loaded and cleaned via load_data.py
    """
    print("=" * 80)
    print("STROKE ANALYSIS MODULE")
    print("=" * 80)
    print("\nThis module contains analysis functions.")
    print("Please use load_data.py to load and clean data first.")
    print("Then pass the cleaned data to analysis functions.")


if __name__ == '__main__':
    main()
