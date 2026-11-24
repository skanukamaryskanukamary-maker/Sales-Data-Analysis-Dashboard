import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Data Analysis Dashboard")

# Load data
df = pd.read_csv("sales.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Region filter
regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.selectbox("Select a region", regions)

if selected_region != "All":
    df = df[df["Region"] == selected_region]

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['Revenue'].sum():,.2f}")
col2.metric("Number of Orders", f"{len(df):,}")
col3.metric("Units Sold", f"{df['Quantity'].sum():,}")

# Monthly revenue chart
monthly_sales = (
    df.set_index("OrderDate")
      .resample("ME")["Revenue"]
      .sum()
      .reset_index()
)

st.subheader("Monthly Revenue")
fig = px.line(
    monthly_sales,
    x="OrderDate",
    y="Revenue",
    markers=True,
    title="Revenue by Month",
)
st.plotly_chart(fig, use_container_width=True)

# Revenue by product
product_sales = (
    df.groupby("Product", as_index=False)["Revenue"]
      .sum()
      .sort_values("Revenue", ascending=False)
)

st.subheader("Revenue by Product")
fig = px.bar(product_sales, x="Product", y="Revenue", color="Product")
st.plotly_chart(fig, use_container_width=True)

# Show the filtered data
st.subheader("Sales Records")
st.dataframe(df, use_container_width=True)