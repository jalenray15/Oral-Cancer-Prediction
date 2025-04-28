import numpy as np
import pandas as pd

# Load the dataset
print("Loading the dataset...")
df = pd.read_csv('oral_cancer_prediction_dataset.csv')

# Display basic information
print("\n--- DATASET OVERVIEW ---")
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# 1. DETECT AND HANDLE MISSING VALUES
print("\n--- HANDLING MISSING VALUES ---")
print("Missing values per column:")
missing_values = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100
missing_data = pd.concat([missing_values, missing_percent], axis=1)
missing_data.columns = ['Missing Values', 'Percentage']
print(missing_data[missing_data['Missing Values'] > 0])

# Fill missing values based on data type
print("\nFilling missing values...")
# For numerical columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        print(f"Filling {col} with median")
        df[col] = df[col].fillna(df[col].median())

# For categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if df[col].isnull().sum() > 0:
        print(f"Filling {col} with mode")
        df[col] = df[col].fillna(df[col].mode()[0])

# Verify no missing values remain
print(f"Missing values after filling: {df.isnull().sum().sum()}")

# 2. FILTER OUTLIERS USING NUMPY
print("\n--- HANDLING OUTLIERS ---")
# Function to detect and handle outliers using IQR method
def handle_outliers(df, column):
    Q1 = np.percentile(df[column], 25)
    Q3 = np.percentile(df[column], 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Count outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
    print(f"Column {column}: {len(outliers)} outliers detected")
    
    # Cap outliers instead of removing them
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    
    return df

# Handle outliers in numerical columns that make sense to cap
outlier_columns = ['Age', 'Tumor Size (cm)', 'Survival Rate (5-Year, %)', 
                  'Cost of Treatment (USD)', 'Economic Burden (Lost Workdays per Year)']

for col in outlier_columns:
    df = handle_outliers(df, col)

# 3. CALCULATE DESCRIPTIVE STATISTICS
print("\n--- DESCRIPTIVE STATISTICS ---")
# Basic statistics for numerical columns
print("Numerical Statistics:")
print(df[numeric_cols].describe())

# Calculate additional statistics using NumPy
print("\nAdditional Statistics using NumPy:")
for col in ['Age', 'Tumor Size (cm)', 'Survival Rate (5-Year, %)']:
    print(f"\n{col} statistics:")
    print(f"Mean: {np.mean(df[col])}")
    print(f"Median: {np.median(df[col])}")
    print(f"Standard deviation: {np.std(df[col])}")
    print(f"Min: {np.min(df[col])}")
    print(f"Max: {np.max(df[col])}")
    print(f"25th percentile: {np.percentile(df[col], 25)}")
    print(f"75th percentile: {np.percentile(df[col], 75)}")

# Correlation between numerical variables using NumPy
print("\nCorrelation matrix using NumPy:")
corr_cols = ['Age', 'Tumor Size (cm)', 'Cancer Stage', 'Survival Rate (5-Year, %)', 'Cost of Treatment (USD)']
corr_matrix = np.corrcoef(df[corr_cols].values, rowvar=False)
# Create a DataFrame for better display
corr_df = pd.DataFrame(corr_matrix, columns=corr_cols, index=corr_cols)
print(corr_df)

# 4. NORMALIZE DATA
print("\n--- NORMALIZING DATA ---")
# Function to normalize data using Min-Max scaling with NumPy
def normalize_column(df, column):
    min_val = np.min(df[column])
    max_val = np.max(df[column])
    df[f'{column}_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df

# Normalize numerical columns
normalize_columns = ['Age', 'Tumor Size (cm)', 'Cost of Treatment (USD)', 
                     'Economic Burden (Lost Workdays per Year)']

for col in normalize_columns:
    df = normalize_column(df, col)
    print(f"Created normalized column: {col}_normalized")

# Z-score normalization (another approach)
print("\nAdding Z-score normalized columns:")
for col in ['Age', 'Tumor Size (cm)']:
    col_mean = np.mean(df[col])
    col_std = np.std(df[col])
    df[f'{col}_zscore'] = (df[col] - col_mean) / col_std
    print(f"Created Z-score normalized column: {col}_zscore")

# 5. HANDLING INCONSISTENT FORMATS
print("\n--- HANDLING INCONSISTENT FORMATS ---")
# Standardize text data formats
for col in categorical_cols:
    # Convert to string and strip whitespace
    df[col] = df[col].astype(str).str.strip()
    # Convert to title case for consistency
    df[col] = df[col].str.title()
    print(f"Standardized format for {col}")

# Print sample of processed data
print("\n--- PROCESSED DATA SAMPLE ---")
print(df.head())

# Save the processed dataset
processed_file = 'oral_cancer_processed.csv'
df.to_csv(processed_file, index=False)
print(f"\nProcessed data saved to {processed_file}")

# SUMMARY OF TRANSFORMATIONS
print("\n--- SUMMARY OF DATA PREPARATION STEPS ---")
print(f"1. Handled missing values in {len(missing_data[missing_data['Missing Values'] > 0])} columns")
print(f"2. Addressed outliers in {len(outlier_columns)} numerical columns")
print(f"3. Calculated descriptive statistics using NumPy")
print(f"4. Created {len(normalize_columns)} normalized feature columns")
print(f"5. Standardized formats for {len(categorical_cols)} categorical variables")
print(f"6. Processed dataset shape: {df.shape}")

print("\nData preparation complete and ready for analysis or modeling.")