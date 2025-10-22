import streamlit as st
import pandas as pd
import plotly.express as px
from utils.audit_functions import audit_employee_data, department_summary

st.set_page_config(page_title="HR Data Compliance & Audit Tracker", layout="wide")

st.title("🧾 HR Data Compliance & Audit Tracker")
st.write("Easily audit employee compliance documents and visualize organization-wide HR readiness.")

# --- File Upload ---
st.sidebar.header("Upload Employee Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("Using sample dataset from /data folder.")
    df = pd.read_csv("data/employee_records.csv")

# --- Audit Employee Data ---
audited_df = audit_employee_data(df)
dept_summary = department_summary(audited_df)

st.subheader("📋 Employee Compliance Report")
st.dataframe(audited_df, use_container_width=True)

# --- Stats ---
col1, col2, col3 = st.columns(3)
with col1:
    total = len(audited_df)
    st.metric("Total Employees", total)
with col2:
    compliant = (audited_df['Status'] == 'Compliant').sum()
    st.metric("Compliant Employees", compliant)
with col3:
    st.metric("Compliance Rate (%)", round((compliant / total) * 100, 2))

# --- Department-Level Chart ---
st.subheader("🏢 Department-wise Compliance Overview")
fig = px.bar(dept_summary, x='Department', y='Avg_Department_Score', color='Avg_Department_Score',
             color_continuous_scale='Blues', title='Average Compliance by Department')
st.plotly_chart(fig, use_container_width=True)

# --- Non-Compliant Employees ---
st.subheader("⚠️ Non-Compliant Employees")
non_compliant = audited_df[audited_df['Status'] == 'Non-Compliant']
if len(non_compliant) > 0:
    st.dataframe(non_compliant, use_container_width=True)
else:
    st.success("✅ All employees are fully compliant!")

# --- Download Report ---
st.subheader("📤 Download Audited Report")
csv = audited_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV Report", csv, "audited_compliance_report.csv", "text/csv")
