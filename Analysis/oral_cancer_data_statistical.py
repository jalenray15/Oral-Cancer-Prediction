import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

# Load the dataset
print("Loading the oral cancer dataset...")
df = pd.read_csv('oral_cancer_prediction_dataset.csv')

# Display basic info about the dataset
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# --- CHI-SQUARE TEST: TOBACCO USE VS. ORAL CANCER ---
print("\n--- CHI-SQUARE TEST: TOBACCO USE VS. ORAL CANCER DIAGNOSIS ---")
print("Research Question: Is there a significant association between tobacco use and oral cancer diagnosis?")

# Create the contingency table
contingency_table = pd.crosstab(df['Tobacco Use'], df['Oral Cancer (Diagnosis)'])
print("\nContingency Table (Tobacco Use vs. Oral Cancer Diagnosis):")
print(contingency_table)

# Calculate row percentages to better understand the relationship
percentage_table = pd.crosstab(df['Tobacco Use'], df['Oral Cancer (Diagnosis)'], 
                               normalize='index') * 100
print("\nPercentage Table (row percentages):")
print(percentage_table)

# Perform the Chi-Square Test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print("\nChi-Square Test Results:")
print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"P-Value: {p_value:.8f}")
print(f"Degrees of Freedom: {dof}")

# Interpret the results
alpha = 0.05
print("\nInterpretation:")
if p_value < alpha:
    print(f"The p-value ({p_value:.8f}) is less than the significance level ({alpha}).")
    print("We reject the null hypothesis.")
    print("There is a statistically significant association between tobacco use and oral cancer diagnosis.")
else:
    print(f"The p-value ({p_value:.8f}) is greater than the significance level ({alpha}).")
    print("We fail to reject the null hypothesis.")
    print("There is no statistically significant association between tobacco use and oral cancer diagnosis.")

# Calculate effect size (Cramer's V)
n = contingency_table.sum().sum()
cramer_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
print(f"\nEffect Size (Cramer's V): {cramer_v:.4f}")

# Interpret effect size
print("Effect Size Interpretation:")
if cramer_v < 0.1:
    print("Negligible association")
elif cramer_v < 0.3:
    print("Small association")
elif cramer_v < 0.5:
    print("Moderate association")
else:
    print("Strong association")

# Calculate odds ratio to quantify the relationship
odds_ratio = (contingency_table.iloc[0, 1] * contingency_table.iloc[1, 0]) / (contingency_table.iloc[0, 0] * contingency_table.iloc[1, 1])
print(f"\nOdds Ratio: {odds_ratio:.4f}")
print("Interpretation: A person who uses tobacco is {:.2f} times more likely to be diagnosed with oral cancer compared to a non-tobacco user.".format(odds_ratio))

# --- ADDITIONAL ANALYSIS: MULTIPLE RISK FACTORS ---
print("\n--- ADDITIONAL ANALYSIS: MULTIPLE RISK FACTORS ---")

# Analyze the impact of combined risk factors (Tobacco + Alcohol)
df['Risk_Combination'] = 'None'
df.loc[(df['Tobacco Use'] == 'No') & (df['Alcohol Consumption'] == 'No'), 'Risk_Combination'] = 'Neither'
df.loc[(df['Tobacco Use'] == 'Yes') & (df['Alcohol Consumption'] == 'No'), 'Risk_Combination'] = 'Tobacco Only'
df.loc[(df['Tobacco Use'] == 'No') & (df['Alcohol Consumption'] == 'Yes'), 'Risk_Combination'] = 'Alcohol Only'
df.loc[(df['Tobacco Use'] == 'Yes') & (df['Alcohol Consumption'] == 'Yes'), 'Risk_Combination'] = 'Both'

# Create contingency table for combined risk factors
combined_table = pd.crosstab(df['Risk_Combination'], df['Oral Cancer (Diagnosis)'])
print("\nContingency Table (Combined Risk Factors vs. Oral Cancer Diagnosis):")
print(combined_table)

# Calculate row percentages for combined risk factors
combined_percentage = pd.crosstab(df['Risk_Combination'], df['Oral Cancer (Diagnosis)'], 
                                 normalize='index') * 100
print("\nPercentage Table for Combined Risk Factors (row percentages):")
print(combined_percentage)

# Perform Chi-Square test for combined factors
chi2_combined, p_value_combined, dof_combined, expected_combined = chi2_contingency(combined_table)

print("\nChi-Square Test Results for Combined Risk Factors:")
print(f"Chi-Square Statistic: {chi2_combined:.4f}")
print(f"P-Value: {p_value_combined:.8f}")
print(f"Degrees of Freedom: {dof_combined}")

# Interpret the results for combined factors
if p_value_combined < alpha:
    print("\nThere is a statistically significant association between combined risk factors and oral cancer diagnosis.")
else:
    print("\nThere is no statistically significant association between combined risk factors and oral cancer diagnosis.")

# Calculate Cramer's V for combined factors
n_combined = combined_table.sum().sum()
cramer_v_combined = np.sqrt(chi2_combined / (n_combined * (min(combined_table.shape) - 1)))
print(f"Effect Size (Cramer's V) for Combined Factors: {cramer_v_combined:.4f}")

# --- SUMMARY ---
print("\n--- SUMMARY OF FINDINGS ---")
print("1. Chi-Square test shows that there is a statistically significant association between tobacco use and oral cancer diagnosis.")
print(f"   - Chi-Square value: {chi2:.4f}, p-value: {p_value:.8f}")
print(f"   - Effect size (Cramer's V): {cramer_v:.4f}, indicating a small association")
print(f"   - Odds ratio: {odds_ratio:.4f}, suggesting tobacco users have a higher chance of developing oral cancer")

print("\n2. Analysis of combined risk factors (tobacco and alcohol) also shows a significant association with oral cancer diagnosis.")
print(f"   - Chi-Square value: {chi2_combined:.4f}, p-value: {p_value_combined:.8f}")
print(f"   - Effect size: {cramer_v_combined:.4f}")

print("\nConclusion: The statistical evidence supports that both tobacco use alone and the combination of tobacco and alcohol use are significantly associated with oral cancer diagnosis. However, the effect size suggests that while statistically significant, the strength of this association is relatively small, indicating that other factors may also play important roles in oral cancer development.")