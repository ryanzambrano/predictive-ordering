"""
Time-Segmented Apriori Analysis for New Coffee Shop Dataset

Dataset: ylchang/coffee-shop-sample-data-1113
April 2019 Sales Data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os
from pathlib import Path

# Configuration
DATASET_PATH = Path.home() / ".cache/kagglehub/datasets/ylchang/coffee-shop-sample-data-1113/versions/1"
OUTPUT_DIR = Path("apriori_results_new")
MIN_SUPPORT = 0.02  # 2%
MIN_CONFIDENCE = 0.40  # 40%

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("TIME-SEGMENTED APRIORI ANALYSIS - NEW COFFEE SHOP DATASET")
print("="*80)
print()

# ============================================================================
# PHASE 1: DATA LOADING
# ============================================================================

print("Phase 1: Loading data...")
print("-"*80)

# Load sales receipts
sales_file = DATASET_PATH / "201904 sales reciepts.csv"
print(f"Loading: {sales_file}")
df_sales = pd.read_csv(sales_file)
print(f"✓ Loaded {len(df_sales):,} sales records")

# Load product information
product_file = DATASET_PATH / "product.csv"
print(f"Loading: {product_file}")
df_products = pd.read_csv(product_file)
print(f"✓ Loaded {len(df_products):,} products")

# Display product columns
print(f"\nProduct columns: {', '.join(df_products.columns.tolist())}")
print()

# Show sample products
print("Sample products:")
print(df_products.head(10))
print()

# Merge sales with product names
print("Merging sales data with product information...")
df = df_sales.merge(df_products[['product_id', 'product']], on='product_id', how='left')
print(f"✓ Merged successfully")
print()

# Check for any products without names
missing_products = df['product'].isna().sum()
if missing_products > 0:
    print(f"⚠️  Warning: {missing_products} records have missing product names")
else:
    print("✓ All products have names")
print()

# ============================================================================
# PHASE 2: DATE/TIME PROCESSING
# ============================================================================

print("Phase 2: Processing date and time...")
print("-"*80)

# Convert date and time
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_time'] = pd.to_timedelta(df['transaction_time'])

# Combine into datetime
df['transaction_datetime'] = df['transaction_date'] + df['transaction_time']

# Extract hour
df['hour'] = df['transaction_datetime'].dt.hour

print(f"✓ Date range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}")
print(f"✓ Time range: {df['transaction_datetime'].min().time()} to {df['transaction_datetime'].max().time()}")
print()

# ============================================================================
# PHASE 3: TIME SEGMENTATION
# ============================================================================

print("Phase 3: Creating time segments...")
print("-"*80)

# Create day-part segments
def get_day_part(hour):
    if 6 <= hour < 11:
        return 'Morning'
    elif 11 <= hour < 16:
        return 'Afternoon'
    else:
        return 'Evening'

df['day_part'] = df['hour'].apply(get_day_part)

# Create day-type segments
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

print("Phase 4: Creating transaction baskets...")
print("-"*80)

# Group by transaction_id to create baskets
print("Grouping items by transaction_id...")
transactions = df.groupby('transaction_id').agg({
    'product': lambda x: list(x),
    'time_segment': 'first',
    'transaction_datetime': 'first'
}).reset_index()

transactions.columns = ['transaction_id', 'items', 'time_segment', 'datetime']

print(f"✓ Created {len(transactions):,} unique transaction baskets")

# Calculate basket statistics
basket_sizes = transactions['items'].apply(len)
print(f"✓ Average items per basket: {basket_sizes.mean():.2f}")
print(f"✓ Max items in a basket: {basket_sizes.max()}")
print(f"✓ Single-item transactions: {(basket_sizes == 1).sum():,} ({(basket_sizes == 1).sum()/len(basket_sizes)*100:.1f}%)")
print(f"✓ Multi-item transactions: {(basket_sizes > 1).sum():,} ({(basket_sizes > 1).sum()/len(basket_sizes)*100:.1f}%)")
print()

# Show distribution by segment
print("Transaction distribution by segment:")
for segment in sorted(transactions['time_segment'].unique()):
    count = (transactions['time_segment'] == segment).sum()
    print(f"  - {segment}: {count:,} transactions")
print()

# Show sample baskets
print("Sample transaction baskets:")
for idx, row in transactions.head(5).iterrows():
    print(f"  Transaction {row['transaction_id']}: {row['items']}")
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

    # Filter out single-item transactions
    multi_item_transactions = [t for t in segment_transactions if len(t) > 1]

    print(f"Total transactions: {len(segment_transactions):,}")
    print(f"Multi-item transactions: {len(multi_item_transactions):,} ({len(multi_item_transactions)/len(segment_transactions)*100:.1f}%)")

    if len(multi_item_transactions) < 10:
        print(f"⚠️  Warning: Too few multi-item transactions to analyze")
        continue

    # Transform to binary matrix
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

        # Add segment info
        rules['time_segment'] = segment

        # Format antecedents and consequents
        rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

        # Show top 10 rules by confidence
        print(f"\nTop 10 rules by confidence:")
        top_rules = rules.nlargest(10, 'confidence')[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']]
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
# PHASE 6: EXPORT RESULTS
# ============================================================================

print("Phase 6: Exporting results...")
print("-"*80)

if len(all_rules) == 0:
    print("❌ No rules generated. Try lowering min_support or min_confidence.")
    exit(1)

# Combine all rules
combined_rules = pd.concat(all_rules, ignore_index=True)

print(f"✓ Total rules across all segments: {len(combined_rules)}")

# Select columns for export
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

# Rename columns
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

# Sort by confidence
export_rules = export_rules.sort_values(['Time_Segment', 'Confidence'], ascending=[True, False])

# Export to CSV
output_file = OUTPUT_DIR / "association_rules_by_segment.csv"
export_rules.to_csv(output_file, index=False)
print(f"✓ Saved all rules to: {output_file}")

# Export by segment
for segment in export_rules['Time_Segment'].unique():
    segment_rules = export_rules[export_rules['Time_Segment'] == segment]
    segment_file = OUTPUT_DIR / f"rules_{segment}.csv"
    segment_rules.to_csv(segment_file, index=False)
    print(f"✓ Saved {segment} rules to: {segment_file}")

print()

# ============================================================================
# PHASE 7: SUMMARY REPORT
# ============================================================================

print("Phase 7: Generating summary report...")
print("="*80)
print()

summary_lines = []

summary_lines.append("="*80)
summary_lines.append("ASSOCIATION RULE MINING SUMMARY - NEW COFFEE SHOP DATASET")
summary_lines.append("="*80)
summary_lines.append("")
summary_lines.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
summary_lines.append(f"Dataset: April 2019 Sales Data")
summary_lines.append("")

summary_lines.append("CONFIGURATION:")
summary_lines.append(f"  - Minimum Support: {MIN_SUPPORT*100}%")
summary_lines.append(f"  - Minimum Confidence: {MIN_CONFIDENCE*100}%")
summary_lines.append("")

summary_lines.append("DATASET OVERVIEW:")
summary_lines.append(f"  - Total sales records: {len(df_sales):,}")
summary_lines.append(f"  - Unique transactions: {len(transactions):,}")
summary_lines.append(f"  - Multi-item transactions: {(basket_sizes > 1).sum():,} ({(basket_sizes > 1).sum()/len(basket_sizes)*100:.1f}%)")
summary_lines.append(f"  - Unique products: {df['product'].nunique()}")
summary_lines.append(f"  - Date range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}")
summary_lines.append("")

summary_lines.append("RESULTS:")
summary_lines.append(f"  - Total association rules: {len(combined_rules):,}")
summary_lines.append(f"  - Average confidence: {combined_rules['confidence'].mean():.3f}")
summary_lines.append(f"  - Average lift: {combined_rules['lift'].mean():.3f}")
summary_lines.append(f"  - Segments analyzed: {combined_rules['time_segment'].nunique()}")
summary_lines.append("")

summary_lines.append("TOP 20 HIGHEST CONFIDENCE RULES:")
top_20 = export_rules.nlargest(20, 'Confidence')
for idx, (i, row) in enumerate(top_20.iterrows(), 1):
    summary_lines.append(f"\n{idx}. [{row['Time_Segment']}]")
    summary_lines.append(f"   {row['Antecedent_Items']} → {row['Consequent_Items']}")
    summary_lines.append(f"   Confidence: {row['Confidence']:.3f} | Support: {row['Support']:.3f} | Lift: {row['Lift']:.3f}")

summary_lines.append("")
summary_lines.append("="*80)

# Print and save
summary_text = "\n".join(summary_lines)
print(summary_text)

summary_file = OUTPUT_DIR / "analysis_summary.txt"
with open(summary_file, 'w') as f:
    f.write(summary_text)

print()
print(f"✓ Saved summary to: {summary_file}")
print()

print("="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print()
print(f"Results saved to: {OUTPUT_DIR}/")
print()
