import pandas as pd

def calculate_compliance_score(row):
    required_docs = [
        'Aadhaar_Submitted',
        'PAN_Submitted',
        'Bank_Details_Updated',
        'NDA_Signed',
        'Offer_Letter_Submitted',
        'Tax_Form_Submitted'
    ]
    total = len(required_docs)
    filled = sum([row.get(col, 'No') == 'Yes' for col in required_docs])
    return round((filled / total) * 100, 2)

def audit_employee_data(df):
    expected_cols = [
        'Employee_ID', 'Employee_Name',
        'Aadhaar_Submitted', 'PAN_Submitted',
        'Bank_Details_Updated', 'NDA_Signed',
        'Offer_Letter_Submitted', 'Tax_Form_Submitted',
        'Joining_Date', 'Department'
    ]
    
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"❌ Missing expected column(s): {', '.join(missing_cols)}")

    df['Compliance_Score (%)'] = df.apply(calculate_compliance_score, axis=1)
    return df
