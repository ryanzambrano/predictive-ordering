"""
Main Script to Run Complete Apriori Analysis Pipeline
======================================================

This script runs all analysis components in the correct sequence:
1. Primary dataset Apriori analysis
2. Visualization generation
3. Secondary dataset Apriori analysis
4. Cross-dataset comparison
5. Comprehensive verification
6. Results explanation

Usage:
    python3 run_analysis.py

Estimated Runtime: 5-10 minutes

Author: Course Project
Date: November 2024
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def print_section(text):
    """Print a formatted section header"""
    print("\n" + "-"*80)
    print(text)
    print("-"*80)

def run_script(script_name, description):
    """
    Run a Python script and handle errors

    Args:
        script_name: Name of the script file
        description: Description of what the script does

    Returns:
        bool: True if successful, False otherwise
    """
    script_path = Path(__file__).parent / script_name

    if not script_path.exists():
        print(f"❌ ERROR: Script '{script_name}' not found!")
        return False

    print_section(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False,  # Show output in real-time
            text=True
        )

        print(f"\n✓ Completed: {script_name}")
        print(f"Finished: {datetime.now().strftime('%H:%M:%S')}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: Script '{script_name}' failed with exit code {e.returncode}")
        print(f"Please check the error messages above and fix any issues.")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: Unexpected error running '{script_name}': {str(e)}")
        return False

def main():
    """Main execution function"""

    print_banner("TIME-SEGMENTED APRIORI ANALYSIS - COMPLETE PIPELINE")

    start_time = datetime.now()
    print(f"Pipeline started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Working directory: {Path.cwd()}")

    # Define the analysis pipeline (only essential scripts)
    pipeline = [
        ("apriori_analysis.py", "Step 1/3: Primary Dataset Apriori Analysis"),
        ("visualize_results.py", "Step 2/3: Generate Visualizations and Figures"),
        ("compare_datasets.py", "Step 3/3: Cross-Dataset Comparison Analysis"),
    ]

    # Track results
    results = []

    # Execute each script in sequence
    for i, (script, description) in enumerate(pipeline, 1):
        success = run_script(script, description)
        results.append((script, success))

        if not success:
            print_banner("PIPELINE STOPPED DUE TO ERROR")
            print(f"Failed at step {i}/{len(pipeline)}: {script}")
            print("\nPlease review the error messages above and:")
            print("1. Ensure all required libraries are installed (pip install -r requirements.txt)")
            print("2. Verify the dataset files are present")
            print("3. Check that you have sufficient disk space")
            print("4. Review the README.md for troubleshooting tips")
            sys.exit(1)

    # Calculate elapsed time
    end_time = datetime.now()
    elapsed = end_time - start_time
    minutes, seconds = divmod(elapsed.total_seconds(), 60)

    # Print summary
    print_banner("PIPELINE COMPLETED SUCCESSFULLY")

    print("Execution Summary:")
    print("-" * 80)
    for script, success in results:
        status = "✓ SUCCESS" if success else "❌ FAILED"
        print(f"  {status}: {script}")

    print(f"\nTotal execution time: {int(minutes)} minutes {int(seconds)} seconds")
    print(f"Pipeline completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "="*80)
    print("OUTPUT LOCATIONS:")
    print("="*80)
    print("  • Association Rules:    apriori_results/")
    print("  • Visualizations:       visualizations/")
    print("  • Comparison Results:   comparison_results/")
    print("  • Verification Report:  verification_report.txt")
    print("\nAll results are ready for review!")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user (Ctrl+C)")
        print("Partial results may be available in output directories.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
