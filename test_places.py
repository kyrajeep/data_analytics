import unittest
import pandas as pd
import numpy as np
from places import analyze_stroke_data, analyze_risk_factors, analyze_prevention_measures

class TestPlacesAnalysis(unittest.TestCase):
    def setUp(self):
        """Create sample data for testing"""
        self.sample_data = pd.DataFrame({
            'category': ['Health Outcomes', 'Health Outcomes', 'Prevention'],
            'measure': ['Stroke', 'High Blood Pressure', 'Physical Activity'],
            'data_value': ['5.2', '25.3', '75.1'],
            'stateabbr': ['CA', 'CA', 'CA']
        })

    def test_analyze_stroke_data(self):
        """Test stroke data analysis function"""
        result = analyze_stroke_data(self.sample_data)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)  # Should have one state
        self.assertEqual(result['stateabbr'].iloc[0], 'CA')

    def test_analyze_risk_factors(self):
        """Test risk factors analysis function"""
        result = analyze_risk_factors(self.sample_data)
        self.assertIsInstance(result, dict)
        
    def test_analyze_prevention_measures(self):
        """Test prevention measures analysis function"""
        result = analyze_prevention_measures(self.sample_data)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue('measure' in result.columns)
        self.assertTrue('stateabbr' in result.columns)

if __name__ == '__main__':
    unittest.main()