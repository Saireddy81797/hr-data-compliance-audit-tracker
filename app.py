import streamlit as st
import pandas as pd
import plotly.express as px
from utils.audit_functions import audit_employee_data

# ------------------------------------------------
# 🌐 Page setup
st.set_page_config(page_title="HR Data Compliance Tracker 🗄️", page_icon="🧾", layout="wide")

st.title("🧾 HR Data Compliance & Audit Tracker")
st.markdown("#### Track and analyze employee document compliance across departments in real time.")

# ------------------------------------------------
# 📂 Upload or load default data
st.sidebar.header("📁 Upload Employee Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("No file uploaded. Loading sample data...")
    df = pd.read_csv("data/employee_records.csv")

# ------------------------------------------------
# 🧮 Audit employee compliance
try:
    audited_df = audit_employee_data(df)
except KeyError as e:
    st.error(f"❌ Missing expected column: {e}")
    st.stop()

# ------------------------------------------------
# 🎯 Sidebar filters
st.sidebar.header("🔍 Filters")
selected_dept = st.sidebar.selectbox("Filter by Department", ["All"] + sorted(audited_df["Department"].unique()))
if selected_dept != "All":
    audited_df = audited_df[audited_df["Department"] == selected_dept]

show_only_noncompliant = st.sidebar.checkbox("Show Only Non-Compliant Employees")
if show_only_noncompliant:
    audited_df = audited_df[audited_df["Compliance_Score (%)"] < 100]

# ------------------------------------------------
# 📊 Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Employees", len(audited_df))
col2.metric("📈 Avg Compliance (%)", round(audited_df["Compliance_Score (%)"].mean(), 1))
col3.metric("✅ Fully Compliant", (audited_df["Compliance_Score (%)"] == 100).sum())
col4.metric("⚠️ Non-Compliant", (audited_df["Compliance_Score (%)"] < 100).sum())

st.markdown("---")

# ------------------------------------------------
# 📈 Charts
pie = px.pie(audited_df, names='Department', values='Compliance_Score (%)', title='Department-wise Compliance Shar
