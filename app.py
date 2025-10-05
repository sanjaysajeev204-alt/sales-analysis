import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# --- Header ---
st.title("📊 Sales Performance Dashboard")
st.markdown("### Minimalistic & Professional Analytics View")

# --- File Upload ---
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# --- Load Data ---
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, parse_dates=["Date"], dayfirst=True)
    df = df.sort_values("Date")  # Sort by Date ascending
    return df

# --- Handle Uploaded or Default Data ---
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    st.sidebar.info("Using default sample data (data.csv).")
    df = pd.read_csv("data.csv", parse_dates=["Date"])
    df = df.sort_values("Date")

# --- KPIs ---
total_sales = df['Sales'].sum()
total_orders = df['Orders'].sum()
total_profit = df['Profit'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📦 Total Orders", f"{total_orders}")
col3.metric("💹 Total Profit", f"₹{total_profit:,.0f}")

st.markdown("---")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
region = st.sidebar.multiselect("Select Region:", df["Region"].unique())
category = st.sidebar.multiselect("Select Category:", df["Category"].unique())

filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

# --- Graphs ---
tab1, tab2 = st.tabs(["📈 Sales Trend", "🏷️ Sales by Category"])

with tab1:
    trend_fig = px.line(filtered_df, x="Date", y="Sales", title="Sales Over Time", markers=True)
    trend_fig.update_layout(yaxis_tickprefix="₹")
    st.plotly_chart(trend_fig, use_container_width=True)

with tab2:
    cat_fig = px.bar(filtered_df, x="Category", y="Sales", color="Category", title="Sales by Category")
    cat_fig.update_layout(yaxis_tickprefix="₹")
    st.plotly_chart(cat_fig, use_container_width=True)

# --- Data Preview ---
st.markdown("### 📄 Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

# --- Download Button ---
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv'
)

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | © 2025 Sanjay Dashboard")
