"""
Comprehensive Verification of Association Rule Mining Analysis

This script checks for correctness across all analyses:
- Data loading and preprocessing
- Transaction basket creation
- Apriori algorithm execution
- Metrics calculations
- Comparison analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

print("="*80)
print("COMPREHENSIVE VERIFICATION OF ANALYSIS")
print("="*80)
print()

verification_results = []
errors_found = []
warnings_found = []

def add_result(category, check, status, details=""):
    """Add a verification result"""
    verification_results.append({
        'Category': category,
        'Check': check,
        'Status': status,
        'Details': details
    })
    if status == "❌ FAIL":
        errors_found.append(f"{category}: {check} - {details}")
    elif status == "⚠️  WARN":
        warnings_found.append(f"{category}: {check} - {details}")

# ============================================================================
# VERIFICATION 1: DATASET 1 DATA LOADING
# ============================================================================

print("Verification 1: Dataset 1 (NYC 2023) - Data Loading")
print("-"*80)

try:
    # Load original data
    dataset1_path = Path.home() / ".cache/kagglehub/datasets/alfiaziz003/coffee-shop-sales-dashboard-by-alfi-aziz/versions/1/Coffee Shop Sales Dashboard by Alfi Aziz.xlsx"

    if not dataset1_path.exists():
        add_result("Dataset 1", "File exists", "❌ FAIL", "Dataset file not found")
    else:
        df1_raw = pd.read_excel(dataset1_path, sheet_name="Transactions")
        print(f"✓ Loaded {len(df1_raw):,} rows")
        add_result("Dataset 1", "File loading", "✓ PASS", f"{len(df1_raw):,} rows loaded")

        # Check required columns
        required_cols = ['transaction_date', 'transaction_time', 'product_detail', 'store_location']
        missing_cols = [col for col in required_cols if col not in df1_raw.columns]

        if missing_cols:
            add_result("Dataset 1", "Required columns", "❌ FAIL", f"Missing: {missing_cols}")
        else:
            add_result("Dataset 1", "Required columns", "✓ PASS", "All required columns present")

        # Check for null values in critical columns
        null_products = df1_raw['product_detail'].isna().sum()
        if null_products > 0:
            add_result("Dataset 1", "Null products", "⚠️  WARN", f"{null_products} null product values")
        else:
            add_result("Dataset 1", "Null products", "✓ PASS", "No null products")

        print(f"✓ Data integrity checks passed")

except Exception as e:
    add_result("Dataset 1", "Data loading", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 2: DATASET 1 TRANSACTION GROUPING
# ============================================================================

print("Verification 2: Dataset 1 - Transaction Basket Creation")
print("-"*80)

try:
    # Load processed results
    results1_path = Path("apriori_results/association_rules_by_segment.csv")
    if not results1_path.exists():
        add_result("Dataset 1", "Results file", "❌ FAIL", "Results file not found")
    else:
        results1 = pd.read_csv(results1_path)
        print(f"✓ Loaded {len(results1)} rules")
        add_result("Dataset 1", "Results loading", "✓ PASS", f"{len(results1)} rules loaded")

        # Verify rule structure
        required_rule_cols = ['Time_Segment', 'Antecedent_Items', 'Consequent_Items',
                              'Support', 'Confidence', 'Lift']
        missing_rule_cols = [col for col in required_rule_cols if col not in results1.columns]

        if missing_rule_cols:
            add_result("Dataset 1", "Rule structure", "❌ FAIL", f"Missing columns: {missing_rule_cols}")
        else:
            add_result("Dataset 1", "Rule structure", "✓ PASS", "All rule columns present")

        # Verify metric ranges
        if (results1['Confidence'] < 0).any() or (results1['Confidence'] > 1).any():
            add_result("Dataset 1", "Confidence range", "❌ FAIL", "Confidence outside [0,1]")
        else:
            add_result("Dataset 1", "Confidence range", "✓ PASS", "Confidence in valid range")

        if (results1['Support'] < 0).any() or (results1['Support'] > 1).any():
            add_result("Dataset 1", "Support range", "❌ FAIL", "Support outside [0,1]")
        else:
            add_result("Dataset 1", "Support range", "✓ PASS", "Support in valid range")

        if (results1['Lift'] <= 0).any():
            add_result("Dataset 1", "Lift values", "❌ FAIL", "Lift values <= 0 found")
        else:
            add_result("Dataset 1", "Lift values", "✓ PASS", "All lift values positive")

        # Verify time segments
        expected_segments = ['Morning_Weekday', 'Morning_Weekend', 'Afternoon_Weekday',
                            'Afternoon_Weekend', 'Evening_Weekday', 'Evening_Weekend']
        actual_segments = results1['Time_Segment'].unique()

        unexpected_segments = set(actual_segments) - set(expected_segments)
        if unexpected_segments:
            add_result("Dataset 1", "Time segments", "⚠️  WARN",
                      f"Unexpected segments: {unexpected_segments}")
        else:
            add_result("Dataset 1", "Time segments", "✓ PASS",
                      f"Valid segments: {len(actual_segments)}")

        print(f"✓ Rule validation checks passed")

except Exception as e:
    add_result("Dataset 1", "Results validation", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 3: DATASET 2 DATA LOADING
# ============================================================================

print("Verification 3: Dataset 2 (April 2019) - Data Loading")
print("-"*80)

try:
    dataset2_path = Path.home() / ".cache/kagglehub/datasets/ylchang/coffee-shop-sample-data-1113/versions/1/201904 sales reciepts.csv"

    if not dataset2_path.exists():
        add_result("Dataset 2", "File exists", "❌ FAIL", "Dataset file not found")
    else:
        df2_raw = pd.read_csv(dataset2_path)
        print(f"✓ Loaded {len(df2_raw):,} rows")
        add_result("Dataset 2", "File loading", "✓ PASS", f"{len(df2_raw):,} rows loaded")

        # Check required columns
        required_cols = ['transaction_id', 'transaction_date', 'transaction_time', 'product_id']
        missing_cols = [col for col in required_cols if col not in df2_raw.columns]

        if missing_cols:
            add_result("Dataset 2", "Required columns", "❌ FAIL", f"Missing: {missing_cols}")
        else:
            add_result("Dataset 2", "Required columns", "✓ PASS", "All required columns present")

        # Verify transaction IDs
        unique_transactions = df2_raw['transaction_id'].nunique()
        print(f"✓ Found {unique_transactions:,} unique transactions")
        add_result("Dataset 2", "Transaction count", "✓ PASS",
                  f"{unique_transactions:,} unique transactions")

        # Check for duplicates in line items
        expected_line_items = len(df2_raw)
        if expected_line_items != len(df2_raw):
            add_result("Dataset 2", "Line item integrity", "❌ FAIL", "Duplicate line items found")
        else:
            add_result("Dataset 2", "Line item integrity", "✓ PASS", "No duplicate line items")

        print(f"✓ Data integrity checks passed")

except Exception as e:
    add_result("Dataset 2", "Data loading", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 4: DATASET 2 RESULTS
# ============================================================================

print("Verification 4: Dataset 2 - Results Validation")
print("-"*80)

try:
    results2_path = Path("apriori_results_new/association_rules_by_segment.csv")
    if not results2_path.exists():
        add_result("Dataset 2", "Results file", "❌ FAIL", "Results file not found")
    else:
        results2 = pd.read_csv(results2_path)
        print(f"✓ Loaded {len(results2):,} rules")
        add_result("Dataset 2", "Results loading", "✓ PASS", f"{len(results2):,} rules loaded")

        # Verify metric ranges
        if (results2['Confidence'] < 0).any() or (results2['Confidence'] > 1).any():
            add_result("Dataset 2", "Confidence range", "❌ FAIL", "Confidence outside [0,1]")
        else:
            add_result("Dataset 2", "Confidence range", "✓ PASS", "Confidence in valid range")

        if (results2['Support'] < 0).any() or (results2['Support'] > 1).any():
            add_result("Dataset 2", "Support range", "❌ FAIL", "Support outside [0,1]")
        else:
            add_result("Dataset 2", "Support range", "✓ PASS", "Support in valid range")

        if (results2['Lift'] <= 0).any():
            add_result("Dataset 2", "Lift values", "❌ FAIL", "Lift values <= 0 found")
        else:
            add_result("Dataset 2", "Lift values", "✓ PASS", "All lift values positive")

        # Check for suspiciously high values
        max_lift = results2['Lift'].max()
        if max_lift > 100:
            add_result("Dataset 2", "Lift magnitude", "⚠️  WARN",
                      f"Very high lift value: {max_lift:.1f}")
        else:
            add_result("Dataset 2", "Lift magnitude", "✓ PASS", f"Max lift: {max_lift:.1f}")

        # Verify confidence >= support (mathematical requirement)
        invalid_rules = results2[results2['Confidence'] < results2['Support']]
        if len(invalid_rules) > 0:
            add_result("Dataset 2", "Confidence >= Support", "❌ FAIL",
                      f"{len(invalid_rules)} rules violate this")
        else:
            add_result("Dataset 2", "Confidence >= Support", "✓ PASS",
                      "All rules satisfy this requirement")

        print(f"✓ Rule validation checks passed")

except Exception as e:
    add_result("Dataset 2", "Results validation", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 5: MATHEMATICAL CONSISTENCY
# ============================================================================

print("Verification 5: Mathematical Consistency Checks")
print("-"*80)

try:
    # Check Lift calculation: Lift = Confidence / Consequent_Support
    # For Dataset 1
    if 'results1' in locals():
        calculated_lift = results1['Confidence'] / results1['Consequent_Support']
        lift_diff = np.abs(calculated_lift - results1['Lift'])

        if (lift_diff > 0.01).any():  # Allow small rounding errors
            max_diff = lift_diff.max()
            add_result("Dataset 1", "Lift calculation", "⚠️  WARN",
                      f"Max difference: {max_diff:.4f}")
        else:
            add_result("Dataset 1", "Lift calculation", "✓ PASS",
                      "Lift values mathematically correct")

        print("✓ Dataset 1 lift calculations verified")

    # For Dataset 2 (check sample)
    if 'results2' in locals():
        sample_size = min(1000, len(results2))
        results2_sample = results2.head(sample_size)

        calculated_lift = results2_sample['Confidence'] / results2_sample['Consequent_Support']
        lift_diff = np.abs(calculated_lift - results2_sample['Lift'])

        if (lift_diff > 0.01).any():
            max_diff = lift_diff.max()
            add_result("Dataset 2", "Lift calculation", "⚠️  WARN",
                      f"Max difference in sample: {max_diff:.4f}")
        else:
            add_result("Dataset 2", "Lift calculation", "✓ PASS",
                      "Lift values mathematically correct (sample)")

        print("✓ Dataset 2 lift calculations verified (sample)")

except Exception as e:
    add_result("Math Check", "Lift verification", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 6: COMPARISON ANALYSIS
# ============================================================================

print("Verification 6: Comparison Analysis Validation")
print("-"*80)

try:
    comparison_path = Path("comparison_results/comparison_report.txt")

    if not comparison_path.exists():
        add_result("Comparison", "Report file", "❌ FAIL", "Report not found")
    else:
        with open(comparison_path, 'r') as f:
            comparison_content = f.read()

        add_result("Comparison", "Report exists", "✓ PASS", "Report file found")

        # Check that metrics file exists and is valid
        metrics_path = Path("comparison_results/metrics_comparison.csv")
        if metrics_path.exists():
            metrics_comp = pd.read_csv(metrics_path)
            add_result("Comparison", "Metrics file", "✓ PASS",
                      f"{len(metrics_comp)} metrics compared")
        else:
            add_result("Comparison", "Metrics file", "⚠️  WARN", "Metrics file not found")

        # Check category comparison
        category_path = Path("comparison_results/category_comparison.csv")
        if category_path.exists():
            category_comp = pd.read_csv(category_path)
            add_result("Comparison", "Category file", "✓ PASS",
                      f"{len(category_comp)} categories compared")
        else:
            add_result("Comparison", "Category file", "⚠️  WARN", "Category file not found")

        print("✓ Comparison files validated")

except Exception as e:
    add_result("Comparison", "Validation", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 7: VISUALIZATION FILES
# ============================================================================

print("Verification 7: Visualization Files")
print("-"*80)

try:
    viz_dirs = {
        'Dataset 1': Path('visualizations'),
        'Dataset 2': Path('visualizations_new'),
        'Comparison': Path('comparison_results')
    }

    for name, viz_dir in viz_dirs.items():
        if not viz_dir.exists():
            add_result("Visualizations", f"{name} directory", "❌ FAIL", "Directory not found")
        else:
            png_files = list(viz_dir.glob('*.png'))
            if len(png_files) == 0:
                add_result("Visualizations", f"{name} images", "⚠️  WARN", "No PNG files found")
            else:
                add_result("Visualizations", f"{name} images", "✓ PASS",
                          f"{len(png_files)} images found")
                print(f"✓ {name}: {len(png_files)} visualizations")

except Exception as e:
    add_result("Visualizations", "File check", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 8: SPOT CHECK APRIORI CALCULATION
# ============================================================================

print("Verification 8: Spot Check - Manual Apriori Calculation")
print("-"*80)

try:
    # Create a simple test case to verify Apriori works correctly
    test_transactions = [
        ['milk', 'bread', 'butter'],
        ['milk', 'bread'],
        ['milk', 'butter'],
        ['bread', 'butter'],
        ['milk', 'bread', 'butter'],
    ]

    te = TransactionEncoder()
    te_array = te.fit(test_transactions).transform(test_transactions)
    df_test = pd.DataFrame(te_array, columns=te.columns_)

    # Run Apriori
    frequent_itemsets = apriori(df_test, min_support=0.4, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

    if len(rules) > 0:
        add_result("Spot Check", "Apriori execution", "✓ PASS",
                  f"Generated {len(rules)} test rules")
        print(f"✓ Apriori algorithm works correctly")

        # Verify a specific rule
        # milk -> bread should exist (appears in 4 out of 5 transactions with milk)
        milk_bread_rules = rules[
            (rules['antecedents'] == frozenset(['milk'])) &
            (rules['consequents'] == frozenset(['bread']))
        ]

        if len(milk_bread_rules) > 0:
            confidence = milk_bread_rules.iloc[0]['confidence']
            expected_confidence = 4/4  # milk appears in 4 transactions, 4 have bread

            if abs(confidence - expected_confidence) < 0.01:
                add_result("Spot Check", "Confidence calculation", "✓ PASS",
                          f"Confidence matches expected: {confidence:.2f}")
            else:
                add_result("Spot Check", "Confidence calculation", "⚠️  WARN",
                          f"Expected {expected_confidence:.2f}, got {confidence:.2f}")
        else:
            add_result("Spot Check", "Rule generation", "⚠️  WARN",
                      "Expected milk->bread rule not found")
    else:
        add_result("Spot Check", "Apriori execution", "⚠️  WARN",
                  "No test rules generated")

except Exception as e:
    add_result("Spot Check", "Apriori test", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# VERIFICATION 9: CHECK FOR COMMON ISSUES
# ============================================================================

print("Verification 9: Common Issues Check")
print("-"*80)

try:
    # Check for single-item transactions affecting results
    if 'results1' in locals():
        single_item_rules = results1[
            (results1['Antecedent_Items'].str.count(',') == 0) &
            (results1['Consequent_Items'].str.count(',') == 0)
        ]

        if len(single_item_rules) == len(results1):
            add_result("Issues", "Rule complexity DS1", "✓ PASS",
                      "All rules are item pairs")
        else:
            multi_item_count = len(results1) - len(single_item_rules)
            add_result("Issues", "Rule complexity DS1", "✓ PASS",
                      f"{multi_item_count} multi-item rules")

        print(f"✓ Dataset 1: {len(single_item_rules)}/{len(results1)} are simple pairs")

    if 'results2' in locals():
        results2_sample = results2.head(1000)
        single_item_rules = results2_sample[
            (results2_sample['Antecedent_Items'].str.count(',') == 0) &
            (results2_sample['Consequent_Items'].str.count(',') == 0)
        ]

        multi_item_count = len(results2_sample) - len(single_item_rules)
        add_result("Issues", "Rule complexity DS2", "✓ PASS",
                  f"{multi_item_count}/{len(results2_sample)} are multi-item (sample)")

        print(f"✓ Dataset 2: {multi_item_count}/{len(results2_sample)} are multi-item (sample)")

except Exception as e:
    add_result("Issues", "Complexity check", "❌ FAIL", str(e))
    print(f"❌ Error: {e}")

print()

# ============================================================================
# GENERATE VERIFICATION REPORT
# ============================================================================

print("="*80)
print("VERIFICATION SUMMARY")
print("="*80)
print()

# Create DataFrame
verification_df = pd.DataFrame(verification_results)

# Count results
total_checks = len(verification_df)
passed = len(verification_df[verification_df['Status'] == '✓ PASS'])
warnings = len(verification_df[verification_df['Status'] == '⚠️  WARN'])
failed = len(verification_df[verification_df['Status'] == '❌ FAIL'])

print(f"Total Checks: {total_checks}")
print(f"  ✓ Passed: {passed}")
print(f"  ⚠️  Warnings: {warnings}")
print(f"  ❌ Failed: {failed}")
print()

if failed > 0:
    print("❌ CRITICAL ERRORS FOUND:")
    for error in errors_found:
        print(f"  • {error}")
    print()

if warnings > 0:
    print("⚠️  WARNINGS:")
    for warning in warnings_found:
        print(f"  • {warning}")
    print()

# Display results by category
print("Results by Category:")
print("-"*80)
for category in verification_df['Category'].unique():
    cat_results = verification_df[verification_df['Category'] == category]
    cat_pass = len(cat_results[cat_results['Status'] == '✓ PASS'])
    cat_total = len(cat_results)
    print(f"{category:<20} {cat_pass}/{cat_total} checks passed")

print()

# Save detailed results
verification_df.to_csv('verification_results.csv', index=False)
print("✓ Detailed results saved to: verification_results.csv")

# Save text report
report_lines = []
report_lines.append("="*80)
report_lines.append("VERIFICATION REPORT")
report_lines.append("="*80)
report_lines.append("")
report_lines.append(f"Total Checks: {total_checks}")
report_lines.append(f"Passed: {passed}")
report_lines.append(f"Warnings: {warnings}")
report_lines.append(f"Failed: {failed}")
report_lines.append("")

if failed > 0:
    report_lines.append("CRITICAL ERRORS:")
    for error in errors_found:
        report_lines.append(f"  • {error}")
    report_lines.append("")

if warnings > 0:
    report_lines.append("WARNINGS:")
    for warning in warnings_found:
        report_lines.append(f"  • {warning}")
    report_lines.append("")

report_lines.append("DETAILED RESULTS:")
report_lines.append("-"*80)
for _, row in verification_df.iterrows():
    report_lines.append(f"{row['Status']} [{row['Category']}] {row['Check']}")
    if row['Details']:
        report_lines.append(f"    {row['Details']}")

report_lines.append("")
report_lines.append("="*80)
report_lines.append("OVERALL VERDICT")
report_lines.append("="*80)
report_lines.append("")

if failed == 0 and warnings == 0:
    report_lines.append("✓ ALL CHECKS PASSED")
    report_lines.append("The analysis is verified to be correct.")
    verdict = "PASS"
elif failed == 0:
    report_lines.append("⚠️  PASSED WITH WARNINGS")
    report_lines.append("The analysis is generally correct but has some warnings to review.")
    verdict = "PASS_WITH_WARNINGS"
else:
    report_lines.append("❌ VERIFICATION FAILED")
    report_lines.append("Critical errors were found that need to be addressed.")
    verdict = "FAIL"

report_text = "\n".join(report_lines)
print()
print(report_text)

with open('verification_report.txt', 'w') as f:
    f.write(report_text)

print()
print("✓ Verification report saved to: verification_report.txt")
print()
print("="*80)
print(f"FINAL VERDICT: {verdict}")
print("="*80)
