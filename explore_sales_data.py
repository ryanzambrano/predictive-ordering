"""
Explore Sales Receipts Data
"""

import pandas as pd
import os

print("="*80)
print("EXPLORING SALES RECEIPTS DATA")
print("="*80)
print()

# Path to the dataset
dataset_path = "/Users/ryanzambrano/.cache/kagglehub/datasets/ylchang/coffee-shop-sample-data-1113/versions/1"
sales_file = os.path.join(dataset_path, "201904 sales reciepts.csv")

print(f"Loading: {sales_file}")
df = pd.read_csv(sales_file)
print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")
print()

# Display columns
print("COLUMNS:")
print("-"*80)
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")
print()

# Display first few rows
print("FIRST 10 ROWS:")
print("-"*80)
print(df.head(10))
print()

# Display data types
print("DATA TYPES:")
print("-"*80)
print(df.dtypes)
print()

# Display basic info
print("DATASET INFO:")
print("-"*80)
print(f"  Total rows: {len(df):,}")
print(f"  Total columns: {len(df.columns)}")
print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print()

# Check for null values
print("NULL VALUES:")
print("-"*80)
null_counts = df.isnull().sum()
for col, count in null_counts.items():
    if count > 0:
        print(f"  {col}: {count:,} ({count/len(df)*100:.1f}%)")
if null_counts.sum() == 0:
    print("  No null values found!")
print()

# Display unique value counts for key columns
print("UNIQUE VALUES:")
print("-"*80)
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"  {col}: {unique_count:,} unique values")
print()

# Look for transaction-related columns
print("SAMPLE VALUES FROM KEY COLUMNS:")
print("-"*80)

# Show sample values from first few columns
for col in df.columns[:5]:
    print(f"\n{col}:")
    print(df[col].head(10).tolist())

print()
print("="*80)
print("ANALYSIS QUESTIONS:")
print("="*80)
print()
print("To adapt the Apriori analysis, we need to identify:")
print("  1. Transaction ID column (groups items into baskets)")
print("  2. Product/Item column (what was purchased)")
print("  3. Date/Time columns (for time segmentation)")
print("  4. Quantity column (optional, how many of each item)")
print()

# Try to identify these automatically
print("AUTO-DETECTION:")
print("-"*80)

# Look for transaction ID
transaction_id_candidates = [col for col in df.columns if 'transaction' in col.lower() or 'receipt' in col.lower() or 'order' in col.lower()]
if transaction_id_candidates:
    print(f"✓ Potential Transaction ID: {transaction_id_candidates}")

# Look for product columns
product_candidates = [col for col in df.columns if 'product' in col.lower() or 'item' in col.lower()]
if product_candidates:
    print(f"✓ Potential Product columns: {product_candidates}")

# Look for date/time columns
datetime_candidates = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
if datetime_candidates:
    print(f"✓ Potential Date/Time columns: {datetime_candidates}")

# Look for quantity
quantity_candidates = [col for col in df.columns if 'quantity' in col.lower() or 'qty' in col.lower() or 'count' in col.lower()]
if quantity_candidates:
    print(f"✓ Potential Quantity columns: {quantity_candidates}")

print()
print("="*80)
