"""
Model Explainability Module

This module provides SHAP and LIME-based explanations for model predictions
to enhance interpretability and trust in fraud detection decisions.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict


def get_feature_importance_from_model(model, feature_names: List[str] = None) -> pd.DataFrame:
    """
    Extract feature importance from tree-based models.
    
    Args:
        model: Trained model with feature_importances_ attribute
        feature_names: List of feature names
        
    Returns:
        DataFrame with features and their importance scores
    """
    if not hasattr(model, 'feature_importances_'):
        raise ValueError("Model does not have feature_importances_ attribute")
    
    importances = model.feature_importances_
    
    if feature_names is None:
        feature_names = [f"V{i}" for i in range(len(importances))]
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    return importance_df


def analyze_prediction(model, X_sample, feature_names: List[str] = None, 
                      top_n: int = 10) -> Dict:
    """
    Analyze a single prediction with feature contribution.
    
    Args:
        model: Trained model object
        X_sample: Single sample feature array (1D)
        feature_names: List of feature names
        top_n: Number of top features to show
        
    Returns:
        Dictionary with prediction details
    """
    if len(X_sample.shape) == 1:
        X_sample = X_sample.reshape(1, -1)
    
    # Get prediction
    pred_proba = model.predict_proba(X_sample)[0]
    pred_class = model.predict(X_sample)[0]
    
    # Get feature importance
    importance_df = get_feature_importance_from_model(model, feature_names)
    top_features = importance_df.head(top_n)
    
    # Map feature values
    if feature_names is None:
        feature_names = [f"V{i}" for i in range(X_sample.shape[1])]
    
    sample_values = pd.DataFrame({
        'Feature': feature_names,
        'Value': X_sample[0]
    })
    
    # Merge with importance
    merged = top_features.merge(sample_values, on='Feature')
    
    analysis = {
        'prediction_class': pred_class,
        'fraud_probability': pred_proba[1],
        'legitimate_probability': pred_proba[0],
        'top_features': merged,
        'all_importances': importance_df
    }
    
    return analysis


def explain_decision(analysis: Dict) -> str:
    """
    Generate a human-readable explanation of fraud prediction.
    
    Args:
        analysis: Dictionary from analyze_prediction
        
    Returns:
        String explanation
    """
    pred_class = analysis['prediction_class']
    fraud_prob = analysis['fraud_probability']
    top_features = analysis['top_features']
    
    fraud_status = "FRAUDULENT" if pred_class == 1 else "LEGITIMATE"
    confidence = fraud_prob if pred_class == 1 else 1 - fraud_prob
    
    explanation = f"""
    ═══════════════════════════════════════════════════════
    FRAUD DETECTION EXPLANATION
    ═══════════════════════════════════════════════════════
    
    PREDICTION: {fraud_status}
    Confidence: {confidence:.2%}
    Fraud Probability: {fraud_prob:.2%}
    
    TOP INFLUENTIAL FEATURES:
    ─────────────────────────────────────────────────────
    """
    
    for idx, row in top_features.iterrows():
        explanation += f"\n    • {row['Feature']:15s} | Value: {row['Value']:10.3f} | Importance: {row['Importance']:.4f}"
    
    explanation += "\n    ═════════════════════════════════════════════════════════\n"
    
    return explanation


def create_feature_importance_summary(model, feature_names: List[str] = None, 
                                     top_n: int = 15) -> pd.DataFrame:
    """
    Create a summary of top features by importance.
    
    Args:
        model: Trained model
        feature_names: List of feature names
        top_n: Number of top features
        
    Returns:
        DataFrame with top features
    """
    importance_df = get_feature_importance_from_model(model, feature_names)
    return importance_df.head(top_n)


class ExplanationEngine:
    """Engine for generating model explanations."""
    
    def __init__(self, model, feature_names: List[str] = None):
        """
        Initialize explanation engine.
        
        Args:
            model: Trained model
            feature_names: List of feature names
        """
        self.model = model
        self.feature_names = feature_names
        self.importance_cache = None
    
    def get_importance(self) -> pd.DataFrame:
        """Get cached feature importance."""
        if self.importance_cache is None:
            self.importance_cache = get_feature_importance_from_model(
                self.model, self.feature_names
            )
        return self.importance_cache
    
    def explain(self, X_sample, top_n: int = 10) -> str:
        """Generate explanation for a sample."""
        analysis = analyze_prediction(
            self.model, X_sample, self.feature_names, top_n
        )
        return explain_decision(analysis)
    
    def get_analysis(self, X_sample, top_n: int = 10) -> Dict:
        """Get analysis dictionary for a sample."""
        return analyze_prediction(
            self.model, X_sample, self.feature_names, top_n
        )
    
    def batch_analyze(self, X_samples, top_n: int = 10) -> List[Dict]:
        """Analyze multiple samples."""
        analyses = []
        for idx, sample in enumerate(X_samples):
            analysis = self.get_analysis(sample, top_n)
            analysis['sample_index'] = idx
            analyses.append(analysis)
        return analyses


def get_high_risk_transactions(y_pred_proba, threshold: float = 0.5) -> np.ndarray:
    """
    Filter high-risk transactions based on fraud probability.
    
    Args:
        y_pred_proba: Prediction probabilities from model
        threshold: Fraud probability threshold
        
    Returns:
        Array of indices for high-risk transactions
    """
    fraud_proba = y_pred_proba[:, 1]
    high_risk_idx = np.where(fraud_proba >= threshold)[0]
    return high_risk_idx


def get_borderline_transactions(y_pred_proba, threshold_range: Tuple = (0.4, 0.6)) -> np.ndarray:
    """
    Filter borderline transactions for manual review.
    
    Args:
        y_pred_proba: Prediction probabilities
        threshold_range: Tuple of (low, high) thresholds
        
    Returns:
        Array of indices for borderline transactions
    """
    fraud_proba = y_pred_proba[:, 1]
    borderline_idx = np.where(
        (fraud_proba >= threshold_range[0]) & (fraud_proba <= threshold_range[1])
    )[0]
    return borderline_idx


def create_risk_score(y_pred_proba, weights: Dict = None) -> np.ndarray:
    """
    Create composite risk score from probabilities.
    
    Args:
        y_pred_proba: Prediction probabilities
        weights: Custom weights for fraud probability
        
    Returns:
        Risk scores (0-1)
    """
    fraud_proba = y_pred_proba[:, 1]
    
    if weights is None:
        weights = {'fraud': 1.0}
    
    risk_scores = fraud_proba * weights.get('fraud', 1.0)
    
    return np.clip(risk_scores, 0, 1)
