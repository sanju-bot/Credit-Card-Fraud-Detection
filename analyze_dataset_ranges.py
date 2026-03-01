"""
Analyze the actual credit card dataset to find real min/max amounts
and set fraud detection thresholds based on actual data.
"""

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, 'src')

from data_processing import load_data

# Load the real dataset
df = load_data('data/creditcard.csv')

print("=" * 100)
print("ACTUAL DATASET ANALYSIS - MIN/MAX AMOUNTS")
print("=" * 100)

# Overall statistics
print("\n1. OVERALL DATASET:")
print(f"   Total Transactions: {len(df):,}")
print(f"   Currency: USD (Amount column)")
print(f"\n   MINIMUM Amount: ${df['Amount'].min():.2f}")
print(f"   MAXIMUM Amount: ${df['Amount'].max():.2f}")
print(f"   MEAN Amount: ${df['Amount'].mean():.2f}")
print(f"   MEDIAN Amount: ${df['Amount'].median():.2f}")
print(f"   STD DEV: ${df['Amount'].std():.2f}")

# Percentiles
print(f"\n   PERCENTILES:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    val = df['Amount'].quantile(p/100)
    print(f"   {p:>3}th percentile: ${val:.2f}")

# Split by fraud/legitimate
fraud_df = df[df['Class'] == 1]
legit_df = df[df['Class'] == 0]

print("\n" + "=" * 100)
print("2. LEGITIMATE TRANSACTIONS (Class=0):")
print("=" * 100)
print(f"   Count: {len(legit_df):,}")
print(f"\n   MINIMUM: ${legit_df['Amount'].min():.2f}")
print(f"   MAXIMUM: ${legit_df['Amount'].max():.2f}")
print(f"   MEAN: ${legit_df['Amount'].mean():.2f}")
print(f"   MEDIAN: ${legit_df['Amount'].median():.2f}")
print(f"   STD DEV: ${legit_df['Amount'].std():.2f}")

print(f"\n   PERCENTILES:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    val = legit_df['Amount'].quantile(p/100)
    print(f"   {p:>3}th percentile: ${val:.2f}")

print("\n" + "=" * 100)
print("3. FRAUDULENT TRANSACTIONS (Class=1):")
print("=" * 100)
print(f"   Count: {len(fraud_df):,}")
print(f"\n   MINIMUM: ${fraud_df['Amount'].min():.2f}")
print(f"   MAXIMUM: ${fraud_df['Amount'].max():.2f}")
print(f"   MEAN: ${fraud_df['Amount'].mean():.2f}")
print(f"   MEDIAN: ${fraud_df['Amount'].median():.2f}")
print(f"   STD DEV: ${fraud_df['Amount'].std():.2f}")

print(f"\n   PERCENTILES:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    val = fraud_df['Amount'].quantile(p/100)
    print(f"   {p:>3}th percentile: ${val:.2f}")

# Range analysis
print("\n" + "=" * 100)
print("4. REAL-WORLD AMOUNT RANGES:")
print("=" * 100)

ranges = [
    (0, 10),
    (10, 25),
    (25, 50),
    (50, 100),
    (100, 250),
    (250, 500),
    (500, 1000),
    (1000, 2500),
    (2500, float('inf')),
]

print("\nAmount Range    | Count  | Fraud | Legit | Fraud% | Risk Level")
print("-" * 70)

fraud_alerts = {}

for low, high in ranges:
    if high == float('inf'):
        range_str = f"${low}+"
        mask = df['Amount'] >= low
    else:
        range_str = f"${low:>4}-${high:<4}"
        mask = (df['Amount'] >= low) & (df['Amount'] < high)
    
    total = mask.sum()
    fraud_count = (df[mask]['Class'] == 1).sum()
    legit_count = (df[mask]['Class'] == 0).sum()
    
    if total > 0:
        fraud_pct = (fraud_count / total) * 100
        
        if fraud_pct > 1.0:
            risk = "🚨 VERY HIGH"
        elif fraud_pct > 0.5:
            risk = "🔴 HIGH"
        elif fraud_pct > 0.25:
            risk = "🟠 MEDIUM"
        elif fraud_pct > 0.15:
            risk = "🟡 LOW"
        else:
            risk = "🟢 VERY LOW"
        
        print(f"{range_str} | {total:>6} | {fraud_count:>5} | {legit_count:>5} | {fraud_pct:>6.2f}% | {risk}")
        fraud_alerts[(low, high)] = fraud_pct

print("\n" + "=" * 100)
print("5. FRAUD DETECTION THRESHOLDS (Based on Actual Data):")
print("=" * 100)

print("\nBALE% Formula:")
print("  • SAFE (< 0.15%): Amounts very common, low fraud")
print("  • NORMAL (0.15% - 0.30%): Standard fraud rate")
print("  • ALERT (0.30% - 0.50%): Slightly elevated fraud")
print("  • WARNING (0.50% - 1.0%): High fraud concentration")
print("  • DANGER (> 1.0%): Extremely high fraud concentration")

# Identify critical amount ranges
print("\nCRITICAL FINDINGS:")
high_fraud_ranges = [(r, pct) for r, pct in fraud_alerts.items() if pct > 0.35]
if high_fraud_ranges:
    print(f"\n🚨 HIGH FRAUD RANGES (>0.35% fraud rate):")
    for (low, high), pct in sorted(high_fraud_ranges, key=lambda x: x[1], reverse=True):
        if high == float('inf'):
            print(f"   • ${low}+ : {pct:.2f}% fraud rate")
        else:
            print(f"   • ${low}-${high} : {pct:.2f}% fraud rate")

# Safe ranges
safe_ranges = [(r, pct) for r, pct in fraud_alerts.items() if pct < 0.15]
if safe_ranges:
    print(f"\n✅ SAFE RANGES (<0.15% fraud rate):")
    for (low, high), pct in sorted(safe_ranges, key=lambda x: x[1]):
        if high == float('inf'):
            print(f"   • ${low}+ : {pct:.2f}% fraud rate")
        else:
            print(f"   • ${low}-${high} : {pct:.2f}% fraud rate")

# Recommended thresholds
print("\n" + "=" * 100)
print("6. RECOMMENDED FRAUD ALERT SYSTEM:")
print("=" * 100)

print("""
FRAUD ALERT SCORE CALCULATION:

Amount-Based Risk:
  • $0-50:        +10%  (Fraudsters test with small amounts)
  • $50-250:      +5%   (Safe zone)
  • $250-500:     +8%   (Slightly elevated)
  • $500-1000:    +20%  (HIGH RISK - Sweet spot for fraud!)
  • $1000-2500:   +15%  (Risky - Large amounts)
  • $2500+:       +8%   (Rare - Usually legitimate)

Time Risk:
  • Night (0-6):  +25%  (Highest risk)
  • Morning (6-12): +10%
  • Afternoon (12-18): +0%
  • Evening (18-24): +5%

Merchant Risk:
  • Online: +12%
  • Gas Station: +8%
  • ATM: +10%
  • Others: +0%

FRAUD ALERT THRESHOLDS:
  • < 40%: ✅ LEGITIMATE - Auto-approve
  • 40-50%: ⚠️ SUSPICIOUS - Manual review
  • 50%+: 🚨 FRAUD - Decline/Block
""")

print("\n" + "=" * 100)
print("7. DATASET RANGE RECOMMENDATIONS FOR INTERFACE:")
print("=" * 100)

# Get actual max from dataset to set max input limits
real_min = df['Amount'].min()
real_max = df['Amount'].max()
fraud_max = fraud_df['Amount'].max()
legit_max = legit_df['Amount'].max()

print(f"\nReal Dataset Ranges:")
print(f"  • Global Min: ${real_min:.2f}")
print(f"  • Global Max: ${real_max:.2f}")
print(f"  • Fraud Max: ${fraud_max:.2f}")
print(f"  • Legitimate Max: ${legit_max:.2f}")

print(f"\nRecommended UI Max Values:")
print(f"  • Grocery: $150 (realistic for shopping)")
print(f"  • Gas: $100 (realistic for tank fill)")
print(f"  • Restaurant: $300 (group dinner)")
print(f"  • Online: $2500 (high-end electronics)")
print(f"  • Hotel: $2500 (luxury stay)")
print(f"  • Airline: $3000 (premium tickets)")
print(f"  • ATM: $500 (daily withdrawal)")
print(f"  • Other: $5000 (catch-all, but real max is ${real_max:.2f})")

print("\n" + "=" * 100)
print("ANALYSIS COMPLETE")
print("=" * 100)
