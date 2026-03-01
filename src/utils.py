"""
Utility Functions Module

This module contains helper functions for common tasks used throughout the pipeline.
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Any, Dict, List
import joblib


def create_directory(path: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        path (str): Directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")


def save_object(obj: Any, filepath: str) -> None:
    """
    Save Python object using joblib.
    
    Args:
        obj: Object to save
        filepath: Path to save file
    """
    create_directory(os.path.dirname(filepath))
    joblib.dump(obj, filepath)
    print(f"Object saved: {filepath}")


def load_object(filepath: str) -> Any:
    """
    Load Python object using joblib.
    
    Args:
        filepath: Path to load file
        
    Returns:
        Loaded object
    """
    obj = joblib.load(filepath)
    print(f"Object loaded: {filepath}")
    return obj


def save_config(config: Dict, filepath: str) -> None:
    """
    Save configuration as JSON.
    
    Args:
        config: Configuration dictionary
        filepath: Path to save file
    """
    create_directory(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Config saved: {filepath}")


def load_config(filepath: str) -> Dict:
    """
    Load configuration from JSON.
    
    Args:
        filepath: Path to load file
        
    Returns:
        Configuration dictionary
    """
    with open(filepath, 'r') as f:
        config = json.load(f)
    print(f"Config loaded: {filepath}")
    return config


def print_separator(title: str = "", length: int = 80) -> None:
    """
    Print a separator line for console output.
    
    Args:
        title: Title to display
        length: Length of separator
    """
    if title:
        print(f"\n{'='*length}")
        print(f"{title.center(length)}")
        print(f"{'='*length}\n")
    else:
        print(f"\n{'='*length}\n")


def get_timestamp() -> str:
    """
    Get current timestamp as string.
    
    Returns:
        Formatted timestamp
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_message(message: str, level: str = "INFO") -> str:
    """
    Format log message with timestamp.
    
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
        
    Returns:
        Formatted log message
    """
    timestamp = get_timestamp()
    return f"[{timestamp}] [{level}] {message}"


def print_metrics_summary(metrics: Dict) -> None:
    """
    Print model metrics in formatted table.
    
    Args:
        metrics: Dictionary of metrics
    """
    print_separator("MODEL PERFORMANCE METRICS")
    
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key:.<40} {value:.4f}")
        elif isinstance(value, int):
            print(f"{key:.<40} {value}")
        else:
            print(f"{key:.<40} {str(value)[:40]}")


def create_sample_transaction(n_features: int = 30) -> np.ndarray:
    """
    Create a random sample transaction for testing.
    
    Args:
        n_features: Number of features
        
    Returns:
        Sample transaction array
    """
    return np.random.randn(n_features)


def scale_value(value: float, min_val: float, max_val: float) -> float:
    """
    Scale value to 0-1 range.
    
    Args:
        value: Value to scale
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Scaled value
    """
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)


def get_risk_level(probability: float) -> str:
    """
    Convert fraud probability to risk level.
    
    Args:
        probability: Fraud probability (0-1)
        
    Returns:
        Risk level string
    """
    if probability < 0.3:
        return "LOW"
    elif probability < 0.6:
        return "MEDIUM"
    elif probability < 0.8:
        return "HIGH"
    else:
        return "CRITICAL"


def get_risk_color(probability: float) -> str:
    """
    Get color code for risk level.
    
    Args:
        probability: Fraud probability (0-1)
        
    Returns:
        Color code (if using in plots): returns string
    """
    level = get_risk_level(probability)
    color_map = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "orange",
        "CRITICAL": "red"
    }
    return color_map[level]


def create_summary_report(results: Dict) -> str:
    """
    Create a text summary report.
    
    Args:
        results: Results dictionary
        
    Returns:
        Formatted report string
    """
    report = f"""
    {'='*80}
    CREDIT CARD FRAUD DETECTION - SUMMARY REPORT
    {'='*80}
    
    Generated: {get_timestamp()}
    
    Model Performance:
    ─────────────────────────────────────────
    """
    
    if 'metrics' in results:
        metrics = results['metrics']
        report += f"""
    Accuracy:  {metrics.get('accuracy', 'N/A'):.4f}
    Precision: {metrics.get('precision', 'N/A'):.4f}
    Recall:    {metrics.get('recall', 'N/A'):.4f}
    F1-Score:  {metrics.get('f1', 'N/A'):.4f}
    ROC-AUC:   {metrics.get('roc_auc', 'N/A'):.4f}
    MCC:       {metrics.get('mcc', 'N/A'):.4f}
    """
    
    report += f"\n    {'='*80}\n"
    return report


def batch_process_predictions(predictions_list: List[Dict]) -> pd.DataFrame:
    """
    Convert list of predictions to DataFrame.
    
    Args:
        predictions_list: List of prediction dictionaries
        
    Returns:
        DataFrame with predictions
    """
    return pd.DataFrame(predictions_list)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Result of division
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default


def format_currency(amount: float) -> str:
    """
    Format amount as currency.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Value to format
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value*100:.{decimals}f}%"
