"""
Understanding Apriori Results - Interactive Explanation

This script helps you understand what the association rules mean and how to interpret them.
"""

import pandas as pd
from pathlib import Path

print("="*80)
print("UNDERSTANDING YOUR APRIORI RESULTS")
print("="*80)
print()

# ============================================================================
# PART 1: WHAT IS ASSOCIATION RULE MINING?
# ============================================================================

print("PART 1: What is Association Rule Mining?")
print("-"*80)
print()
print("Association rules find patterns like: 'When customers buy X, they also buy Y'")
print("Format: {Antecedent} → {Consequent}")
print("       (What they buy first) → (What they buy next)")
print()
print("Real example from your data:")
print("  'Ouro Brasileiro shot' → 'Ginger Scone'")
print("  This means: Customers who buy Ouro Brasileiro shot often buy Ginger Scone too")
print()
input("Press Enter to continue...")
print()

# ============================================================================
# PART 2: UNDERSTANDING THE METRICS
# ============================================================================

print("PART 2: Understanding the Key Metrics")
print("-"*80)
print()

print("📊 SUPPORT:")
print("  - What it means: How often this combination appears in ALL transactions")
print("  - Formula: (# of transactions with both items) / (total transactions)")
print("  - Example: Support = 0.028 (2.8%)")
print("    → Out of 100 transactions, about 3 have both items together")
print("  - Why it matters: Shows if the pattern is common enough to care about")
print()

print("📊 CONFIDENCE:")
print("  - What it means: How often Y is bought WHEN X is bought")
print("  - Formula: (# of transactions with both X and Y) / (# of transactions with X)")
print("  - Example: Confidence = 0.794 (79.4%)")
print("    → When someone buys Ouro Brasileiro shot, there's a 79% chance they buy Ginger Scone")
print("  - Why it matters: This is your prediction accuracy!")
print("  - Rule of thumb:")
print("    • 60%+ = Very reliable (strong predictor)")
print("    • 40-60% = Moderately reliable")
print("    • <40% = Weak predictor")
print()

print("📊 LIFT:")
print("  - What it means: How much more likely Y is bought when X is bought, compared to random")
print("  - Formula: Confidence / (Probability of Y appearing anywhere)")
print("  - Example: Lift = 8.709")
print("    → Ginger Scone is 8.7x MORE likely to be bought when customer has Ouro Brasileiro shot")
print("  - Why it matters: Shows if the relationship is due to the rule, not just popularity")
print("  - Rule of thumb:")
print("    • Lift > 1 = Positive correlation (good!)")
print("    • Lift = 1 = No correlation (random)")
print("    • Lift < 1 = Negative correlation (items bought separately)")
print()
input("Press Enter to continue...")
print()

# ============================================================================
# PART 3: YOUR ACTUAL RESULTS
# ============================================================================

print("PART 3: Your Actual Results")
print("-"*80)
print()

# Load the results
results_file = Path("apriori_results/association_rules_by_segment.csv")
if results_file.exists():
    df = pd.read_csv(results_file)

    print(f"Found {len(df)} association rules in your café data")
    print()

    for idx, row in df.iterrows():
        print(f"Rule #{idx + 1}: [{row['Time_Segment']}]")
        print(f"  {row['Antecedent_Items']} → {row['Consequent_Items']}")
        print()
        print(f"  📈 SUPPORT: {row['Support']:.1%}")
        print(f"     → This combination appears in {row['Support']:.1%} of all transactions")
        print()
        print(f"  ✅ CONFIDENCE: {row['Confidence']:.1%}")
        print(f"     → When someone buys {row['Antecedent_Items']},")
        print(f"        they buy {row['Consequent_Items']} {row['Confidence']:.1%} of the time")
        print()
        print(f"  🚀 LIFT: {row['Lift']:.2f}x")
        print(f"     → {row['Consequent_Items']} is {row['Lift']:.2f}x more likely to be purchased")
        print(f"        when customer has {row['Antecedent_Items']}")
        print()
        print("-"*80)
        print()
else:
    print("⚠️  Results file not found. Make sure you ran apriori_analysis.py first.")
    print()

input("Press Enter to continue...")
print()

