import unittest
import pandas as pd
import numpy as np
from analyze_stroke import (
    analyze_stroke_data,
    analyze_risk_factors,
    analyze_prevention_measures,
    prepare_tableau_data
)

class TestStrokeAnalysis(unittest.TestCase):
    """Test stroke data analysis functionality"""
    
    def setUp(self):
        """Create sample data for testing"""
        self.sample_wide = pd.DataFrame({
            'stateabbr': ['CA', 'TX', 'FL', 'NY'],
            'stroke_rate': [5.2, 6.1, 5.8, 6.0],
            'blood_pressure': [25.3, 26.5, 25.1, 24.8],
            'diabetes': [8.5, 9.2, 8.9, 8.8],
            'obesity': [25.1, 26.3, 25.8, 24.5],
            'current_smoking': [15.2, 16.5, 15.1, 14.8],
            'physical_inactivity': [22.3, 23.5, 22.1, 21.8],
            'heart_disease': [4.2, 4.8, 4.1, 3.9],
            'poor_physical_health': [12.3, 13.5, 12.1, 11.8],
            'poor_mental_health': [11.5, 12.3, 11.2, 10.8],
            'binge_drinking': [16.2, 17.5, 16.1, 15.8]
        })
    
    def test_analyze_stroke_data(self):
        """Test stroke data analysis function"""
        result = analyze_stroke_data(self.sample_wide)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)  # Should have 4 states
        self.assertIn('stateabbr', result.columns)
        self.assertIn('stroke_rate', result.columns)
        # Verify sorting is descending
        self.assertGreater(result.iloc[0]['stroke_rate'], result.iloc[-1]['stroke_rate'])
    
    def test_analyze_stroke_data_missing_columns(self):
        """Test error handling for missing columns"""
        bad_data = pd.DataFrame({'column': [1, 2, 3]})
        with self.assertRaises(ValueError):
            analyze_stroke_data(bad_data)


class TestRiskFactorAnalysis(unittest.TestCase):
    """Test risk factor analysis functionality"""
    
    def setUp(self):
        """Create sample data for testing"""
        self.sample_wide = pd.DataFrame({
            'stateabbr': ['CA', 'TX', 'FL', 'NY'],
            'stroke_rate': [5.2, 6.1, 5.8, 6.0],
            'blood_pressure': [25.3, 26.5, 25.1, 24.8],
            'diabetes': [8.5, 9.2, 8.9, 8.8],
            'obesity': [25.1, 26.3, 25.8, 24.5],
            'current_smoking': [15.2, 16.5, 15.1, 14.8],
            'physical_inactivity': [22.3, 23.5, 22.1, 21.8],
            'heart_disease': [4.2, 4.8, 4.1, 3.9],
            'poor_physical_health': [12.3, 13.5, 12.1, 11.8],
            'poor_mental_health': [11.5, 12.3, 11.2, 10.8],
            'binge_drinking': [16.2, 17.5, 16.1, 15.8]
        })
    
    def test_analyze_risk_factors(self):
        """Test risk factors analysis function"""
        correlations = analyze_risk_factors(self.sample_wide)
        self.assertIsInstance(correlations, dict)
        self.assertGreater(len(correlations), 0)
        # All correlation values should be between -1 and 1
        for factor, corr in correlations.items():
            self.assertGreaterEqual(corr, -1.0)
            self.assertLessEqual(corr, 1.0)
    
    def test_analyze_risk_factors_missing_stroke(self):
        """Test error handling for missing stroke_rate"""
        bad_data = pd.DataFrame({'diabetes': [8.5, 9.2, 8.9, 8.8]})
        with self.assertRaises(ValueError):
            analyze_risk_factors(bad_data)


