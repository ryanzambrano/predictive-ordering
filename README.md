# Time-Segmented Apriori Analysis for Café Inventory Optimization

## Project Overview

This project applies time-segmented association rule mining to café transaction data to identify high-confidence item co-occurrence patterns that can optimize food inventory and reduce surplus.

**Research Question:** Can time-segmented association rule mining of café transaction data identify high-confidence item co-occurrence patterns, {A} → {B}, that, when applied to purchasing, effectively refine food inventory and reduce surplus food for cafés?

## Quick Start

**To run the complete analysis with a single command:**
```bash
python3 run_analysis.py
```
This will execute all analyses sequentially and generate all results (see detailed instructions below).

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Active internet connection (for initial dataset download from Kaggle)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd predictive-ordering
```

3. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Required Libraries

The project uses the following Python libraries (versions specified in requirements.txt):
- **pandas (2.3.3)**: Data manipulation and analysis
- **numpy (2.3.5)**: Numerical computing
- **matplotlib (3.10.7)**: Data visualization
- **seaborn (0.13.2)**: Statistical data visualization
- **openpyxl (3.1.5)**: Excel file handling
- **mlxtend (0.23.4)**: Machine learning extensions (Apriori algorithm)
- **kagglehub (0.3.13)**: Kaggle dataset access
- **networkx (3.5)**: Network graph visualization

## Datasets

The project analyzes two coffee shop transaction datasets:

1. **Dataset 1 (Primary)**: Coffee Shop Sales Dashboard by Alfi Aziz
   - Source: Kaggle (downloaded via kagglehub)
   - Coverage: 6 months of transactions in NYC, 2023
   - File: `Coffee Shop Sales Dashboard by Alfi Aziz.xlsx`

2. **Dataset 2 (Comparison)**: Coffee Shop Sample Data
   - Source: Kaggle (downloaded via kagglehub)
   - Coverage: 1 month (April 2019)
   - File: `149116 sales reciepts.csv`

## Project Structure

```
predictive-ordering/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── SUBMISSION_NOTES.txt                   # Submission guidelines
│
├── ESSENTIAL CODE FILES (5 scripts):
├── run_analysis.py                        # SINGLE-TRIGGER main script
├── apriori_analysis.py                    # Primary Apriori analysis (Dataset 1)
├── apriori_new_dataset.py                 # Apriori analysis on Dataset 2
├── visualize_results.py                   # Generate visualizations
├── compare_datasets.py                    # Cross-dataset comparison
│
├── Dataset:
├── Coffee Shop Sales Dashboard by Alfi Aziz.xlsx  # Primary dataset
│
├── Generated Output Directories:
├── apriori_results/                       # Results from Dataset 1
├── apriori_results_new/                   # Results from Dataset 2
├── comparison_results/                    # Cross-dataset comparison
├── visualizations/                        # Primary visualizations
└── visualizations_new/                    # Secondary visualizations
```

**Note:** Exploration scripts (explore_*.py, download_dataset.py, verify_analysis.py, explain_results.py) are NOT included in the submission as they're not essential for running the core analysis.

## Running the Code

### SINGLE-TRIGGER EXECUTION (Recommended)

Run the complete analysis pipeline with one command:

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run complete pipeline with single trigger
python3 run_analysis.py
```

**This single command will:**
1. Run primary dataset Apriori analysis (Dataset 1)
2. Generate all visualizations and figures
3. Run secondary dataset analysis and cross-dataset comparison

**Estimated Runtime:** 5-10 minutes depending on system specifications

**Real-time Progress:** The script displays live progress updates, completion status for each phase, and timing information.

### Option 2: Run Individual Scripts

Execute scripts individually for specific analyses:

#### 1. Primary Analysis (Dataset 1)
```bash
python3 apriori_analysis.py
```
**Output:**
- `apriori_results/association_rules_by_segment.csv` - All association rules
- `apriori_results/rules_*.csv` - Rules by time segment
- `apriori_results/analysis_summary.txt` - Summary statistics
- Progress display with real-time status updates

