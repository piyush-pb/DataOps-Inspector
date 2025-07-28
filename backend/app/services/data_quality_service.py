import pandas as pd
import numpy as np
from typing import List, Dict, Any
import json

class DataQualityService:
    """Service for running data quality checks"""
    
    def run_quality_checks(self, df: pd.DataFrame, source_id: int) -> List[Dict[str, Any]]:
        """Run comprehensive data quality checks"""
        results = []
        
        # Check for missing values
        results.append(self._check_missing_values(df))
        
        # Check for duplicates
        results.append(self._check_duplicates(df))
        
        # Check data types
        results.append(self._check_data_types(df))
        
        # Check for outliers (basic implementation)
        results.append(self._check_outliers(df))
        
        # Check data completeness
        results.append(self._check_completeness(df))
        
        return results
    
    def _check_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for missing values in the dataset"""
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100
        
        total_missing = missing_counts.sum()
        total_missing_percentage = (total_missing / (len(df) * len(df.columns))) * 100
        
        # Determine status based on missing percentage
        if total_missing_percentage == 0:
            status = "passed"
            score = 1.0
        elif total_missing_percentage < 5:
            status = "warning"
            score = 0.8
        elif total_missing_percentage < 20:
            status = "warning"
            score = 0.6
        else:
            status = "failed"
            score = 0.2
        
        return {
            "check_type": "missing_values",
            "result": {
                "total_missing": int(total_missing),
                "total_missing_percentage": round(total_missing_percentage, 2),
                "missing_by_column": missing_percentages.to_dict()
            },
            "status": status,
            "score": score,
            "details": f"Found {total_missing} missing values ({total_missing_percentage:.2f}%)"
        }
    
    def _check_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for duplicate rows"""
        duplicate_count = df.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(df)) * 100
        
        if duplicate_count == 0:
            status = "passed"
            score = 1.0
        elif duplicate_percentage < 1:
            status = "warning"
            score = 0.9
        elif duplicate_percentage < 5:
            status = "warning"
            score = 0.7
        else:
            status = "failed"
            score = 0.3
        
        return {
            "check_type": "duplicates",
            "result": {
                "duplicate_count": int(duplicate_count),
                "duplicate_percentage": round(duplicate_percentage, 2)
            },
            "status": status,
            "score": score,
            "details": f"Found {duplicate_count} duplicate rows ({duplicate_percentage:.2f}%)"
        }
    
    def _check_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check data types and potential type issues"""
        type_issues = []
        score = 1.0
        
        for column in df.columns:
            # Check for mixed types
            if df[column].dtype == 'object':
                # Try to detect if it should be numeric
                try:
                    pd.to_numeric(df[column], errors='raise')
                    type_issues.append(f"Column '{column}' appears to be numeric but is stored as object")
                    score -= 0.1
                except:
                    pass
                
                # Check for date-like strings
                if df[column].str.contains(r'\d{4}-\d{2}-\d{2}', na=False).any():
                    type_issues.append(f"Column '{column}' appears to contain dates but is stored as object")
                    score -= 0.1
        
        if type_issues:
            status = "warning"
            score = max(0.5, score)
        else:
            status = "passed"
        
        return {
            "check_type": "data_types",
            "result": {
                "type_issues": type_issues,
                "dtypes": df.dtypes.to_dict()
            },
            "status": status,
            "score": score,
            "details": f"Found {len(type_issues)} potential data type issues"
        }
    
    def _check_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Basic outlier detection using IQR method"""
        outlier_issues = []
        score = 1.0
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            outlier_count = len(outliers)
            outlier_percentage = (outlier_count / len(df)) * 100
            
            if outlier_percentage > 10:
                outlier_issues.append({
                    "column": column,
                    "outlier_count": outlier_count,
                    "outlier_percentage": round(outlier_percentage, 2)
                })
                score -= 0.1
        
        if outlier_issues:
            status = "warning"
            score = max(0.6, score)
        else:
            status = "passed"
        
        return {
            "check_type": "outliers",
            "result": {
                "outlier_issues": outlier_issues,
                "numeric_columns_checked": len(numeric_columns)
            },
            "status": status,
            "score": score,
            "details": f"Found outliers in {len(outlier_issues)} numeric columns"
        }
    
    def _check_completeness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check overall data completeness"""
        total_cells = len(df) * len(df.columns)
        non_null_cells = df.count().sum()
        completeness_percentage = (non_null_cells / total_cells) * 100
        
        if completeness_percentage >= 95:
            status = "passed"
            score = 1.0
        elif completeness_percentage >= 80:
            status = "warning"
            score = 0.8
        elif completeness_percentage >= 60:
            status = "warning"
            score = 0.6
        else:
            status = "failed"
            score = 0.3
        
        return {
            "check_type": "completeness",
            "result": {
                "total_cells": total_cells,
                "non_null_cells": non_null_cells,
                "completeness_percentage": round(completeness_percentage, 2)
            },
            "status": status,
            "score": score,
            "details": f"Data completeness: {completeness_percentage:.2f}%"
        } 