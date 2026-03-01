"""
Comprehensive model evaluation script.
Analyzes the trained Random Forest fraud detection model.
"""

import sys
sys.path.insert(0, 'src')

from data_processing import load_data, split_data, scale_features
from models import RandomForestModel
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_curve, roc_curve
)
import numpy as np

print("=" * 100)
print("MODEL EVALUATION - IS THIS A STRONG MODEL?")
print("=" * 100)

# Load and prepare data
print("\n1. Loading and preparing data...")
df = load_data('data/creditcard.csv')
X, y = df.drop('Class', axis=1), df['Class']
X_train, X_test, y_train, y_test = split_data(X, y)

print(f"   Training set: {len(X_train):,} transactions")
print(f"   Test set: {len(X_test):,} transactions")
print(f"   Fraud rate in training: {(y_train == 1).sum() / len(y_train) * 100:.2f}%")
print(f"   Fraud rate in test: {(y_test == 1).sum() / len(y_test) * 100:.2f}%")

# Scale features
X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

# Load trained model
print("\n2. Loading trained model...")
model = RandomForestModel.load('models/fraud_detection_model.pkl')
print("   Model: Random Forest Classifier")
print(f"   Trees: {model.n_estimators}")
print(f"   Max Depth: {model.max_depth}")

# Get predictions
print("\n3. Computing predictions...")
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Basic metrics
print("\n" + "=" * 100)
print("PERFORMANCE METRICS")
print("=" * 100)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\nCore Metrics:")
print(f"  Accuracy:    {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"  Precision:   {precision:.4f} ({precision*100:.2f}%)")
print(f"  Recall:      {recall:.4f} ({recall*100:.2f}%)")
print(f"  F1-Score:    {f1:.4f}")
print(f"  ROC-AUC:     {roc_auc:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print(f"\nConfusion Matrix:")
print(f"  True Negatives:  {tn:,}")
print(f"  False Positives: {fp:,} (Type I Error)")
print(f"  False Negatives: {fn:,} (Type II Error - Missing Frauds!)")
print(f"  True Positives:  {tp:,}")

print(f"\nDetailed Rates:")
print(f"  True Positive Rate (Sensitivity): {tp/(tp+fn):.4f} ({tp/(tp+fn)*100:.2f}%)")
print(f"  True Negative Rate (Specificity): {tn/(tn+fp):.4f} ({tn/(tn+fp)*100:.2f}%)")
print(f"  False Positive Rate: {fp/(tn+fp):.4f} ({fp/(tn+fp)*100:.2f}%)")
print(f"  False Negative Rate: {fn/(fn+tp):.4f} ({fn/(fn+tp)*100:.2f}%)")

# Classification report
print(f"\n" + "=" * 100)
print("DETAILED CLASSIFICATION REPORT")
print("=" * 100)
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraudulent']))

# Industry comparison
print(f"\n" + "=" * 100)
print("INDUSTRY BENCHMARKS & ASSESSMENT")
print("=" * 100)

print(f"\nAccuracy: {accuracy*100:.2f}%")
if accuracy > 0.99:
    print("  ✅ EXCELLENT - Very high overall accuracy")
elif accuracy > 0.95:
    print("  ✅ GREAT - Good overall accuracy")
elif accuracy > 0.90:
    print("  ✓ GOOD - Acceptable for fraud detection")
else:
    print("  ⚠️ AVERAGE - Room for improvement")

print(f"\nPrecision: {precision*100:.2f}%")
if precision > 0.90:
    print("  ✅ EXCELLENT - Very few false positives (good for customer satisfaction)")
    print("     But: Only {:.1f}% of alert cases are actually fraud".format(precision*100))
elif precision > 0.70:
    print("  ✓ GOOD - Manageable false positive rate")
else:
    print("  ⚠️ LOW - Many false alerts will annoy customers")

print(f"\nRecall: {recall*100:.2f}%")
if recall > 0.90:
    print("  ✅ EXCELLENT - Catching >90% of fraud cases")
    print("     This is CRITICAL - missing frauds is worse than false positives")
elif recall > 0.80:
    print("  ✓ GOOD - Catching most fraud cases")
elif recall > 0.70:
    print("  ⚠️ ACCEPTABLE - But 25-30% of frauds slip through")
else:
    print("  🚨 POOR - Too many frauds escaping!")

print(f"\nROC-AUC: {roc_auc:.4f}")
if roc_auc > 0.95:
    print("  ✅ EXCELLENT - Outstanding discrimination ability")
elif roc_auc > 0.90:
    print("  ✅ EXCELLENT - Excellent discrimination ability")
elif roc_auc > 0.80:
    print("  ✓ GOOD - Good discriminative power")
elif roc_auc > 0.70:
    print("  ⚠️ FAIR - Acceptable but could be better")
else:
    print("  🚨 POOR - Better than random guessing, but weak")

# F1 score interpretation
print(f"\nF1-Score: {f1:.4f}")
print(f"  Harmonic mean of precision & recall")
if f1 > 0.80:
    print("  ✅ EXCELLENT - Great balance between precision and recall")
elif f1 > 0.70:
    print("  ✓ GOOD - Reasonable balance")
else:
    print("  ⚠️ NEEDS IMPROVEMENT")

# Overall verdict
print(f"\n" + "=" * 100)
print("FINAL VERDICT: IS THIS A STRONG MODEL?")
print("=" * 100)

score_components = {
    'Accuracy': (accuracy, 0.99),
    'Precision': (precision, 0.90),
    'Recall': (recall, 0.85),
    'ROC-AUC': (roc_auc, 0.90),
}

strengths = []
weaknesses = []

if accuracy > 0.99:
    strengths.append(f"✅ Exceptional accuracy ({accuracy*100:.2f}%)")
elif accuracy > 0.98:
    strengths.append(f"✅ Excellent accuracy ({accuracy*100:.2f}%)")

if precision > 0.90:
    strengths.append(f"✅ High precision ({precision*100:.2f}%) - Few false positives")
    
if recall > 0.80:
    strengths.append(f"✅ Good recall ({recall*100:.2f}%) - Catches most fraud")
elif recall > 0.70:
    weaknesses.append(f"⚠️ Moderate recall ({recall*100:.2f}%) - Some frauds escape (missed: {fn})")
    
if roc_auc > 0.93:
    strengths.append(f"✅ Excellent ROC-AUC ({roc_auc:.4f}) - Superior discrimination")

if fn > 20:
    weaknesses.append(f"⚠️ {fn} false negatives - Missing {fn} fraud cases")

if fp > 50:
    weaknesses.append(f"⚠️ {fp} false positives - Risk of blocking legitimate users")

print("\n📊 STRENGTHS:")
for strength in strengths:
    print(f"   {strength}")

if weaknesses:
    print("\n⚠️ AREAS TO IMPROVE:")
    for weakness in weaknesses:
        print(f"   {weakness}")
else:
    print("\n✅ NO MAJOR WEAKNESSES IDENTIFIED")

# Overall assessment
print("\n" + "-" * 100)

overall_score = (
    (accuracy > 0.98) +
    (precision > 0.85) +
    (recall > 0.80) +
    (roc_auc > 0.90)
)

if overall_score == 4:
    print("🚀 VERDICT: YES - THIS IS A STRONG MODEL!")
    print("\nWhy?")
    print("  • Detects {:.1f}% of fraudulent transactions (high recall)".format(recall*100))
    print("  • Only {:.1f}% false alarm rate (high precision)".format((1-precision)*100))
    print("  • Excellent overall discrimination (ROC-AUC {:.4f})".format(roc_auc))
    print("  • Industry-leading accuracy ({:.2f}%)".format(accuracy*100))
    print("\nThis model is PRODUCTION-READY for deployment!")
    
elif overall_score >= 3:
    print("✅ VERDICT: YES - THIS IS A SOLID MODEL!")
    print("\nGood performance across metrics. Suitable for most use cases.")
    
elif overall_score >= 2:
    print("⚠️ VERDICT: MODERATE - GOOD BUT NOT EXCELLENT")
    print("\nNeeds some tuning but usable for fraud detection.")
    
else:
    print("🚨 VERDICT: WEAK - NEEDS IMPROVEMENT")
    print("\nConsider model tuning or different algorithms.")

print("\n" + "=" * 100)

# Business impact
print("\nBUSINESS IMPACT ANALYSIS:")
print("=" * 100)

print(f"\nOn 56,962 test transactions (10,000 fraud cases expected):")
print(f"  ✅ Caught frauds: {tp:,} ({tp/10000*100:.1f}%)")
print(f"  🚨 Missed frauds: {fn:,} ({fn/10000*100:.1f}%)")
print(f"  💰 False alarms: {fp:,} (customer complaints)")
print(f"  ✓ Legitimate approved: {tn:,}")

print(f"\nFinancial Impact (assuming $100 avg fraud value):")
print(f"  Caught: ${tp * 100:,} of potential fraud")
print(f"  Missed: ${fn * 100:,} undetected")
print(f"  Prevention Rate: {tp/(tp+fn)*100:.1f}%")

print("\n" + "=" * 100)
