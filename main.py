import pandas as pd
import streamlit as st
import plotly.express as px

# Read the dataset directly from the CSV file
df = pd.read_csv('lgbtq_rights_by_country.csv')

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

# Create visualizations

for col in columns:
    if col == 'Territory' or col == 'Same-sex sexual activity':
        continue
    else:
        with st.expander(f"Analysis of {col}"):
            st.subheader(col)
            
            # Basic statistics
            st.write("Unique values:", df[col].nunique())
            st.write("Value counts with percentages:")
            value_counts = df[col].value_counts()
            total = value_counts.sum()
            value_counts_with_percent = value_counts.apply(lambda x: f"{x} ({(x/total*100):.1f}%)")
            
            # Create a DataFrame to display with percentages
            display_df = pd.DataFrame({
                'Value': value_counts.index,
                'Count': value_counts.values,
                'Percentage': [f"{(x/total*100):.1f}%" for x in value_counts.values]
            })
            st.dataframe(display_df)
        
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

