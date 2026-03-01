"""
Model Building and Evaluation Module

This module contains functions for training, evaluating, and comparing different
machine learning models for fraud detection.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, auc, precision_recall_curve, f1_score, accuracy_score,
    matthews_corrcoef
)
import joblib
from typing import Dict, Tuple, Any


class FraudDetectionModel:
    """Base class for fraud detection models."""
    
    def __init__(self, model_name: str = "Model"):
        self.model_name = model_name
        self.model = None
        self.metrics = {}
    
    def fit(self, X_train, y_train):
        """Fit the model."""
        raise NotImplementedError
    
    def predict(self, X):
        """Make predictions."""
        raise NotImplementedError
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance."""
        raise NotImplementedError


class RandomForestModel(FraudDetectionModel):
    """Random Forest classifier for fraud detection."""
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        super().__init__("Random Forest")
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=20,
            class_weight='balanced',
            n_jobs=-1
        )
    
    def fit(self, X_train, y_train) -> None:
        """Train the Random Forest model."""
        print(f"Training {self.model_name}...")
        self.model.fit(X_train, y_train)
        print(f"{self.model_name} training completed")
    
    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities."""
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test) -> Dict:
        """Evaluate model performance."""
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)[:, 1]
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_recall_curve(y_test, y_pred_proba)[0].mean(),
            'recall': precision_recall_curve(y_test, y_pred_proba)[1].mean(),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'mcc': matthews_corrcoef(y_test, y_pred),
            'cm': confusion_matrix(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred)
        }
        
        return self.metrics, y_pred, y_pred_proba
    
    def get_feature_importance(self, feature_names: list = None) -> pd.DataFrame:
        """Get feature importance scores."""
        importances = self.model.feature_importances_
        
        if feature_names is None:
            feature_names = [f"Feature_{i}" for i in range(len(importances))]
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def save(self, filepath: str) -> None:
        """Save model to disk."""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load(filepath: str):
        """Load model from disk."""
        model_obj = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
        return model_obj


def train_multiple_models(X_train, y_train, X_test, y_test) -> Dict[str, Dict]:
    """
    Train and evaluate multiple models.
    
    Args:
        X_train: Training features
        y_train: Training target
        X_test: Testing features
        y_test: Testing target
        
    Returns:
        Dictionary with results for each model
    """
    results = {}
    
    # Random Forest
    print("\n" + "="*50)
    print("RANDOM FOREST")
    print("="*50)
    rf_model = RandomForestModel(n_estimators=100)
    rf_model.fit(X_train, y_train)
    metrics_rf, pred_rf, proba_rf = rf_model.evaluate(X_test, y_test)
    results['Random Forest'] = {
        'model': rf_model,
        'metrics': metrics_rf,
        'predictions': pred_rf,
        'probabilities': proba_rf
    }
    
    print("\nMetrics:")
    print(f"Accuracy: {metrics_rf['accuracy']:.4f}")
    print(f"Precision: {metrics_rf['precision']:.4f}")
    print(f"Recall: {metrics_rf['recall']:.4f}")
    print(f"F1-Score: {metrics_rf['f1']:.4f}")
    print(f"ROC-AUC: {metrics_rf['roc_auc']:.4f}")
    print(f"MCC: {metrics_rf['mcc']:.4f}")
    print(f"\nConfusion Matrix:\n{metrics_rf['cm']}")
    print(f"\nClassification Report:\n{metrics_rf['classification_report']}")
    
    return results


def compare_models(results: Dict) -> pd.DataFrame:
    """
    Compare metrics across different models.
    
    Args:
        results: Dictionary with model results
        
    Returns:
        DataFrame with model comparison
    """
    comparison = []
    
    for model_name, model_results in results.items():
        metrics = model_results['metrics']
        comparison.append({
            'Model': model_name,
            'Accuracy': metrics['accuracy'],
            'Precision': metrics['precision'],
            'Recall': metrics['recall'],
            'F1-Score': metrics['f1'],
            'ROC-AUC': metrics['roc_auc'],
            'MCC': metrics['mcc']
        })
    
    comparison_df = pd.DataFrame(comparison)
    print("\n" + "="*80)
    print("MODEL COMPARISON")
    print("="*80)
    print(comparison_df.to_string(index=False))
    
    return comparison_df


def get_roc_curve(y_test, y_pred_proba) -> Tuple:
    """Calculate ROC curve coordinates."""
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr, roc_auc


def get_precision_recall_curve(y_test, y_pred_proba) -> Tuple:
    """Calculate precision-recall curve coordinates."""
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
    return precision, recall, thresholds
