# Stroke Risk Analysis Across U.S. States

## Project Overview
This project analyzes stroke prevalence and its risk factors across U.S. states using the CDC's PLACES dataset. The analysis explores correlations between stroke rates and various health factors, identifies regional patterns, and provides insights into prevention measures.

## Key Findings

### Stroke Prevalence
- Highest rates found in southeastern states
- Top 5 states with highest stroke prevalence:
  1. Mississippi (5.02%)
  2. Louisiana (4.80%)
  3. Alabama (4.71%)
  4. Arkansas (4.66%)
  5. West Virginia (4.64%)

### Risk Factor Correlations
Strong correlations with stroke rates were found for:
1. High Blood Pressure (0.936)
2. Diabetes (0.873)
3. Heart Disease (0.854)
4. Physical Inactivity (0.832)
5. Current Smoking (0.826)

### Regional Patterns
- Southern states consistently show higher risk factors across multiple health measures
- Western states generally show lower stroke rates and risk factors
- Clear regional disparities in health outcomes and prevention measures

## Data Source
- CDC PLACES Dataset
- API Endpoint: https://chronicdata.cdc.gov/resource/cwsq-ngmh.json
- Measures include:
  - Stroke prevalence
  - Blood pressure
  - Diabetes
  - Obesity
  - Physical inactivity
  - Smoking rates
  - Mental and physical health indicators

## Project Structure
\`\`\`
data_analytics/
├── places.py           # Main analysis script
├── test_places.py      # Unit tests
└── stroke_analysis_tableau.csv  # Processed data for visualization
\`\`\`

## Features
- Data loading and preprocessing from CDC API
- Comprehensive risk factor analysis
- Statistical correlation analysis
- Regional pattern identification
- Tableau-ready data preparation
- Unit tests for reliability

## Analysis Components
1. **Data Collection**
   - Automated fetching from CDC PLACES API
   - Handles pagination for complete data retrieval

2. **Risk Analysis**
   - Correlation analysis with health factors
   - Regional pattern identification
   - Composite risk score calculation

3. **Data Enhancement**
   - State name and region mapping
   - Risk categorization
   - Measure rankings
   - Composite risk scoring

4. **Visualization Preparation**
   - Tableau-ready CSV output
   - Geographic information
   - Risk categories
   - Rankings for all measures

## Tableau Visualization Guide
The processed data (stroke_analysis_tableau.csv) is prepared for various visualizations:

1. **State-Level Risk Map**
   - Choropleth mapping using composite_risk_score
   - Risk category filtering
   - Regional pattern visualization

2. **Regional Analysis Dashboard**
   - Health measure comparisons by region
   - Regional vs. state-level averages
   - Trend analysis

3. **Correlation Matrix**
   - Scatter plots of stroke rates vs. risk factors
   - Regional color coding
   - Trend line analysis

4. **Risk Factor Rankings**
   - Dynamic bar charts
   - Measure selection via parameters
   - State and regional comparisons

## Setup and Usage

### Prerequisites
- Python 3.x
- Virtual Environment (recommended)
- Required packages:
  - pandas
  - requests
  - numpy

### Installation
\`\`\`bash
# Clone the repository
git clone https://github.com/kyrajeep/data_analytics.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install pandas requests numpy
\`\`\`

### Running the Analysis
\`\`\`python
python places.py
\`\`\`

### Running Tests
\`\`\`python
python -m unittest test_places.py
\`\`\`

## Future Enhancements
- Time series analysis with historical data
- Demographic factor integration
- Socioeconomic correlation analysis
- Machine learning predictions
- Interactive visualization dashboard

## Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss the proposed changes.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
Kyra
