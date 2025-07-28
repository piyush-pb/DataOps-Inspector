import pickle
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import random

class ModelMonitoringService:
    """Service for ML model monitoring and drift detection"""
    
    def __init__(self):
        self.models = {}
        self.model_path = "models"
        os.makedirs(self.model_path, exist_ok=True)
        
        # Initialize with sample models
        self._initialize_sample_models()
    
    def _initialize_sample_models(self):
        """Initialize with sample ML models"""
        # Sample classification model (Iris dataset)
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import load_iris
        from sklearn.model_selection import train_test_split
        
        # Load iris dataset
        iris = load_iris()
        X, y = iris.data, iris.target
        
        # Train a simple model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Save model
        model_file = os.path.join(self.model_path, "iris_classifier.pkl")
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)
        
        self.models["iris_classifier"] = {
            "model": model,
            "file_path": model_file,
            "type": "classification",
            "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
            "target": "species",
            "version": "1.0"
        }
        
        # Sample regression model
        from sklearn.linear_model import LinearRegression
        from sklearn.datasets import load_boston
        
        # Load boston dataset
        boston = load_boston()
        X_reg, y_reg = boston.data, boston.target
        
        # Train regression model
        reg_model = LinearRegression()
        reg_model.fit(X_reg, y_reg)
        
        # Save model
        reg_model_file = os.path.join(self.model_path, "boston_regressor.pkl")
        with open(reg_model_file, 'wb') as f:
            pickle.dump(reg_model, f)
        
        self.models["boston_regressor"] = {
            "model": reg_model,
            "file_path": reg_model_file,
            "type": "regression",
            "features": boston.feature_names.tolist(),
            "target": "price",
            "version": "1.0"
        }
    
    def deploy_sample_model(self, model_name: str, model_type: str = "classification") -> Dict[str, Any]:
        """Deploy a sample model"""
        if model_name in self.models:
            return {
                "version": self.models[model_name]["version"],
                "type": self.models[model_name]["type"],
                "features": self.models[model_name]["features"]
            }
        
        # Create a new sample model
        if model_type == "classification":
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.datasets import make_classification
            
            X, y = make_classification(n_samples=1000, n_features=4, random_state=42)
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            model.fit(X, y)
            
            features = [f"feature_{i}" for i in range(4)]
        else:
            from sklearn.linear_model import LinearRegression
            from sklearn.datasets import make_regression
            
            X, y = make_regression(n_samples=1000, n_features=4, random_state=42)
            model = LinearRegression()
            model.fit(X, y)
            
            features = [f"feature_{i}" for i in range(4)]
        
        # Save model
        model_file = os.path.join(self.model_path, f"{model_name}.pkl")
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)
        
        self.models[model_name] = {
            "model": model,
            "file_path": model_file,
            "type": model_type,
            "features": features,
            "target": "target",
            "version": "1.0"
        }
        
        return {
            "version": "1.0",
            "type": model_type,
            "features": features
        }
    
    def get_deployed_models(self) -> List[str]:
        """Get list of deployed models"""
        return list(self.models.keys())
    
    def make_prediction(self, model_name: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make a prediction using the deployed model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model_info = self.models[model_name]
        model = model_info["model"]
        
        # Convert features to array
        feature_values = []
        for feature in model_info["features"]:
            if feature in features:
                feature_values.append(features[feature])
            else:
                feature_values.append(0.0)  # Default value
        
        X = np.array([feature_values])
        
        # Make prediction
        if model_info["type"] == "classification":
            prediction = model.predict(X)[0]
            confidence = max(model.predict_proba(X)[0]) if hasattr(model, 'predict_proba') else 0.8
        else:
            prediction = model.predict(X)[0]
            confidence = 0.9  # For regression, we'll use a fixed confidence
        
        return {
            "prediction": float(prediction),
            "confidence": float(confidence),
            "model_name": model_name,
            "model_version": model_info["version"],
            "features_used": model_info["features"]
        }
    
    def check_model_drift(self, model_name: str) -> List[Dict[str, Any]]:
        """Check for model drift using various methods"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model_info = self.models[model_name]
        model = model_info["model"]
        
        drift_results = []
        
        # Simulate feature drift detection
        for feature in model_info["features"]:
            # Simulate drift score (in real implementation, this would compare distributions)
            drift_score = random.uniform(0.1, 0.3)  # Simulated drift score
            threshold = 0.2
            
            drift_results.append({
                "drift_type": "feature_drift",
                "drift_score": round(drift_score, 3),
                "threshold": threshold,
                "is_drift_detected": drift_score > threshold,
                "feature_name": feature,
                "details": f"Feature drift detected for {feature} with score {drift_score:.3f}"
            })
        
        # Simulate prediction drift
        pred_drift_score = random.uniform(0.05, 0.25)
        pred_threshold = 0.15
        
        drift_results.append({
            "drift_type": "prediction_drift",
            "drift_score": round(pred_drift_score, 3),
            "threshold": pred_threshold,
            "is_drift_detected": pred_drift_score > pred_threshold,
            "feature_name": None,
            "details": f"Prediction drift detected with score {pred_drift_score:.3f}"
        })
        
        # Simulate data drift
        data_drift_score = random.uniform(0.1, 0.4)
        data_threshold = 0.25
        
        drift_results.append({
            "drift_type": "data_drift",
            "drift_score": round(data_drift_score, 3),
            "threshold": data_threshold,
            "is_drift_detected": data_drift_score > data_threshold,
            "feature_name": None,
            "details": f"Data drift detected with score {data_drift_score:.3f}"
        })
        
        return drift_results
    
    def get_model_performance_metrics(self, model_name: str) -> Dict[str, float]:
        """Get model performance metrics"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        # Simulate performance metrics
        return {
            "accuracy": random.uniform(0.75, 0.95),
            "precision": random.uniform(0.70, 0.90),
            "recall": random.uniform(0.70, 0.90),
            "f1_score": random.uniform(0.70, 0.90)
        } 