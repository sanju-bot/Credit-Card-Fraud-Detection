"""
Data Processing Module

This module handles data loading, cleaning, preprocessing, and train-test splits
for the credit card fraud detection pipeline.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple


def load_data(path: str) -> pd.DataFrame:
    """
    Load credit card fraud dataset from CSV.
    
    Args:
        path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: DataFrame containing the dataset
    """
    try:
        df = pd.read_csv(path)
        print(f"Dataset loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
        raise
    except Exception as e:
        print(f"Error loading data: {e}")
        raise


def explore_data(df: pd.DataFrame) -> dict:
    """
    Explore basic statistics of the dataset.
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        dict: Dictionary containing exploration results
    """
    exploration = {
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "fraud_distribution": df['Class'].value_counts().to_dict() if 'Class' in df.columns else {},
        "fraud_percentage": (df['Class'].value_counts(normalize=True) * 100).to_dict() if 'Class' in df.columns else {},
        "data_types": df.dtypes.to_dict(),
    }
    return exploration


def separate_features_target(df: pd.DataFrame, target_col: str = 'Class') -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separate features and target variable.
    
    Args:
        df (pd.DataFrame): Input dataset
        target_col (str): Name of target column
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: Features and target variables
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset")
    
    X = df.drop([target_col], axis=1)
    y = df[target_col]
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    return X, y


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df (pd.DataFrame): Input dataset
        strategy (str): Strategy to handle missing values ('drop' or 'mean')
        
    Returns:
        pd.DataFrame: Dataset with missing values handled
    """
    missing_count = df.isnull().sum().sum()
    
    if missing_count == 0:
        print("No missing values found in the dataset")
        return df
    
    if strategy == 'drop':
        df = df.dropna()
        print(f"Dropped rows with missing values. New shape: {df.shape}")
    elif strategy == 'mean':
        df = df.fillna(df.mean())
        print("Filled missing values with mean")
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    return df


def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, 
               random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split data into training and testing sets with stratification.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target variable
        test_size (float): Proportion of test set (default: 0.2)
        random_state (int): Random seed for reproducibility
        
    Returns:
        Tuple: X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y  # Maintain class distribution
    )
    
    print(f"Training set size: {X_train.shape}")
    print(f"Testing set size: {X_test.shape}")
    print(f"Training fraud rate: {y_train.mean():.4f}")
    print(f"Testing fraud rate: {y_test.mean():.4f}")
    
    return X_train, X_test, y_train, y_test


def scale_features(X_train: np.ndarray, X_test: np.ndarray, 
                   scaler=None) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Scale features using StandardScaler.
    
    Args:
        X_train (np.ndarray): Training features
        X_test (np.ndarray): Testing features
        scaler (StandardScaler, optional): Pre-fitted scaler
        
    Returns:
        Tuple: Scaled X_train, scaled X_test, and the scaler object
    """
    if scaler is None:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
    else:
        X_train_scaled = scaler.transform(X_train)
    
    X_test_scaled = scaler.transform(X_test)
    
    print("Features scaled successfully")
    
    return X_train_scaled, X_test_scaled, scaler


def preprocess_pipeline(csv_path: str, test_size: float = 0.2, 
                       scale: bool = True) -> Tuple:
    """
    Complete preprocessing pipeline.
    
    Args:
        csv_path (str): Path to CSV file
        test_size (float): Proportion of test set
        scale (bool): Whether to scale features
        
    Returns:
        Tuple: Processed train/test data and scaler
    """
    # Load and explore
    df = load_data(csv_path)
    exploration = explore_data(df)
    print("\nDataset Exploration:")
    print(f"Shape: {exploration['shape']}")
    print(f"Missing values: {sum(exploration['missing_values'].values())}")
    print(f"Fraud distribution: {exploration['fraud_distribution']}")
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Separate features and target
    X, y = separate_features_target(df)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=test_size)
    
    # Scale features
    if scale:
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train.values, X_test.values)
        return X_train_scaled, X_test_scaled, y_train.values, y_test.values, scaler
    else:
        return X_train.values, X_test.values, y_train.values, y_test.values, None
