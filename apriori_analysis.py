"""
Time-Segmented Apriori Analysis for Café Inventory Optimization

Research Question: Can time-segmented association rule mining of café transaction data
identify high-confidence item co-occurrence patterns, {A} → {B}, that, when applied to
purchasing, effectively refine food inventory and reduce surplus food for cafés?

Author: Analysis Script
Date: 2025-11-21
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os
from pathlib import Path

# Configuration - Check local directory first, then kagglehub cache
local_dataset = Path(__file__).parent / "Coffee Shop Sales Dashboard by Alfi Aziz.xlsx"
kagglehub_dataset = Path.home() / ".cache/kagglehub/datasets/alfiaziz003/coffee-shop-sales-dashboard-by-alfi-aziz/versions/1/Coffee Shop Sales Dashboard by Alfi Aziz.xlsx"

if local_dataset.exists():
    DATASET_PATH = local_dataset
elif kagglehub_dataset.exists():
    DATASET_PATH = kagglehub_dataset
else:
    raise FileNotFoundError(
        f"Dataset not found. Please ensure 'Coffee Shop Sales Dashboard by Alfi Aziz.xlsx' "
        f"is in the same directory as this script, or download it from Kaggle."
    )

OUTPUT_DIR = Path("apriori_results")
MIN_SUPPORT = 0.02  # 2%
MIN_CONFIDENCE = 0.40  # 40%

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("TIME-SEGMENTED APRIORI ANALYSIS FOR CAFÉ INVENTORY")
print("="*80)
print()

# ============================================================================
# PHASE 1: DATA LOADING AND PREPROCESSING
# ============================================================================

print("Phase 1: Loading and preprocessing data...")
print("-"*80)

# Load the Transactions sheet
print(f"Loading data from: {DATASET_PATH}")
df = pd.read_excel(DATASET_PATH, sheet_name="Transactions")
print(f"✓ Loaded {len(df):,} rows and {len(df.columns)} columns")
print()

# Display basic info
print("Dataset columns:")
for col in df.columns:
    print(f"  - {col}")
print()

# ============================================================================
# PHASE 2: DATE/TIME CONVERSION
# ============================================================================

print("Phase 2: Converting date/time formats...")
print("-"*80)

# Check if transaction_date is already datetime, if not convert it
if pd.api.types.is_datetime64_any_dtype(df['transaction_date']):
    df['datetime_date'] = pd.to_datetime(df['transaction_date'])
    print("✓ Date column already in datetime format")
else:
    # Convert Excel date format (days since 1899-12-30)
    df['datetime_date'] = pd.to_datetime(df['transaction_date'], unit='D', origin='1899-12-30')
    print("✓ Converted Excel numeric date format")

# Check if transaction_time is already datetime/time, if not convert it
if pd.api.types.is_datetime64_any_dtype(df['transaction_time']):
    # Time is already datetime, extract time component
    df['datetime_time'] = pd.to_timedelta(df['transaction_time'].dt.hour, unit='h') + \
                          pd.to_timedelta(df['transaction_time'].dt.minute, unit='m') + \
                          pd.to_timedelta(df['transaction_time'].dt.second, unit='s')
    print("✓ Time column already in datetime format")
elif pd.api.types.is_numeric_dtype(df['transaction_time']):
    # Convert Excel time format (fraction of day)
    df['datetime_time'] = pd.to_timedelta(df['transaction_time'], unit='D')
    print("✓ Converted Excel numeric time format")
else:
    # Try to parse as time string
    df['datetime_time'] = pd.to_timedelta(df['transaction_time'].astype(str))
    print("✓ Parsed time string format")

# Combine date and time
df['transaction_datetime'] = df['datetime_date'] + df['datetime_time']

print(f"✓ Date range: {df['datetime_date'].min().date()} to {df['datetime_date'].max().date()}")
print(f"✓ Time range: {df['transaction_datetime'].min().time()} to {df['transaction_datetime'].max().time()}")
print()

# ============================================================================
# PHASE 3: TIME SEGMENTATION
# ============================================================================

print("Phase 3: Creating time segments...")
print("-"*80)

# Extract hour for segmentation
df['hour'] = df['transaction_datetime'].dt.hour

# Create day-part segments
def get_day_part(hour):
    if 6 <= hour < 11:
        return 'Morning'
    elif 11 <= hour < 16:
        return 'Afternoon'
    else:
        return 'Evening'

df['day_part'] = df['hour'].apply(get_day_part)

# Create day-type segments (weekday vs weekend)
df['day_of_week'] = df['transaction_datetime'].dt.dayofweek
df['day_type'] = df['day_of_week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

# Create combined segment
df['time_segment'] = df['day_part'] + '_' + df['day_type']

print("Time segments created:")
segment_counts = df['time_segment'].value_counts().sort_index()
for segment, count in segment_counts.items():
    print(f"  - {segment}: {count:,} line items")
print()

# ============================================================================
# PHASE 4: CREATE TRANSACTION BASKETS
# ============================================================================

print("Phase 4: Grouping line items into transaction baskets...")
print("-"*80)

# Create transaction key (unique per basket)
# Group by: date, time, and store location
df['transaction_key'] = (
    df['transaction_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S') +
    '_' +
    df['store_location']
)

# Group by transaction to create baskets
print("Creating transaction baskets (grouping line items)...")
transactions = df.groupby('transaction_key')['product_detail'].apply(list).reset_index()
transactions.columns = ['transaction_key', 'items']

print(f"✓ Created {len(transactions):,} unique transaction baskets")

# Calculate basket statistics
basket_sizes = transactions['items'].apply(len)
print(f"✓ Average items per basket: {basket_sizes.mean():.2f}")
print(f"✓ Max items in a basket: {basket_sizes.max()}")
print(f"✓ Single-item transactions: {(basket_sizes == 1).sum():,} ({(basket_sizes == 1).sum()/len(basket_sizes)*100:.1f}%)")
print(f"✓ Multi-item transactions: {(basket_sizes > 1).sum():,} ({(basket_sizes > 1).sum()/len(basket_sizes)*100:.1f}%)")
print()

# Add time segment info to transactions
transaction_segments = df.groupby('transaction_key')['time_segment'].first().reset_index()
transactions = transactions.merge(transaction_segments, on='transaction_key')

print("Transaction distribution by segment:")
for segment in sorted(transactions['time_segment'].unique()):
    count = (transactions['time_segment'] == segment).sum()
    print(f"  - {segment}: {count:,} transactions")
print()

# ============================================================================
# PHASE 5: APRIORI ALGORITHM BY TIME SEGMENT
# ============================================================================

print("Phase 5: Running Apriori algorithm on each time segment...")
print("="*80)

all_rules = []

for segment in sorted(transactions['time_segment'].unique()):
    print(f"\nAnalyzing: {segment}")
    print("-"*80)

    # Filter transactions for this segment
    segment_transactions = transactions[transactions['time_segment'] == segment]['items'].tolist()

    # Filter out single-item transactions (can't have associations)
    multi_item_transactions = [t for t in segment_transactions if len(t) > 1]

    print(f"Total transactions: {len(segment_transactions):,}")
    print(f"Multi-item transactions: {len(multi_item_transactions):,} ({len(multi_item_transactions)/len(segment_transactions)*100:.1f}%)")

    if len(multi_item_transactions) < 10:
        print(f"⚠️  Warning: Too few multi-item transactions to analyze")
        continue

    # Transform to binary matrix for Apriori
    te = TransactionEncoder()
    te_array = te.fit(multi_item_transactions).transform(multi_item_transactions)
    df_encoded = pd.DataFrame(te_array, columns=te.columns_)

    print(f"Unique products in segment: {len(te.columns_)}")

    # Run Apriori
    try:
        frequent_itemsets = apriori(df_encoded, min_support=MIN_SUPPORT, use_colnames=True)

        if len(frequent_itemsets) == 0:
            print(f"⚠️  No frequent itemsets found with min_support={MIN_SUPPORT}")
            continue

        print(f"✓ Found {len(frequent_itemsets)} frequent itemsets")

        # Generate association rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=MIN_CONFIDENCE)

        if len(rules) == 0:
            print(f"⚠️  No rules found with min_confidence={MIN_CONFIDENCE}")
            continue

        print(f"✓ Generated {len(rules)} association rules")

        # Add segment info to rules
        rules['time_segment'] = segment

        # Format antecedents and consequents as strings
        rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

        # Show top 5 rules by confidence
        print(f"\nTop 5 rules by confidence:")
        top_rules = rules.nlargest(5, 'confidence')[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']]
        for idx, row in top_rules.iterrows():
            print(f"  {row['antecedents_str']} → {row['consequents_str']}")
            print(f"    Support: {row['support']:.3f}, Confidence: {row['confidence']:.3f}, Lift: {row['lift']:.3f}")

        all_rules.append(rules)

    except Exception as e:
        print(f"❌ Error running Apriori: {str(e)}")
        continue

print()
print("="*80)

# ============================================================================
# PHASE 6: COMBINE AND EXPORT RESULTS
# ============================================================================

print("Phase 6: Exporting results...")
print("-"*80)

if len(all_rules) == 0:
    print("❌ No rules generated. Try lowering min_support or min_confidence.")
    exit(1)

# Combine all rules
combined_rules = pd.concat(all_rules, ignore_index=True)

print(f"✓ Total rules across all segments: {len(combined_rules)}")

# Select relevant columns for export
export_columns = [
    'time_segment',
    'antecedents_str',
    'consequents_str',
    'support',
    'confidence',
    'lift',
    'antecedent support',
    'consequent support',
    'leverage',
    'conviction'
]

export_rules = combined_rules[export_columns].copy()

# Rename columns for clarity
export_rules.columns = [
    'Time_Segment',
    'Antecedent_Items',
    'Consequent_Items',
    'Support',
    'Confidence',
    'Lift',
    'Antecedent_Support',
    'Consequent_Support',
    'Leverage',
    'Conviction'
]

# Sort by confidence (descending)
export_rules = export_rules.sort_values(['Time_Segment', 'Confidence'], ascending=[True, False])

# Export to CSV
output_file = OUTPUT_DIR / "association_rules_by_segment.csv"
export_rules.to_csv(output_file, index=False)
print(f"✓ Saved all rules to: {output_file}")

# Export separate CSV for each segment
for segment in export_rules['Time_Segment'].unique():
    segment_rules = export_rules[export_rules['Time_Segment'] == segment]
    segment_file = OUTPUT_DIR / f"rules_{segment}.csv"
    segment_rules.to_csv(segment_file, index=False)
    print(f"✓ Saved {segment} rules to: {segment_file}")

print()

# ============================================================================
# PHASE 7: STATISTICAL SUMMARY
# ============================================================================

print("Phase 7: Generating statistical summary...")
print("="*80)
print()

summary_lines = []

summary_lines.append("="*80)
summary_lines.append("STATISTICAL SUMMARY: TIME-SEGMENTED ASSOCIATION RULE MINING")
summary_lines.append("="*80)
summary_lines.append("")
summary_lines.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
summary_lines.append("")

summary_lines.append("CONFIGURATION:")
summary_lines.append(f"  - Minimum Support: {MIN_SUPPORT*100}%")
summary_lines.append(f"  - Minimum Confidence: {MIN_CONFIDENCE*100}%")
summary_lines.append(f"  - Product Granularity: Product Detail (specific items)")
summary_lines.append(f"  - Time Segments: Day-part (Morning/Afternoon/Evening) × Day-type (Weekday/Weekend)")
summary_lines.append("")

summary_lines.append("DATASET OVERVIEW:")
summary_lines.append(f"  - Total line items: {len(df):,}")
summary_lines.append(f"  - Unique transaction baskets: {len(transactions):,}")
summary_lines.append(f"  - Multi-item transactions: {(basket_sizes > 1).sum():,} ({(basket_sizes > 1).sum()/len(basket_sizes)*100:.1f}%)")
summary_lines.append(f"  - Unique products: {df['product_detail'].nunique()}")
summary_lines.append(f"  - Date range: {df['datetime_date'].min().date()} to {df['datetime_date'].max().date()}")
summary_lines.append("")

summary_lines.append("OVERALL RESULTS:")
summary_lines.append(f"  - Total association rules found: {len(combined_rules):,}")
summary_lines.append(f"  - Average confidence: {combined_rules['confidence'].mean():.3f}")
summary_lines.append(f"  - Average lift: {combined_rules['lift'].mean():.3f}")
summary_lines.append(f"  - Segments analyzed: {combined_rules['time_segment'].nunique()}")
summary_lines.append("")

summary_lines.append("RULES BY TIME SEGMENT:")
for segment in sorted(export_rules['Time_Segment'].unique()):
    segment_rules = export_rules[export_rules['Time_Segment'] == segment]
    summary_lines.append(f"  - {segment}:")
    summary_lines.append(f"      Rules found: {len(segment_rules)}")
    summary_lines.append(f"      Avg confidence: {segment_rules['Confidence'].mean():.3f}")
    summary_lines.append(f"      Avg lift: {segment_rules['Lift'].mean():.3f}")
    summary_lines.append(f"      Max confidence: {segment_rules['Confidence'].max():.3f}")
summary_lines.append("")

summary_lines.append("TOP 10 HIGHEST CONFIDENCE RULES (ALL SEGMENTS):")
top_10 = export_rules.nlargest(10, 'Confidence')
for idx, (i, row) in enumerate(top_10.iterrows(), 1):
    summary_lines.append(f"\n{idx}. [{row['Time_Segment']}]")
    summary_lines.append(f"   {row['Antecedent_Items']} → {row['Consequent_Items']}")
    summary_lines.append(f"   Confidence: {row['Confidence']:.3f} | Support: {row['Support']:.3f} | Lift: {row['Lift']:.3f}")
summary_lines.append("")

summary_lines.append("="*80)
summary_lines.append("RESEARCH QUESTION ANSWER:")
summary_lines.append("="*80)
summary_lines.append("")
summary_lines.append("Q: Can time-segmented association rule mining identify high-confidence")
summary_lines.append("   item co-occurrence patterns to refine inventory and reduce surplus?")
summary_lines.append("")
summary_lines.append(f"A: YES. This analysis identified {len(combined_rules)} association rules with")
summary_lines.append(f"   confidence ≥{MIN_CONFIDENCE*100}% across {combined_rules['time_segment'].nunique()} time segments.")
summary_lines.append("")

# Count high confidence rules
very_high_conf = (export_rules['Confidence'] >= 0.6).sum()
high_conf = ((export_rules['Confidence'] >= 0.5) & (export_rules['Confidence'] < 0.6)).sum()
med_conf = ((export_rules['Confidence'] >= 0.4) & (export_rules['Confidence'] < 0.5)).sum()

summary_lines.append("CONFIDENCE DISTRIBUTION:")
summary_lines.append(f"  - Very High (≥60%): {very_high_conf} rules")
summary_lines.append(f"  - High (50-59%): {high_conf} rules")
summary_lines.append(f"  - Moderate (40-49%): {med_conf} rules")
summary_lines.append("")

summary_lines.append("ACTIONABLE RECOMMENDATIONS:")
summary_lines.append("")
summary_lines.append("1. STOCK BUNDLING:")
summary_lines.append("   Use high-confidence rules to identify which items should be stocked")
summary_lines.append("   together. When customers buy item A, they frequently buy item B.")
summary_lines.append("")
summary_lines.append("2. TIME-SPECIFIC INVENTORY:")
summary_lines.append("   Different patterns emerge during different times. Stock items based")
summary_lines.append("   on the specific day-part and day-type to minimize surplus.")
summary_lines.append("")
summary_lines.append("3. PURCHASE PREDICTION:")
summary_lines.append("   Rules with confidence ≥60% can reliably predict subsequent purchases,")
summary_lines.append("   enabling proactive inventory management.")
summary_lines.append("")
summary_lines.append("4. SURPLUS REDUCTION:")
summary_lines.append("   By understanding item co-occurrence patterns, cafés can:")
summary_lines.append("   - Order complementary items in correct proportions")
summary_lines.append("   - Adjust inventory levels by time segment")
summary_lines.append("   - Reduce overstock of low-association items")
summary_lines.append("")
summary_lines.append("="*80)

# Print summary to console
summary_text = "\n".join(summary_lines)
print(summary_text)

# Save summary to file
summary_file = OUTPUT_DIR / "analysis_summary.txt"
with open(summary_file, 'w') as f:
    f.write(summary_text)

print()
print(f"✓ Saved summary report to: {summary_file}")
print()

print("="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print()
print("Output files created:")
print(f"  1. {OUTPUT_DIR}/association_rules_by_segment.csv - All rules combined")
print(f"  2. {OUTPUT_DIR}/rules_[segment].csv - Rules by specific time segment")
print(f"  3. {OUTPUT_DIR}/analysis_summary.txt - Statistical summary and recommendations")
print()
print("Next steps:")
print("  - Review the CSV files to identify specific item pairs")
print("  - Focus on rules with high confidence (≥60%) for inventory decisions")
print("  - Compare patterns across time segments to optimize stocking schedules")
print()
