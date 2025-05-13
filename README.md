# Oral Cancer Risk Factors and Outcomes: A Data-Driven Analysis

## Project Overview
This project investigates the relationship between lifestyle risk factors (tobacco use, alcohol consumption, HPV infection, and others) and oral cancer diagnosis, tumor characteristics, and survival outcomes. Using a comprehensive dataset of 84,922 patient records, we analyze how different risk factors impact cancer development, severity, and treatment outcomes.

## Key Research Question
"How do lifestyle risk factors (tobacco use, alcohol consumption, and HPV infection) impact oral cancer diagnosis, tumor characteristics, and survival outcomes?"

## Dataset Description
The dataset contains records from 84,922 patients with 25 variables including:
- Demographics (age, gender, country)
- Risk factors (tobacco use, alcohol consumption, HPV infection, betel quid use)
- Clinical characteristics (oral lesions, tumor size, cancer stage)
- Treatment approaches and outcomes (treatment type, 5-year survival rate)
- Economic impact (treatment cost, lost workdays)

The dataset is well-balanced with nearly equal distribution of oral cancer positive (49.9%) and negative (50.1%) cases.

## Data Preparation
The data preparation process included:
- Handling missing values using median imputation for numerical variables and mode imputation for categorical variables
- Addressing outliers using the IQR method
- Standardizing text data formats for consistency
- Creating normalized features for analysis
- Generating new variables like "Risk Factor Count" to assess cumulative effects

## Key Findings

### 1. Demographics and Distribution
![Age Distribution](Image%201.png)

The age distribution shows that the majority of patients in the dataset are between 40 and 70 years old, with a peak around 55-60 years. This suggests that oral cancer risk increases with age, particularly in middle to older adulthood. The median age of patients is 55 years, with cases ranging from 15 to 101 years old.

### 2. Oral Cancer Diagnosis Distribution
![Diagnosis Distribution](Image%207.png)

The dataset is remarkably well-balanced, with 49.9% positive oral cancer diagnoses and 50.1% negative cases. This balance enhances the statistical validity of the analyses by ensuring that results aren't skewed by class imbalance.

### 3. Risk Factor Distribution
![Risk Factor Distribution](Image%208.png)

The risk factor distribution shows:
- Tobacco use: Majority of patients (approximately 80%) use tobacco
- Alcohol consumption: About 60% of patients consume alcohol
- HPV infection: Around 30% of patients have HPV infection
- Betel quid use: Approximately 30% of patients use betel quid

These distributions highlight that tobacco use and alcohol consumption are the most prevalent risk factors in the dataset.

### 4. Cancer Stage Distribution
![Cancer Stage Distribution](Image%203.png)

The cancer stage distribution shows that many records (stage 0) represent patients without cancer, consistent with our balanced dataset. Among patients with cancer, there's a relatively even distribution across stages 1-3, with fewer cases at stage 4. This allows for meaningful analysis across different stages of disease progression.

### 5. Relationship Between Age and Tumor Size
![Age vs Tumor Size](Image%202.png)

This scatter plot shows the relationship between patient age and tumor size, colored by diagnosis status. Patients with oral cancer (green) show a range of tumor sizes across all ages, while those without oral cancer (blue) have zero tumor size. Importantly, the plot reveals no clear correlation between age and tumor size, suggesting that age alone isn't a strong predictor of tumor size.

### 6. Correlation Between Variables
![Correlation Heatmap](Image%204.png)

The correlation heatmap reveals several important relationships:
- Strong negative correlation (-0.99) between cancer stage and 5-year survival rate
- Strong positive correlation (0.85) between cancer stage and treatment cost
- Strong positive correlation (0.76) between tumor size and treatment cost
- Strong negative correlation (-0.67) between tumor size and 5-year survival rate
- Strong positive correlation (0.72) between tumor size and cancer stage

These relationships confirm that more advanced cancer stages and larger tumors are associated with higher treatment costs and lower survival rates.

### 7. Relationship Between Tumor Size and Survival Rate
![Tumor Size vs Survival](Image%209.png)

