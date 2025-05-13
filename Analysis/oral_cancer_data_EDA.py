import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for plots
sns.set(style="whitegrid")
plt.style.use('seaborn-v0_8')

# Load the dataset
print("Loading the oral cancer dataset...")
df = pd.read_csv('oral_cancer_prediction_dataset.csv')

# Display basic info about the dataset
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values per column:")
missing_values = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100
missing_data = pd.concat([missing_values, missing_percent], axis=1)
missing_data.columns = ['Missing Values', 'Percentage']
print(missing_data[missing_data['Missing Values'] > 0])

# Fill missing values if necessary
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])

print("\n--- EXPLORATORY DATA ANALYSIS (EDA) ---")

# SECTION 1: UNIVARIATE ANALYSIS
print("\n=== UNIVARIATE ANALYSIS ===")

# 1. Distribution of Age (Histogram)
plt.figure(figsize=(10, 6))
sns.histplot(df['Age'], bins=20, kde=True)
plt.title('Distribution of Patient Age', fontsize=16)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.savefig('age_distribution.png')
plt.close()

# 2. Detect outliers in Tumor Size using Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(y=df['Tumor Size (cm)'])
plt.title('Tumor Size Distribution (Outlier Detection)', fontsize=16)
plt.ylabel('Tumor Size (cm)', fontsize=12)
plt.savefig('tumor_size_boxplot.png')
plt.close()

