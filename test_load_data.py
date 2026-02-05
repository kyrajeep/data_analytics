import unittest
import pandas as pd
import numpy as np
from load_data import (
    detect_duplicates, 
    remove_duplicates, 
    analyze_missing_values,
    check_state_coverage,
    clean_missing_values,
    validate_data_quality
)

class TestDetectDuplicates(unittest.TestCase):
    """Test duplicate detection functionality"""
    
    def setUp(self):
        """Create sample data for testing"""
        self.sample_data = pd.DataFrame({
            'stateabbr': ['CA', 'CA', 'TX', 'TX'],
            'measureid': ['STROKE', 'STROKE', 'STROKE', 'DIABETES'],
            'data_value': [5.2, 5.2, 6.1, 8.5]
        })
    
    def test_detect_duplicates_found(self):
        """Test detection of duplicate rows"""
        duplicates = detect_duplicates(self.sample_data)
        self.assertEqual(len(duplicates), 2)  # Two identical CA STROKE rows
    
    def test_detect_duplicates_none(self):
        """Test when no duplicates exist"""
        unique_data = self.sample_data.drop_duplicates(keep='first')
        duplicates = detect_duplicates(unique_data)
        self.assertEqual(len(duplicates), 0)
    
    def test_remove_duplicates(self):
        """Test removal of duplicate rows"""
        deduplicated = remove_duplicates(self.sample_data)
        self.assertEqual(len(deduplicated), 3)  # Should have 3 unique rows


class TestMissingValues(unittest.TestCase):
    """Test missing value analysis and cleaning"""
    
    def setUp(self):
        """Create sample data with missing values"""
        self.sample_data = pd.DataFrame({
            'stateabbr': ['CA', 'TX', 'FL', 'NY'],
            'stroke_rate': [5.2, np.nan, 5.8, 6.1],
            'diabetes': [8.5, 9.2, np.nan, 8.9],
            'obesity': [25.1, 26.3, 25.8, 24.5]
        })
    
    def test_analyze_missing_values(self):
        """Test missing value analysis"""
        missing_df = analyze_missing_values(self.sample_data)
        self.assertEqual(len(missing_df), 2)  # Two columns with missing values
        self.assertIn('stroke_rate', missing_df['Column'].values)
        self.assertIn('diabetes', missing_df['Column'].values)
    
    def test_clean_missing_values(self):
        """Test cleaning of missing values"""
        cleaned = clean_missing_values(self.sample_data)
        self.assertEqual(cleaned.isnull().sum().sum(), 0)  # No missing values
    
    def test_validate_data_quality(self):
        """Test data quality validation"""
        cleaned = clean_missing_values(self.sample_data)
        metrics = validate_data_quality(cleaned)
        self.assertEqual(metrics['missing_values'], 0)
        self.assertEqual(metrics['total_rows'], 4)


class TestStateCoverage(unittest.TestCase):
    """Test state coverage analysis"""
    
    def setUp(self):
        """Create sample data"""
        self.sample_data = pd.DataFrame({
            'stateabbr': ['CA', 'TX', 'FL'],
            'stroke_rate': [5.2, 6.1, 5.8],
            'diabetes': [8.5, 9.2, 8.9]
        })
    
    def test_check_state_coverage(self):
        """Test state coverage check"""
        # This should not raise an error
        try:
            check_state_coverage(self.sample_data)
            coverage_ok = True
        except:
            coverage_ok = False
        self.assertTrue(coverage_ok)


class TestDataQuality(unittest.TestCase):
    """Test data quality validation"""
    
    def setUp(self):
        """Create sample data"""
        self.sample_data = pd.DataFrame({
            'stateabbr': ['CA', 'TX', 'FL', 'NY'],
            'stroke_rate': [5.2, 6.1, 5.8, 6.0],
            'diabetes': [8.5, 9.2, 8.9, 8.8],
            'obesity': [25.1, 26.3, 25.8, 24.5]
        })
    
    def test_validate_clean_data(self):
        """Test validation of clean data"""
        metrics = validate_data_quality(self.sample_data)
        self.assertEqual(metrics['missing_values'], 0)
        self.assertEqual(metrics['duplicate_rows'], 0)
        self.assertEqual(metrics['total_rows'], 4)
        self.assertEqual(metrics['total_columns'], 4)


if __name__ == '__main__':
    unittest.main()
