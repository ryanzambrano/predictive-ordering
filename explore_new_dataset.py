"""
Explore New Coffee Shop Dataset from Kaggle

Dataset: ylchang/coffee-shop-sample-data-1113
"""

import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd

print("="*80)
print("EXPLORING NEW COFFEE SHOP DATASET")
print("="*80)
print()

print("Step 1: Downloading dataset from Kaggle...")
print("-"*80)

# Download the dataset
path = kagglehub.dataset_download("ylchang/coffee-shop-sample-data-1113")
print(f"✓ Dataset downloaded to: {path}")
print()

# List files in the dataset
import os
files = os.listdir(path)
print(f"Files in dataset:")
for f in files:
    file_path = os.path.join(path, f)
    size = os.path.getsize(file_path)
    print(f"  - {f} ({size:,} bytes)")
print()

# Try to load each file
print("Step 2: Loading and examining files...")
print("-"*80)
print()

for file in files:
    file_path = os.path.join(path, file)

    print(f"\n{'='*80}")
    print(f"FILE: {file}")
    print('='*80)

    try:
        # Try to load based on file extension
        if file.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.endswith('.xlsx') or file.endswith('.xls'):
            df = pd.read_excel(file_path)
        elif file.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            print(f"⚠️  Unknown file format, skipping...")
            continue

        print(f"\n✓ Loaded successfully!")
        print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print()

        print("Column names and types:")
        for col in df.columns:
            dtype = df[col].dtype
            non_null = df[col].notna().sum()
            print(f"  - {col:<30} {dtype:<15} ({non_null:,} non-null)")
        print()

        print("First 10 rows:")
        print(df.head(10).to_string())
        print()

        print("Basic statistics:")
        print(df.describe(include='all').to_string())
        print()

        # Check for transaction-related columns
        print("Looking for transaction-related columns...")
        transaction_cols = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['transaction', 'order', 'id', 'date', 'time']):
                transaction_cols.append(col)

        if transaction_cols:
            print(f"✓ Found potential transaction columns: {', '.join(transaction_cols)}")
        print()

        # Check for product-related columns
        print("Looking for product-related columns...")
        product_cols = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['product', 'item', 'name', 'category', 'detail']):
                product_cols.append(col)

        if product_cols:
            print(f"✓ Found potential product columns: {', '.join(product_cols)}")
        print()

        # Save this dataframe info
        print(f"Saving dataset info to: dataset_info_{file.split('.')[0]}.txt")
        with open(f"dataset_info_{file.split('.')[0]}.txt", 'w') as f:
            f.write(f"Dataset: {file}\n")
            f.write(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n\n")
            f.write("Columns:\n")
            for col in df.columns:
                f.write(f"  - {col} ({df[col].dtype})\n")
            f.write(f"\nFirst 10 rows:\n")
            f.write(df.head(10).to_string())

    except Exception as e:
        print(f"❌ Error loading file: {str(e)}")
        continue

print()
print("="*80)
print("EXPLORATION COMPLETE!")
print("="*80)
print()
print("Next steps:")
print("  1. Review the output above to understand the dataset structure")
print("  2. Identify transaction ID, product, and timestamp columns")
print("  3. Adapt the Apriori analysis script for this new format")
print()