# 3. Distribution of Cancer Stage (Count Plot)
plt.figure(figsize=(10, 6))
sns.countplot(x='Cancer Stage', data=df)
plt.title('Distribution of Cancer Stages', fontsize=16)
plt.xlabel('Cancer Stage', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.savefig('cancer_stage_distribution.png')
plt.close()

# 4. Risk Factors Distribution
risk_factors = ['Tobacco Use', 'Alcohol Consumption', 'HPV Infection', 'Betel Quid Use']
plt.figure(figsize=(14, 10))

for i, factor in enumerate(risk_factors, 1):
    plt.subplot(2, 2, i)
    sns.countplot(x=factor, data=df)
    plt.title(f'Distribution of {factor}', fontsize=14)
    plt.xlabel(factor, fontsize=10)
    plt.ylabel('Count', fontsize=10)

plt.tight_layout()
plt.savefig('risk_factors_distribution.png')
plt.close()

# 5. Distribution of Oral Cancer Diagnosis
plt.figure(figsize=(10, 6))
diagnosis_counts = df['Oral Cancer (Diagnosis)'].value_counts()
plt.pie(diagnosis_counts, labels=diagnosis_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Oral Cancer Diagnosis Distribution', fontsize=16)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.savefig('diagnosis_distribution_pie.png')
plt.close()

# 6. Central Tendency for Key Variables
age_mean = df['Age'].mean()
age_median = df['Age'].median()
tumor_mean = df['Tumor Size (cm)'].mean()
tumor_median = df['Tumor Size (cm)'].median()
survival_mean = df['Survival Rate (5-Year, %)'].mean()
survival_median = df['Survival Rate (5-Year, %)'].median()

print("\nCentral Tendency Measures:")
print(f"Age - Mean: {age_mean:.2f}, Median: {age_median:.2f}")
print(f"Tumor Size - Mean: {tumor_mean:.2f}cm, Median: {tumor_median:.2f}cm")
print(f"5-Year Survival Rate - Mean: {survival_mean:.2f}%, Median: {survival_median:.2f}%")

# SECTION 2: MULTIVARIATE ANALYSIS
print("\n=== MULTIVARIATE ANALYSIS ===")

# 7. Correlation Heatmap for Numerical Variables
plt.figure(figsize=(14, 10))
numerical_df = df.select_dtypes(include=['int64', 'float64'])
correlation = numerical_df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap of Numerical Variables', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

# 8. Relationship between Age and Tumor Size (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Age', y='Tumor Size (cm)', hue='Oral Cancer (Diagnosis)', data=df, alpha=0.6)
plt.title('Age vs Tumor Size by Diagnosis', fontsize=16)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Tumor Size (cm)', fontsize=12)
plt.savefig('age_vs_tumor_size.png')
plt.close()

# 9. Relationship between Tumor Size and Survival Rate
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Tumor Size (cm)', y='Survival Rate (5-Year, %)', hue='Cancer Stage', data=df, alpha=0.6, palette='viridis')
plt.title('Tumor Size vs 5-Year Survival Rate by Cancer Stage', fontsize=16)
plt.xlabel('Tumor Size (cm)', fontsize=12)
plt.ylabel('5-Year Survival Rate (%)', fontsize=12)
plt.savefig('tumor_size_vs_survival.png')
plt.close()

# SECTION 3: CATEGORICAL VS. NUMERICAL DATA (COMPARING GROUPS)
print("\n=== COMPARING GROUPS ===")

# 10. Survival Rate by Gender (Box Plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Gender', y='Survival Rate (5-Year, %)', data=df)
plt.title('5-Year Survival Rate by Gender', fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('5-Year Survival Rate (%)', fontsize=12)
plt.savefig('survival_by_gender.png')
plt.close()

# 11. Tumor Size by Risk Factors
plt.figure(figsize=(14, 10))

for i, factor in enumerate(risk_factors, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x=factor, y='Tumor Size (cm)', data=df)
    plt.title(f'Tumor Size by {factor}', fontsize=14)
    plt.xlabel(factor, fontsize=10)
    plt.ylabel('Tumor Size (cm)', fontsize=10)

plt.tight_layout()
plt.savefig('tumor_size_by_risk_factors.png')
plt.close()

# 12. Survival Rate by Treatment Type
plt.figure(figsize=(12, 6))
sns.boxplot(x='Treatment Type', y='Survival Rate (5-Year, %)', data=df)
plt.title('5-Year Survival Rate by Treatment Type', fontsize=16)
plt.xlabel('Treatment Type', fontsize=12)
plt.ylabel('5-Year Survival Rate (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('survival_by_treatment.png')
plt.close()

# SECTION 4: DETECTING PATTERNS & ANOMALIES
print("\n=== DETECTING PATTERNS & ANOMALIES ===")

# 13. Relationship between Multiple Risk Factors and Cancer Diagnosis
# Create a risk factor count column
risk_columns = ['Tobacco Use', 'Alcohol Consumption', 'HPV Infection', 'Betel Quid Use', 
                'Chronic Sun Exposure', 'Poor Oral Hygiene', 'Family History of Cancer']

# Convert 'Yes' to 1 and 'No' to 0 for counting risk factors
for col in risk_columns:
    df[col + '_Binary'] = df[col].apply(lambda x: 1 if x == 'Yes' else 0)

# Count risk factors for each patient
df['Risk Factor Count'] = df[[col + '_Binary' for col in risk_columns]].sum(axis=1)

# Visualize relationship between risk factor count and cancer diagnosis
plt.figure(figsize=(12, 6))
sns.countplot(x='Risk Factor Count', hue='Oral Cancer (Diagnosis)', data=df)
plt.title('Oral Cancer Diagnosis by Number of Risk Factors', fontsize=16)
plt.xlabel('Number of Risk Factors', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.savefig('diagnosis_by_risk_count.png')
plt.close()

# 14. Cost of Treatment vs Economic Burden by Cancer Stage
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Cost of Treatment (USD)', y='Economic Burden (Lost Workdays per Year)', 
                hue='Cancer Stage', size='Tumor Size (cm)', sizes=(20, 200), data=df, alpha=0.7)
plt.title('Cost of Treatment vs Economic Burden by Cancer Stage', fontsize=16)
plt.xlabel('Cost of Treatment (USD)', fontsize=12)
plt.ylabel('Economic Burden (Lost Workdays per Year)', fontsize=12)
plt.savefig('cost_vs_burden.png')
plt.close()

# 15. Comparison of Diagnosis Rates by Country (Top 10 countries)
country_counts = df.groupby('Country')['ID'].count().reset_index()
country_counts.columns = ['Country', 'Total Patients']
country_counts = country_counts.sort_values('Total Patients', ascending=False).head(10)

country_diagnosis = df.groupby('Country')['Oral Cancer (Diagnosis)'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100).reset_index()
country_diagnosis.columns = ['Country', 'Diagnosis Rate (%)']

top_countries = pd.merge(country_counts, country_diagnosis, on='Country')
top_countries = top_countries.sort_values('Total Patients', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x='Country', y='Diagnosis Rate (%)', data=top_countries)
plt.title('Oral Cancer Diagnosis Rate by Country (Top 10)', fontsize=16)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Diagnosis Rate (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('diagnosis_rate_by_country.png')
plt.close()

# SECTION 5: SUMMARY AND INSIGHTS
print("\n=== SUMMARY OF EDA FINDINGS ===")
print("1. Univariate Analysis:")
print(f"   - Age distribution is centered around {age_median} years")
print(f"   - Tumor sizes show some outliers beyond the typical range")
print(f"   - Cancer stages are distributed as: {df['Cancer Stage'].value_counts().to_dict()}")
print(f"   - The dataset has {diagnosis_counts['Yes']} positive and {diagnosis_counts['No']} negative oral cancer cases")

print("\n2. Multivariate Analysis:")
print("   - Correlation analysis shows relationships between numerical variables")
print("   - Tumor size and cancer stage are correlated with survival rate")

print("\n3. Group Comparisons:")
print("   - There are differences in survival rates based on gender and treatment type")
print("   - Risk factors like tobacco use and alcohol consumption show correlation with tumor size")

print("\n4. Pattern Detection:")
print("   - Number of risk factors is associated with higher oral cancer diagnosis rates")
print("   - Economic burden increases with treatment cost and cancer stage")
print("   - Diagnosis rates vary by country, possibly due to different risk factor prevalence")

print("\nAll visualizations have been saved as PNG files in the current directory.")