# ============================================================================
# PART 4: PRACTICAL APPLICATION
# ============================================================================

print("PART 4: How to Use This for Inventory Management")
print("-"*80)
print()

print("🎯 SCENARIO: Customer orders Ouro Brasileiro shot")
print()
print("What the data tells you:")
print("  • Confidence = 79.4% (on weekday afternoons)")
print("  • This customer will VERY LIKELY also want a Ginger Scone")
print()
print("Action for café:")
print("  1. STOCKING: For every 10 Ouro Brasileiro shots in inventory,")
print("     stock 7-8 Ginger Scones (based on 70-80% confidence)")
print()
print("  2. PLACEMENT: Put Ginger Scones near the espresso bar")
print()
print("  3. TIMING: Pattern is strongest during:")
print("     - Afternoon Weekday (79.4% confidence)")
print("     - Morning Weekday (72.0% confidence)")
print()
print("  4. UPSELLING: Train baristas to suggest:")
print("     'Would you like a Ginger Scone with your Ouro Brasileiro shot?'")
print("     (This has a 70-80% success rate!)")
print()
print("  5. REDUCE SURPLUS: Don't overstock Ginger Scones during:")
print("     - Evening hours (no strong association found)")
print()

input("Press Enter to continue...")
print()

# ============================================================================
# PART 5: WHY ONLY 4 RULES?
# ============================================================================

print("PART 5: Why Did We Only Find 4 Rules?")
print("-"*80)
print()

print("Good question! Here's why:")
print()
print("1. HIGH CONFIDENCE THRESHOLD (40%):")
print("   - We only kept rules where Y happens 40%+ of the time when X is bought")
print("   - This ensures reliable predictions for inventory")
print()
print("2. SUPPORT THRESHOLD (2%):")
print("   - We only kept patterns that appear in at least 2% of transactions")
print("   - This filters out rare combinations that don't matter for inventory")
print()
print("3. SINGLE-ITEM TRANSACTIONS (75% of your data):")
print("   - Most customers buy only 1 item")
print("   - Association rules need multi-item baskets to find patterns")
print()
print("4. QUALITY OVER QUANTITY:")
print("   - Better to have 4 STRONG, ACTIONABLE rules than 100 weak ones")
print("   - Confidence of 70-79% is EXCELLENT for prediction")
print()
print("Want to find more rules?")
print("  • Lower min_confidence to 30% (but predictions become less reliable)")
print("  • Lower min_support to 1% (but patterns become less significant)")
print()

input("Press Enter to continue...")
print()

# ============================================================================
# PART 6: COMPARING TIME SEGMENTS
# ============================================================================

print("PART 6: Time Segment Comparison")
print("-"*80)
print()

if results_file.exists():
    print("How does the pattern change by time?")
    print()

    df_sorted = df.sort_values('Confidence', ascending=False)

    print("Ranking by Confidence (highest to lowest):")
    for idx, row in df_sorted.iterrows():
        print(f"  {idx+1}. {row['Time_Segment']:<20} {row['Confidence']:.1%} confidence")
    print()

    print("Insight:")
    print("  • BEST time for this pattern: Afternoon Weekday (79.4%)")
    print("  • Pattern exists ALL DAY on both weekdays and weekends")
    print("  • Evening hours: No patterns met our thresholds")
    print()
    print("Inventory Strategy:")
    print("  → Stock more Ginger Scones during morning and afternoon")
    print("  → Reduce Ginger Scone inventory for evening shifts")
    print()

print()
print("="*80)
print("SUMMARY: Your Data in Plain English")
print("="*80)
print()
print("✅ YES, time-segmented association rule mining works!")
print()
print("Key Finding:")
print("  When a customer orders 'Ouro Brasileiro shot', they will buy")
print("  'Ginger Scone' about 70-80% of the time, depending on the time of day.")
print()
print("This is VERY STRONG evidence that you should:")
print("  1. Always stock these items together")
print("  2. Maintain a 7:10 or 8:10 ratio (Scones:Shots)")
print("  3. Focus stocking during morning and afternoon")
print("  4. Train staff to suggest this combination")
print()
print("This kind of insight can directly reduce food waste and optimize inventory!")
print()
print("="*80)
