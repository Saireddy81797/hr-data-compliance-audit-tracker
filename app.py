import streamlit as st
import pandas as pd
import plotly.express as px
from utils.audit_functions import audit_employee_data

# --- Page Config ---
st.set_page_config(
    page_title="HR Data Compliance & Audit Tracker",
    page_icon="🧾",
    layout="wide"
)

# --- App Header ---
st.title("🧾 HR Data Compliance & Audit Tracker")
st.caption("Analyze and visualize employee document compliance across departments in real time.")

st.markdown("---")

# --- Upload Section ---
st.sidebar.header("📂 Upload Employee Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"], help="Upload HR employee record CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/employee_records.csv")
    st.sidebar.info("Using sample data (employee_records.csv)")

# --- Process Data ---
try:
    audited_df = audit_employee_data(df)

    # --- KPIs ---
    avg_score = audited_df["Compliance_Score (%)"].mean()
    fully_compliant = (audited_df["Compliance_Score (%)"] == 100).sum()
    total_emp = len(audited_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Average Compliance", f"{avg_score:.2f}%")
    col2.metric("✅ Fully Compliant Employees", f"{fully_compliant}/{total_emp}")
    col3.metric("👥 Total Employees", total_emp)

    st.markdown("---")

    # --- Charts ---
    col1, col2 = st.columns(2)

    with col1:
        pie = px.pie(
            audited_df,
            names="Department",
            values="Compliance_Score (%)",
            title="Department-wise Compliance Share"
        )
        st.plotly_chart(pie, use_container_width=True)

    with col2:
        bar = px.bar(
            audited_df,
            x="Employee_Name",
            y="Compliance_Score (%)",
            color="Department",
            title="Individual Compliance Scores",
            hover_data=["Department"],
            height=450
        )
        st.plotly_chart(bar, use_container_width=True)

    st.markdown("---")

    # --- Data Table ---
    st.subheader("📋 Employee Compliance Details")
    st.dataframe(
        audited_df.style.background_gradient(subset=["Compliance_Score (%)"], cmap="RdYlGn"),
        use_container_width=True
    )

except KeyError as e:
    st.error(str(e))
except Exception as e:
    st.error("⚠️ Unexpected error while processing data.")
    st.exception(e)
