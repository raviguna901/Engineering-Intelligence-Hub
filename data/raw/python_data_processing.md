# Python Data Processing Troubleshooting

## Pandas Missing Values
Use isna and isnull to identify missing values. Decide whether to remove or impute missing values based on their meaning and quantity. Avoid replacing missing values blindly because missingness may contain useful information.

## Data Types
Inspect DataFrame column types with dtypes and info. Convert numeric strings using pandas.to_numeric when appropriate. Invalid values can raise errors or become missing when errors='coerce' is specified.

## Duplicate Records
Use duplicated to identify repeated rows and drop_duplicates to remove them when appropriate. Before deleting duplicates, determine whether repeated records represent genuine events or accidental duplication.

## Train-Test Preprocessing
Split the dataset before learning preprocessing parameters. Fit imputers, scalers, and encoders on training data, then transform the test data using those fitted objects. A scikit-learn Pipeline helps prevent data leakage.

## File Paths
Prefer pathlib.Path for cross-platform file paths. Check that input files exist before reading them and use clear error messages when paths are incorrect.
