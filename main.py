import pandas as pd
import streamlit as st

# Read the dataset directly from the CSV file
df = pd.read_csv('/Users/alexdubro/.cache/kagglehub/datasets/wilomentena/lgbt-rights-worldwide/versions/2/lgbtq_rights_by_country.csv')

# Set page configuration
st.set_page_config(page_title="LGBTQ Rights Analysis", layout="wide")

# Add title and description
st.title("LGBTQ Rights Analysis")
st.write("""
This analysis explores the LGBTQ rights dataset across different countries.
Each section analyzes a specific aspect of LGBTQ rights.
""")

# Create tabs for each analysis
with st.expander("Dataset Overview"):
    st.write("Number of countries:", len(df['Territory'].unique()))
    st.write("Countries (Descending Order):")
    st.write(df['Territory'].sort_values(ascending=True).unique())
    st.write("Columns:", df.columns.tolist())
    
# Analyze each column
columns = df.columns

for col in columns:
    if col == 'Territory':
        continue
    else:
        with st.expander(f"Analysis of {col}"):
            st.subheader(col)
            
            # Basic statistics
            st.write("Unique values:", df[col].nunique())
            st.write("Value counts:")
            value_counts = df[col].value_counts()
            st.write(value_counts)
        
            # Create bar chart
            if col != 'Territory':  # Skip territory for bar chart
                fig = px.bar(
                    value_counts,
                    title=f'Distribution of {col}',
                    labels={'index': 'Value', 'value': 'Count'}
                )
                st.plotly_chart(fig)
                
            # Map visualization for territory-based columns
            if col != 'Territory':
                st.write("Map visualization:")
                # Create a map using plotly
                fig = px.choropleth(
                    df,
                    locations="Territory",
                    locationmode="country names",
                    color=col,
                    title=f"{col} by Country",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig)

