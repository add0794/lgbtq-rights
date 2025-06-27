import pandas as pd
import streamlit as st
import plotly.express as px

# Read the datasets
df = pd.read_csv('lgbtq_rights_by_country.csv')
democracy_df = pd.read_csv('democracy_index.csv')

# Join the datasets on country name
merged_df = pd.merge(df, democracy_df, left_on='Territory', right_on='Country', how='inner')

# Update the main DataFrame to use the merged data
df = merged_df

# Set page configuration
st.set_page_config(page_title="LGBTQ Rights in Pride Month 2025", layout="wide")

# Add title and description
st.title("LGBTQ Rights in 2025")
st.write("""
Pride Month is a time to honor the resilience, visibility, and progress of queer communities around the world. Over the past few decades, LGBTQ+ people have achieved significant legal and cultural milestones, especially in many Western countries, where same-sex marriage, civil unions, and adoption rights are now widely recognized. However, this progress is far from universal. In much of the Global South and in many non-Western countries, same-sex relationships remain criminalized, legal protections are minimal or nonexistent, and queer individuals often face widespread social stigma, violence, and state repression. These disparities create hostile conditions for both travel and daily life for queer people globally.

As Pride comes to a close, I’ve analyzed global LGBTQ+ rights, tracking legal recognition, civil protections, and societal acceptance across regions. It highlights where progress has been made and where urgent action is still needed, emphasizing that Pride is not only a celebration, but also a call to action for global equity and human rights.

Feel free to give feedback!

Data can be found [here](https://www.kaggle.com/datasets/wilomentena/lgbt-rights-worldwide/data).
""")

# Analyze each column
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
        with st.expander(f"{col}"):
            st.subheader(col)
            # Column descriptions and analysis
            if col == "Recognition of same-sex unions":
                st.write("Indicates whether a country legally recognizes same-sex unions, such as civil partnerships or domestic partnerships. This is distinct from marriage, but still grants some or many of the legal benefits associated with marriage, such as inheritance rights, hospital visitation, and tax benefits.")
            if col == "Same-sex marriage":
                st.write("Indicates whether same-sex marriage is legally recognized, granting full marital rights equal to those of heterosexual couples. This includes not only civil benefits but also symbolic recognition of equality under the law. As of now, less than one-third of countries allow full same-sex marriage.")
            if col == "Adoption by same-sex couples":
                st.write("Indicates whether same-sex couples are legally allowed to adopt children. This includes joint adoption as well as second-parent or stepchild adoption. Legal barriers in many countries still prevent same-sex couples from building families with full parental rights.")
            if col == "LGBT people allowed to serve openly in military?":
                st.write("Indicates whether LGBTQ+ individuals are permitted to serve openly in the national armed forces without risk of expulsion, harassment, or forced concealment. In some countries, LGBTQ+ people are barred entirely; in others, they may serve but must hide their identity.")
            if col == "Anti-discrimination laws concerning sexual orientation":
                st.write("Indicates whether a country has national laws that protect individuals from discrimination based on sexual orientation in key areas such as employment, housing, education, and access to services. These laws are essential for protecting the dignity and safety of LGBTQ+ people.")
            if col == "Anti-discrimination laws concerning gender identity":
                st.write("Indicates whether a country has national laws protecting against discrimination based on gender identity. These laws are crucial for safeguarding the rights of transgender and gender nonconforming individuals in areas such as employment, healthcare, education, and housing.")
            
            # Basic statistics and analysis
            st.write("Unique values:", df[col].nunique())
            st.write("Value counts with percentages:")
            value_counts = df[col].value_counts()
            total = value_counts.sum()
            
            # Create a DataFrame to display with percentages
            display_df = pd.DataFrame({
                'Value': value_counts.index,
                'Count': value_counts.values.astype(str),
                'Percentage': [f"{(x/total*100):.1f}%" for x in value_counts.values]
            })
            display_df['Count'] = display_df['Count'].str.ljust(3)  # Left-justify count values
            st.table(display_df)
            
            # Create bar chart
            if col != 'Territory':  # Skip territory for bar chart
                fig = px.bar(
                    value_counts,
                    title=f'Count of {col}',
                    labels={'index': 'Value', 'value': 'Count'}
                )
                st.plotly_chart(fig, key=f'bar_chart_{col}')
                
            # Map visualization for territory-based columns
            if col != 'Territory':
                fig = px.choropleth(
                    df,
                    locations="Territory",
                    locationmode="country names",
                    color=col,
                    title=f"{col} by Country",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, key=f'map_chart_{col}')

# Display countries with unknown data
with st.expander("Countries with Unknown Data"):
    
    # Create dictionary to store unknown data
    unknown_data_dict = {}
    
    # Process unknown data
    for _, row in df.iterrows():
        country = row['Territory']
        unknown_rights = [col for col in df.columns if row[col] == 'Unknown']
        if unknown_rights:
            unknown_data_dict[country] = unknown_rights
    
    # Display number of countries with unknown data
    num_countries_with_unknown = len(unknown_data_dict)

    st.write(f"The following countries have unknown data for some rights: {num_countries_with_unknown}")
    # Display unknown data dictionary
    st.write(unknown_data_dict)

    # Add choropleth map of unknown data distribution
    st.subheader("Distribution of Unknown Data")
    df['Unknown Rights'] = df.apply(lambda row: sum(row == 'Unknown'), axis=1)
    fig = px.choropleth(
        df,
        locations="Territory",
        locationmode="country names",
        color="Unknown Rights",
        title="Most countries have known data for LGBTQ+ rights",  
        color_continuous_scale="Viridis",
        hover_data=['Territory', 'Unknown Rights']
    )
    st.plotly_chart(fig)