#### 2. Generate Visualizations
```bash
python3 visualize_results.py
```
**Output:**
- `visualizations/1_confidence_by_segment.png` - Confidence distribution
- `visualizations/2_lift_by_segment.png` - Lift analysis
- `visualizations/3_support_confidence_scatter.png` - Scatter plot
- `visualizations/4_association_network.png` - Network graph
- `visualizations/5_combined_dashboard.png` - Comprehensive dashboard
- `visualizations/6_inventory_recommendations.png` - Actionable recommendations

#### 3. Cross-Dataset Comparison
```bash
python3 compare_datasets.py
```
**Output:**
- Runs `apriori_new_dataset.py` internally for Dataset 2
- `comparison_results/comparison_report.txt` - Detailed comparison
- `comparison_results/*.csv` - Comparative metrics
- `comparison_results/*.png` - Comparison visualizations

## Real-Time Progress Tracking

All scripts include real-time progress indicators showing:
- Current phase of execution
- Estimated completion percentage
- Success/failure status for each step
- Summary statistics as they're computed

Example output:
```
================================================================================
TIME-SEGMENTED APRIORI ANALYSIS FOR CAFÉ INVENTORY
================================================================================

Phase 1: Loading and preprocessing data...
--------------------------------------------------------------------------------
✓ Loaded 149,116 rows and 11 columns

Phase 2: Converting date/time formats...
--------------------------------------------------------------------------------
✓ Converted Excel numeric date format
✓ Date range: 2023-01-01 to 2023-06-30
...
Analysis Complete!
================================================================================
```

## Expected Results

### Association Rules
- 400-800 high-confidence association rules per dataset
- Rules segmented by time period (Morning/Afternoon × Weekday/Weekend)
- Minimum support: 2%
- Minimum confidence: 40%

### Key Metrics
- **Support**: Frequency of item combinations
- **Confidence**: Probability of consequent given antecedent
- **Lift**: Strength of association (>1 indicates positive correlation)

### Visualizations
- Confidence distributions by time segment
- Lift analysis showing strongest associations
- Network graphs of product relationships
- Comparative analysis between datasets

## Code Organization

All code files include:
- Detailed docstrings explaining purpose
- Phase-by-phase execution with progress indicators
- Inline comments for complex operations
- Error handling and validation
- Output directory management

## Methodology

### 1. Data Preprocessing
- Excel/CSV file loading
- Date/time format conversion
- Transaction basket creation (grouping items by transaction ID)
- Time segmentation (Morning/Afternoon, Weekday/Weekend)

### 2. Apriori Algorithm
- Frequent itemset mining with minimum support threshold
- Association rule generation with minimum confidence threshold
- Metric calculation (support, confidence, lift)

### 3. Time Segmentation
- **Morning**: 6:00 AM - 12:00 PM
- **Afternoon**: 12:00 PM - 6:00 PM
- **Weekday**: Monday - Friday
- **Weekend**: Saturday - Sunday

### 4. Validation
- Cross-dataset comparison
- Statistical verification
- Metric consistency checks

## Troubleshooting

### Dataset Not Found
If the dataset file is not found, ensure:
1. The Excel file is in the project root directory, or
2. The file is downloaded via kagglehub (automatic on first run)

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Memory Issues
For large datasets, the scripts may require 2-4 GB of available RAM. Close other applications if needed.

## Citation

If using borrowed code or external libraries:
- **mlxtend**: Raschka, S. (2018). MLxtend: Providing machine learning and data science utilities and extensions to Python's scientific computing stack. Journal of Open Source Software, 3(24), 638.
- **Datasets**: Kaggle datasets cited in code comments and docstrings

## Academic Integrity

This project was developed for educational purposes. All external code sources are properly cited within the code files. The Apriori algorithm implementation uses the mlxtend library (properly cited above).

## Submission Package

To create a submission-ready zip file (under 50 MB):

```bash
python3 create_submission_zip.py
```

This will create `submission.zip` containing:
- All code files
- Documentation (README, requirements.txt)
- Dataset file
- Sample visualization outputs

**Note:** Generated results (CSV files, full visualizations) are excluded from the zip to meet the 50MB size limit. The instructor can regenerate all results by running `python3 run_analysis.py`.

See `SUBMISSION_NOTES.txt` for detailed submission guidelines.

## Contact

For questions or issues running the code, refer to the inline documentation in each script file.

---

**Last Updated:** November 2024