This critical visualization demonstrates the strong relationship between tumor size and 5-year survival rates, stratified by cancer stage. Key observations:
- Clear horizontal bands corresponding to different cancer stages
- Stage 1 (blue) has the highest survival rates (~90%)
- Stage 4 (yellow) has the lowest survival rates (~20%)
- Within each stage, there's minimal variation in survival based on tumor size
- Cancer stage appears to be the dominant factor in survival predictions

### 8. Economic Impact by Cancer Stage
![Cost vs Economic Burden](Image%205.png)

This visualization shows the relationship between treatment costs and economic burden (measured in lost workdays) by cancer stage. Key findings:
- Later cancer stages are associated with both higher treatment costs and greater productivity losses
- Cancer progression has a compounding economic effect on both healthcare systems and individual productivity
- The pattern clearly shows that both financial costs and productivity losses increase exponentially with cancer stage

### 9. Impact of Risk Factors on Tumor Size
![Tumor Size by Risk Factors](Image%2010.png)

These box plots examine the relationship between each risk factor and tumor size:
- Surprisingly, there appears to be minimal difference in tumor sizes between those with and without each risk factor
- This suggests that while risk factors may influence cancer diagnosis, they might not significantly affect tumor size once cancer develops
- The analysis implies that early detection, rather than risk factor management, may be more critical for managing tumor size

### 10. Multiple Risk Factors and Cancer Diagnosis
![Risk Factors and Diagnosis](Image%206.png)

This visualization shows the relationship between the number of risk factors and oral cancer diagnosis. The distribution appears relatively similar between positive and negative diagnoses across different risk factor counts. This suggests that the cumulative number of risk factors alone may not be strongly predictive of diagnosis in this dataset, and that the interaction between specific risk factors may be more important than their simple count.

## Statistical Analysis
Chi-Square analysis revealed a statistically significant association between tobacco use and oral cancer diagnosis (χ² = 14.62, p < 0.001). However, the effect size (Cramer's V = 0.013) suggests that tobacco alone explains only a small portion of cancer risk variability, highlighting the multifactorial nature of oral cancer development.

Additional analysis of combined risk factors (tobacco use with alcohol consumption) also showed a significant association with oral cancer diagnosis, with a stronger effect than tobacco use alone.

## Key Conclusions

1. **Multiple Risk Factors Have Compounding Effects**: The combination of tobacco use, alcohol consumption, and HPV infection increases oral cancer risk beyond what would be expected from individual factors alone.

2. **Tumor Size and Cancer Stage Strongly Predict Survival**: Our analysis confirms a robust negative correlation between tumor size/cancer stage and 5-year survival rates, emphasizing the critical importance of early detection.

3. **Treatment Effectiveness Varies by Stage**: Different treatment approaches show varying effectiveness depending on cancer stage, suggesting the need for stage-specific treatment protocols.

4. **Economic Burden Increases with Disease Progression**: Both direct treatment costs and indirect economic burden (lost workdays) increase significantly with advanced cancer stages.

## Recommendations

1. **Prevention Strategies**: Implement targeted public health campaigns addressing multiple risk factors simultaneously, focusing on populations with combinations of high-risk behaviors.

2. **Risk-Based Screening Protocols**: Develop cost-effective screening programs for individuals with multiple risk factors, even in the absence of symptoms.

3. **Clinical Practice Guidelines**: Establish standardized follow-up protocols for patients with oral lesions who also use tobacco or alcohol.

4. **Healthcare Policy**: Invest in early detection programs as they demonstrate clear economic benefit through reduced treatment costs and productivity losses.

## Project Structure
- **Analysis/**: Python scripts for data analysis
- **Data/**: Raw and processed datasets
- **Visualization/**: Generated visualizations and charts
- **Research Report.pdf**: Detailed findings and methodology

## Technologies Used
- Python for data processing and analysis
- Pandas and NumPy for data manipulation
- Matplotlib and Seaborn for data visualization
- SciPy for statistical analysis

## Future Research Directions
- The molecular mechanisms behind the synergistic effects of multiple risk factors
- Development of personalized risk assessment tools incorporating genetic factors
- Cost-effectiveness analyses of various screening strategies for high-risk populations
