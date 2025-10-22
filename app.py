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

# Pie chart - Department-wise Compliance Share
pie = px.pie(
    audited_df,
    names='Department',
    values='Compliance_Score (%)',
    title='Department-wise Compliance Share'
)
st.plotly_chart(pie, use_container_width=True)

# Bar chart - Average Compliance by Department
bar = px.bar(
    audited_df.groupby("Department")["Compliance_Score (%)"].mean().reset_index(),
    x="Department",
    y="Compliance_Score (%)",
    color="Department",
    title="Average Compliance by Department"
)
st.plotly_chart(bar, use_container_width=True)

# ------------------------------------------------
# 📋 Data Table
st.subheader("📋 Employee Compliance Details")
st.dataframe(
    audited_df.style.background_gradient(subset=["Compliance_Score (%)"], cmap="RdYlGn"),
    use_container_width=True
)

# ------------------------------------------------
# 💡 Insights
st.subheader("💡 Compliance Insights")
avg_score = audited_df["Compliance_Score (%)"].mean()
if avg_score < 80:
    st.warning("⚠️ Overall compliance is below optimal levels. Please review incomplete document submissions.")
else:
    st.success("✅ Great job! Most employees are compliant with documentation requirements.")

# ------------------------------------------------
# 🧾 Footer
st.markdown("---")
st.markdown(
    "<center>Developed by <b>Byreddy Sai Reddy</b> | HR Data Compliance & Audit Tracker © 2025</center>",
    unsafe_allow_html=True,
)
