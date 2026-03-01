"""
Test fraud detection with REAL dataset patterns.
Based on analysis of 284,807 actual credit card transactions.
"""

print("=" * 100)
print("FRAUD DETECTION TEST - BASED ON REAL DATASET ANALYSIS")
print("=" * 100)

def calc_fraud(amount, hour, merchant_type):
    """Calculate fraud using real dataset patterns."""
    fraud_score = 0.15
    
    # Time
    if 0 <= hour < 6:
        fraud_score += 0.25
    elif 6 <= hour < 12:
        fraud_score += 0.10
    elif 12 <= hour < 18:
        fraud_score += 0.00
    elif 18 <= hour < 24:
        fraud_score += 0.05
    
    # Amount - CALIBRATED FOR REAL DATA
    if amount < 10:
        fraud_score += 0.08  # $0-10: 0.26% real fraud
    elif 10 <= amount < 25:
        fraud_score += 0.02  # $10-25: 0.05% real fraud
    elif 25 <= amount < 50:
        fraud_score += 0.03  # $25-50: 0.07% real fraud
    elif 50 <= amount < 100:
        fraud_score += 0.04  # $50-100: 0.15% real fraud
    elif 100 <= amount < 250:
        fraud_score += 0.05  # $100-250: 0.16% real fraud
    elif 250 <= amount < 500:
        fraud_score += 0.08  # $250-500: 0.29% real fraud
    elif 500 <= amount < 1000:
        fraud_score += 0.22  # $500-1000: 0.40% real fraud (SWEET SPOT!)
    elif 1000 <= amount < 2500:
        fraud_score += 0.18  # $1000-2500: 0.34% real fraud
    else:
        fraud_score += 0.00  # $2500+: 0.00% real fraud (never happens!)
    
    # Merchant
    if merchant_type == "Online Shopping":
        fraud_score += 0.12
    elif merchant_type == "Gas Station":
        fraud_score += 0.08
    elif merchant_type == "ATM":
        fraud_score += 0.10
    
    # Combo risks
    if 0 <= hour < 6:  # Night
        if amount < 10:
            fraud_score += 0.15  # Night + tiny amount
        elif 500 <= amount < 1000:
            fraud_score += 0.12  # Night + sweet spot
        if merchant_type == "ATM" and amount >= 50:
            fraud_score += 0.12  # ATM at night
    
    fraud_score = min(max(fraud_score, 0.0), 0.92)
    return fraud_score

# Test scenarios
tests = [
    ("Test 1", 50, 14, "Grocery", "Afternoon grocery shopping"),
    ("Test 2", 75, 3, "Gas Station", "Night gas station (SUSPICIOUS!)"),
    ("Test 3", 650, 2, "Online Shopping", "Midnight online - PERFECT FRAUD STORM!"),
    ("Test 4", 350, 10, "Hotel", "Morning hotel booking"),
    ("Test 5", 300, 4, "ATM", "Night ATM withdrawal - HIGH RISK!"),
]

print("\nScenario | Amount | Hour | Merchant | Pattern | Data Fraud % | Component")
print("-" * 100)

for test_name, amount, hour, merchant, desc in tests:
    fraud_pattern = calc_fraud(amount, hour, merchant)
    
    # Find amount range for reference
    if amount < 10:
        range_ref = "$0-10 (0.26%)"
    elif amount < 25:
        range_ref = "$10-25 (0.05%)"
    elif amount < 50:
        range_ref = "$25-50 (0.07%)"
    elif amount < 100:
        range_ref = "$50-100 (0.15%)"
    elif amount < 250:
        range_ref = "$100-250 (0.16%)"
    elif amount < 500:
        range_ref = "$250-500 (0.29%)"
    elif amount < 1000:
        range_ref = "$500-1K (0.40%) ⭐"
    elif amount < 2500:
        range_ref = "$1K-2.5K (0.34%)"
    else:
        range_ref = "$2.5K+ (0.00%)"
    
    print(f"{test_name:>8} | ${amount:>5} | {hour:>2}h | {merchant:<15} | {range_ref:>20}")
    print(f"         | Fraud: {fraud_pattern:>6.1%} | {desc}")
    
    # With blending 65% patterns + 35% model (assuming model ~18%)
    model_pred = 0.18
    final = (fraud_pattern * 0.65) + (model_pred * 0.35)
    
    if final >= 0.50:
        status = "🚨 FRAUD DETECTED"
    elif final >= 0.40:
        status = "⚠️ SUSPICIOUS"
    else:
        status = "✅ LEGITIMATE"
    
    print(f"         | Final: {final:>6.1%} (65% patterns + 35% model) → {status}")
    print()

print("=" * 100)
print("KEY INSIGHTS FROM REAL DATA:")
print("=" * 100)
print("""
1. MICRO AMOUNTS ($0-10): 0.26% fraud rate!
   - Fraudsters test with tiny amounts
   - Avoid false positives but watch carefully
   
2. SWEET SPOT ($500-1000): 0.40% fraud rate!
   - Highest real fraud concentration
   - This is where criminals strike
   
3. LARGE AMOUNTS ($2500+): 0.00% fraud rate!
   - Never fraudulent in entire dataset
   - Big purchases are almost always legitimate
   
4. NIGHT TIME ($0-6 AM): 3.3x more fraud!
   - Fraudsters operate when cardholders sleep
   - Combine night + $500-1K + online = MAXIMUM RISK
   
5. DATASET FACTS:
   - Max fraud amount ever: $2,125.87
   - Max legitimate amount: $25,691.16
   - Fraudsters never go above $2,125.87
""")

print("=" * 100)
