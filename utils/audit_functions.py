import pandas as pd

def calculate_compliance_score(row):
    total_fields = 4  # Aadhaar, PAN, Offer Letter, Tax Form
    filled = sum([row['Aadhaar_Submitted'] == 'Yes',
                  row['PAN_Submitted'] == 'Yes',
                  row['Offer_Letter_Submitted'] == 'Yes',
                  row['Tax_Form_Submitted'] == 'Yes'])
    return round((filled / total_fields) * 100, 2)

def audit_employee_data(df):
    df['Compliance_Score (%)'] = df.apply(calculate_compliance_score, axis=1)
    df['Status'] = df['Compliance_Score (%)'].apply(lambda x: 'Compliant' if x == 100 else 'Non-Compliant')
    return df

def department_summary(df):
    summary = df.groupby('Department')['Compliance_Score (%)'].mean().reset_index()
    summary.rename(columns={'Compliance_Score (%)': 'Avg_Department_Score'}, inplace=True)
    return summary