class TestPreventionMeasures(unittest.TestCase):
    """Test prevention measures analysis"""
    
    def setUp(self):
        """Create sample data in long format"""
        self.sample_long = pd.DataFrame({
            'stateabbr': ['CA', 'CA', 'TX', 'TX'],
            'category': ['Prevention', 'Prevention', 'Health Risk Behaviors', 'Health Risk Behaviors'],
            'measure': ['Physical Activity', 'Physical Activity', 'Current Smoking', 'Current Smoking'],
            'data_value': ['75.1', '74.9', '15.2', '15.5']
        })
    
    def test_analyze_prevention_measures(self):
        """Test prevention measures analysis function"""
        result = analyze_prevention_measures(self.sample_long)
        self.assertIsInstance(result, pd.DataFrame)
        if len(result) > 0:
            self.assertIn('stateabbr', result.columns)
            self.assertIn('measure', result.columns)
            self.assertIn('data_value', result.columns)
    
    def test_analyze_prevention_measures_no_data(self):
        """Test handling when no prevention measures exist"""
        bad_data = pd.DataFrame({
            'stateabbr': ['CA'],
            'category': ['Unknown'],
            'measure': ['Unknown'],
            'data_value': ['1.0']
        })
        result = analyze_prevention_measures(bad_data)
        self.assertEqual(len(result), 0)


class TestTableauDataPreparation(unittest.TestCase):
    """Test Tableau data preparation"""
    
    def setUp(self):
        """Create sample data for testing"""
        self.sample_wide = pd.DataFrame({
            'stateabbr': ['CA', 'TX', 'FL', 'NY'],
            'stroke_rate': [5.2, 6.1, 5.8, 6.0],
            'blood_pressure': [25.3, 26.5, 25.1, 24.8],
            'diabetes': [8.5, 9.2, 8.9, 8.8],
            'obesity': [25.1, 26.3, 25.8, 24.5],
            'current_smoking': [15.2, 16.5, 15.1, 14.8],
            'physical_inactivity': [22.3, 23.5, 22.1, 21.8],
            'heart_disease': [4.2, 4.8, 4.1, 3.9],
            'poor_physical_health': [12.3, 13.5, 12.1, 11.8],
            'poor_mental_health': [11.5, 12.3, 11.2, 10.8],
            'binge_drinking': [16.2, 17.5, 16.1, 15.8]
        })
    
    def test_prepare_tableau_data(self):
        """Test Tableau data preparation"""
        tableau_df = prepare_tableau_data(self.sample_wide)
        self.assertIsInstance(tableau_df, pd.DataFrame)
        # Check for new columns
        self.assertIn('state_name', tableau_df.columns)
        self.assertIn('region', tableau_df.columns)
        self.assertIn('stroke_rate_rank', tableau_df.columns)
        self.assertIn('composite_risk_score', tableau_df.columns)
        self.assertIn('risk_category', tableau_df.columns)
        # Check state names were added
        self.assertEqual(tableau_df.iloc[0]['state_name'], 'California')
        self.assertEqual(tableau_df.iloc[1]['state_name'], 'Texas')
    
    def test_prepare_tableau_data_missing_stateabbr(self):
        """Test error handling for missing stateabbr"""
        bad_data = pd.DataFrame({'stroke_rate': [5.2, 6.1]})
        with self.assertRaises(ValueError):
            prepare_tableau_data(bad_data)
    
    def test_ranks_are_calculated(self):
        """Test that ranks are properly calculated"""
        tableau_df = prepare_tableau_data(self.sample_wide)
        # The highest stroke rate should have rank 1
        highest_stroke = tableau_df['stroke_rate'].max()
        rank_of_highest = tableau_df[tableau_df['stroke_rate'] == highest_stroke]['stroke_rate_rank'].values[0]
        self.assertEqual(rank_of_highest, 1.0)
    
    def test_regions_are_assigned(self):
        """Test that regions are properly assigned"""
        tableau_df = prepare_tableau_data(self.sample_wide)
        regions = tableau_df['region'].unique()
        self.assertIn('West', regions)  # CA and TX are in West
        self.assertGreater(len(regions), 0)


if __name__ == '__main__':
    unittest.main()
