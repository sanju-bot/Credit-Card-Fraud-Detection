"""
Data-driven fraud risk calculator based on real-world patterns from the dataset.
Rules:
- 40-49%: SUSPICIOUS (needs verification)
- 50%+: FRAUD (high confidence)
"""

def calculate_fraud_probability(amount, hour, features=None):
    """
    Calculate fraud probability based on real-world patterns from analysis.
    
    Real Data Insights:
    - Night (0-6): 0.45% fraud rate (3.3x baseline)
    - Morning (6-12): 0.26% fraud rate (1.8x baseline)
    - Afternoon (12-18): 0.15% fraud rate (baseline)
    - Evening (18-24): 0.13% fraud rate (0.9x baseline)
    
    Amount patterns:
    - $0-50: 0.16% fraud (small amounts suspicious)
    - $50-500: 0.15-0.20% fraud
    - $500-1000: 0.40% fraud (2.5x increase!)
    - $1000-5000: 0.30% fraud
    
    Median fraud amount: $9.25 (fraudsters love small amounts)
    Mean fraud amount: $122
    """
    
    # BASE SCORE: 0.15 (represents baseline ~0.17% fraud rate scaling to 15%)
    fraud_score = 0.15
    
    # TIME-BASED RISK (normalized from actual percentages)
    # Night (0-6): 0.45% / 100% average = HIGH RISK bonus
    if 0 <= hour < 6:
        fraud_score += 0.25  # Night is highest risk
    # Morning (6-12): 0.26% fraud rate
    elif 6 <= hour < 12:
        fraud_score += 0.10  # Morning moderate risk
    # Afternoon (12-18): 0.15% fraud rate (baseline, no bonus)
    elif 12 <= hour < 18:
        fraud_score += 0.00  # Afternoon is safe
    # Evening (18-24): 0.13% fraud rate
    elif 18 <= hour < 24:
        fraud_score += 0.05  # Evening slight risk
    
    # AMOUNT-BASED RISK (real patterns from data)
    # Key insight: $500-1000 range has 0.40% fraud (2.5x higher)
    if 500 <= amount < 1000:
        fraud_score += 0.20  # Sweet spot for fraud
    # $1000-5000: 0.30% fraud rate
    elif 1000 <= amount < 5000:
        fraud_score += 0.18
    # $0-50: Very common frauds with small amounts
    elif 0 <= amount < 50:
        fraud_score += 0.08  # Small amounts more suspicious
    # $50-100: Low risk
    elif 50 <= amount < 100:
        fraud_score += 0.04
    # $100-500: Low-medium risk
    elif 100 <= amount < 500:
        fraud_score += 0.06
    # Large amounts (rarely fraudulent in data)
    elif amount >= 5000:
        fraud_score += 0.02
    
    # CLASSIFICATION TIER
    # Combine amount and time: late night + specific amount = higher risk
    if 0 <= hour < 6:  # Night hours
        if 500 <= amount < 1000:
            fraud_score += 0.15  # High risk combo
        elif amount < 100:
            fraud_score += 0.10  # Small night purchases suspicious
    
    # Ensure score stays in valid range
    fraud_score = min(max(fraud_score, 0.0), 0.95)
    
    return fraud_score


# Test scenarios with real-world examples
print("=" * 80)
print("DATA-DRIVEN FRAUD PROBABILITY CALCULATOR - TEST SCENARIOS")
print("=" * 80)

test_cases = [
    # (amount, hour, description)
    (25, 8, "$25 grocery morning"),           # Low risk
    (45, 5, "$45 gas station 5am"),          # Suspicious (night, small)
    (75, 12, "$75 lunch afternoon"),         # Safe
    (150, 20, "$150 online evening"),        # Low-medium
    (500, 3, "$500 ATM withdrawal night"),   # SUSPICIOUS
    (750, 2, "$750 transfer midnight"),      # SUSPICIOUS -> FRAUD
    (1200, 6, "$1200 airline morning"),      # SUSPICIOUS
    (1500, 19, "$1500 hotel evening"),       # Medium risk
    (2500, 4, "$2500 hardware night"),       # HIGH RISK
    (5000, 15, "$5000 jewelry afternoon"),   # Low risk
    (8000, 10, "$8000 transfer morning"),    # Low risk
    (15000, 2, "$15000 online midnight"),    # FRAUD (rare, high amount at night)
]

print("\nAmount | Time | Description              | Fraud % | Risk Level")
print("---" * 27)

for amount, hour, desc in test_cases:
    prob = calculate_fraud_probability(amount, hour)
    percent = prob * 100
    
    if percent >= 50:
        risk = "🚨 FRAUD"
    elif percent >= 40:
        risk = "⚠️  SUSPICIOUS"
    elif percent >= 25:
        risk = "⚠️  MEDIUM"
    elif percent >= 15:
        risk = "✓ LOW"
    else:
        risk = "✓ SAFE"
    
    print(f"${amount:>6} | {hour:>2}h | {desc:<24} | {percent:>6.1f}% | {risk}")

print("\n" + "=" * 80)
print("THRESHOLD RULES (Based on Real Data)")
print("=" * 80)
print("\n0-39%:    SAFE - Legitimate transaction")
print("40-49%:   ⚠️  SUSPICIOUS - Requires verification")
print("50%+:     🚨 FRAUD - High confidence fraud alert")
print("\n" + "=" * 80)
