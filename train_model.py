#!/usr/bin/env python3
"""
Quick model training script - Trains and saves the fraud detection model
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.data_processing import preprocess_pipeline
from src.models import RandomForestModel

def main():
    print("=" * 80)
    print("CREDIT CARD FRAUD DETECTION - MODEL TRAINING")
    print("=" * 80)
    
    # Step 1: Load and preprocess data
    print("\n📊 Step 1: Loading and preprocessing data...")
    try:
        X_train, X_test, y_train, y_test, scaler = preprocess_pipeline(
            'data/creditcard.csv',
            test_size=0.2,
            scale=True
        )
        print("✅ Data loaded and preprocessed successfully")
    except FileNotFoundError:
        print("❌ Error: data/creditcard.csv not found!")
        print("   Please download from: https://www.kaggle.com/mlg-ulb/creditcardfraud")
        return
    
    # Step 2: Train model
    print("\n🤖 Step 2: Training Random Forest model...")
    model = RandomForestModel(n_estimators=100)
    model.fit(X_train, y_train)
    print("✅ Model training completed")
    
    # Step 3: Evaluate model
    print("\n📈 Step 3: Evaluating model...")
    metrics, predictions, probabilities = model.evaluate(X_test, y_test)
    
    print("\n✅ MODEL PERFORMANCE:")
    print(f"   Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"   Precision: {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
    print(f"   Recall:    {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
    print(f"   F1-Score:  {metrics['f1']:.4f}")
    print(f"   ROC-AUC:   {metrics['roc_auc']:.4f} ({metrics['roc_auc']*100:.2f}%)")
    print(f"   MCC:       {metrics['mcc']:.4f}")
    
    # Step 4: Save model
    print("\n💾 Step 4: Saving model...")
    model.save('models/fraud_detection_model.pkl')
    print("✅ Model saved to: models/fraud_detection_model.pkl")
    
    print("\n" + "=" * 80)
    print("🎉 MODEL TRAINING COMPLETE!")
    print("=" * 80)
    print("\n✅ Next steps:")
    print("   1. Refresh your Streamlit dashboard at http://localhost:8501")
    print("   2. The app will now load the real trained model")
    print("   3. Try analyzing transactions in the dashboard!")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
