import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.stats import ttest_ind

# Read datasets
df = pd.read_csv('lgbtq_rights_by_country.csv')

# Add title and description
st.title("LGBTQ+ Rights in 2025: A Global Snapshot")
st.write("""
Pride Month serves not only as a celebration of resilience, visibility, and identity, but also as a moment to reflect on the global state of LGBTQ+ rights. In recent decades, queer communities—particularly in Western democracies—have made notable legal and cultural advances, including the legalization of same-sex marriage, civil unions, and adoption rights. However, these gains are not evenly distributed. Across much of the Global South and many non-Western regions, same-sex relationships remain criminalized, legal protections are weak or absent, and queer individuals continue to face systemic discrimination, violence, and state-sponsored repression.

To assess the current landscape, I conducted an analysis of LGBTQ+ rights worldwide using publicly available datasets. This work highlights the stark disparities between regions and underscores the need for continued advocacy and policy change.

#### Methodology and Indicators Analyzed
The dataset includes country-level data on:
- Legal recognition of same-sex unions and marriages
- Adoption rights for same-sex couples
- Military service eligibility for LGBTQ+ individuals
- Anti-discrimination protections based on sexual orientation and gender identity
- Democracy scores, used to explore correlations with legal protections

#### Key Insights
- Western democracies are leading in rights recognition, with widespread legalization of same-sex marriage and joint adoption.
- Countries in the Global South continue to lag behind, with many still criminalizing same-sex activity and offering little to no legal protection.
- A strong positive correlation was found between a country's democracy score and its level of LGBTQ+ rights recognition. Countries with higher democratic indices are significantly more likely to uphold protections and recognition for queer individuals.
- Progress is not linear: While some countries are advancing rapidly, others are experiencing legal and social regression in LGBTQ+ rights.

#### Conclusion
The findings make clear that while important strides have been made, global equity for LGBTQ+ people remains far from achieved. As Pride Month concludes, this analysis reaffirms that Pride must remain both a celebration and a call to action—for universal dignity, safety, and equality.

Data sources: [Kaggle](https://www.kaggle.com/datasets/wilomentena/lgbt-rights-worldwide/data) and [World Population Review](https://worldpopulationreview.com/country-rankings/democracy-index-by-country).
""")

# Dataset Overview
with st.expander("Dataset Overview"):
    st.write("Number of countries:", len(df['Territory'].unique()))
    st.write("Countries (Descending Order):")
    st.write(df['Territory'].sort_values(ascending=True).unique())
    st.write("Columns:", df.columns.tolist())


# Display countries with unknown data
with st.expander("Countries with Unknown Data"):
    
    # Create dictionary to store unknown data
    unknown_data_dict = {}
    
    # Process unknown data
    for _, row in df.iterrows():
        country = row['Territory']
        unknown_rights = [column for column in df.columns if row[column] == 'Unknown']
        if unknown_rights:
            unknown_data_dict[country] = unknown_rights
    
    # Display number of countries with unknown data
    num_countries_with_unknown = len(unknown_data_dict)

    st.write(f"The following countries have unknown data for some rights: {num_countries_with_unknown}")
    # Display unknown data dictionary
    st.write(unknown_data_dict)

    # Add choropleth map of unknown data distribution
    st.subheader("Distribution of Unknown Data")
    df['Rights with Unknown Data'] = df.apply(lambda row: sum(row == 'Unknown'), axis=1)
    fig = px.choropleth(
        df,
        locations="Territory",
        locationmode="country names",
        color="Rights with Unknown Data",
        title="Most countries have known data for LGBTQ+ rights",  
        color_continuous_scale="Viridis",
        hover_data=['Territory', 'Rights with Unknown Data']
    )
    st.plotly_chart(fig, key='unknown_rights_map')

# Analyze each column

# Country-Level Highlights
with st.expander("🌍 Country-Level Highlights"):
    # Create tabs for different categories
    tab_titles = ["✅ Countries Where LGBTQ+ Rights Have Improved", "❌ Countries Where LGBTQ+ Rights Have Regressed", "Conclusion"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        st.markdown("""
        **1. Estonia**  
        • In June 2023, Estonia became the **first former Soviet country** to legalize same-sex marriage and joint adoption, effective **January 1, 2024**.  
        • Estonia also recognizes legal gender changes without surgery and has broad anti-discrimination laws in place.  
        🔗 [Source](https://en.wikipedia.org/wiki/LGBT_rights_in_Estonia)

        **2. Greece**  
        • In **February 2024**, Greece became the **first Orthodox-majority country** to legalize same-sex marriage via parliamentary vote.  
        • In **May 2025**, the Greek Supreme Court upheld same-sex marriage and **joint adoption** as constitutional.  
        🔗 [Source](https://en.wikipedia.org/wiki/LGBT_rights_in_Greece)

        **3. Thailand**  
        • In **late 2024**, Thailand passed the **Marriage Equality Act**, with full implementation in **January 2025**.  
        • Same-sex couples now enjoy full marriage and adoption rights—the first such move in Southeast Asia.  
        🔗 [The Times](https://www.thetimes.co.uk/article/hundreds-same-sex-couples-marry-thailand-changes-law-6hqhqwbv3)
        """)

    with tabs[1]:
        st.markdown("""
        **1. Hungary**  
        • In **2025**, Hungary banned the **Budapest Pride march** and passed new laws restricting LGBTQ+ content for minors, blocking gender marker changes, and limiting adoption by same-sex couples.  
        • These changes have been widely criticized by EU officials and human rights groups.  
        🔗 [Reuters – Pride Ban](https://www.reuters.com/world/hungarys-pm-orban-warns-legal-consequences-over-banned-budapest-pride-march-2025-06-27/)  
        🔗 [Reuters – LGBTQ laws](https://www.reuters.com/world/hungarys-lgbtq-community-reels-under-orbans-laws-pride-ban-2025-06-26/)

        **2. United Kingdom**  
        • In **April 2025**, the UK’s highest court ruled that the legal definition of "woman" refers solely to biological sex under the Equality Act.  
        • This ruling weakens legal protections for transgender women, especially in cases of employment and housing discrimination.  
        🔗 [Feminist.org](https://feminist.org/news/united-kingdom-ruling-highlights-global-rollback-of-trans-rights/)

        **3. United States**  
        • In **June 2025**, the US Supreme Court ruled in favor of parents opting their children out of **LGBTQ-inclusive school curricula**, citing religious liberty.  
        • Multiple states have continued to pass laws restricting access to **gender-affirming care** for minors.  
        🔗 [Time – Curriculum Ruling](https://time.com/7298359/supreme-court-lgbtq-curriculum-opt-out-religious-liberty/)  
        🔗 [WSJ – Trans Rights Rollback](https://www.wsj.com/politics/policy/transgender-rights-movement-challenges-b8de6e62)
        """)

    with tabs[2]:
        st.markdown("These examples highlight the global divergence in LGBTQ+ rights: while some countries are making historic strides toward equality, others are enacting laws that undermine decades of progress.")

# Create tabs for each column
with st.expander("LGBTQ+ Rights Exploratory Analysis"):
    columns = df.columns
    column_tabs = st.tabs([col for col in columns if col not in ['Territory', 'Same-sex sexual activity', 'Unknown Rights']])
    
    for tab, column in zip(column_tabs, [col for col in columns if col not in ['Territory', 'Same-sex sexual activity', 'Unknown Rights']]):
        with tab:
            st.subheader(column)
            
            # Column descriptions and analysis
            if column == "Recognition of same-sex unions":
                st.write("Indicates whether a country legally recognizes same-sex unions, such as civil partnerships or domestic partnerships. This is distinct from marriage, but still grants some or many of the legal benefits associated with marriage, such as inheritance rights, hospital visitation, and tax benefits.")
            if column == "Same-sex marriage":
                st.write("Indicates whether same-sex marriage is legally recognized, granting full marital rights equal to those of heterosexual couples. This includes not only civil benefits but also symbolic recognition of equality under the law. As of now, less than one-third of countries allow full same-sex marriage.")
            if column == "Adoption by same-sex couples":
                st.write("Indicates whether same-sex couples are legally allowed to adopt children. This includes joint adoption as well as second-parent or stepchild adoption. Legal barriers in many countries still prevent same-sex couples from building families with full parental rights.")
            if column == "LGBT people allowed to serve openly in military?":
                st.write("Indicates whether LGBTQ+ individuals are permitted to serve openly in the national armed forces without risk of expulsion, harassment, or forced concealment. In some countries, LGBTQ+ people are barred entirely; in others, they may serve but must hide their identity.")
            if column == "Anti-discrimination laws concerning sexual orientation":
                st.write("Indicates whether a country has national laws that protect individuals from discrimination based on sexual orientation in key areas such as employment, housing, education, and access to services. These laws are essential for protecting the dignity and safety of LGBTQ+ people.")
            if column == "Anti-discrimination laws concerning gender identity":
                st.write("Indicates whether a country has national laws protecting against discrimination based on gender identity. These laws are crucial for safeguarding the rights of transgender and gender nonconforming individuals in areas such as employment, healthcare, education, and housing.")
            
            # Basic statistics and analysis
            value_counts = df[column].value_counts()
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
            fig = px.bar(
                value_counts,
                title=f'Breakdown of {column}',
                labels={'index': 'Value', 'value': 'Count'}
            )
            st.plotly_chart(fig, key=f'bar_chart_{column}')
            
            # Create map visualization
            fig = px.choropleth(
                df,
                locations="Territory",
                locationmode="country names",
                color=column,
                title=f"Global Distribution of {column}",
                color_continuous_scale="Viridis",
                hover_data=['Territory', column]
            )
            st.plotly_chart(fig, key=f'map_{column}')

with st.expander("Same-sex Marriage and Democracy Analysis"):
    st.markdown("""
    Countries that allow same-sex marriage tend to have higher democracy scores on average, indicating a statistically significant correlation between LGBTQ+ rights and democratic governance.
    """)

    # Read democracy index data
    democracy_df = pd.read_csv('democracy_index.csv')

    # Merge datasets on country name
    merged_df = pd.merge(df, democracy_df, left_on='Territory', right_on='Country', how='inner')

    # Calculate average democracy scores for countries with and without same-sex marriage
    marriage_allowed = merged_df[merged_df['Same-sex marriage'] == 'Yes']['Democracy Index'].mean()
    marriage_not_allowed = merged_df[merged_df['Same-sex marriage'] == 'No']['Democracy Index'].mean()

    # Create DataFrame for visualization
    avg_scores = pd.DataFrame({
        'Group': ['Same-sex marriage allowed', 'Same-sex marriage not allowed'],
        'Average Democracy Score': [marriage_allowed, marriage_not_allowed]
    })

    # Create bar chart
    fig = px.bar(
        avg_scores,
        x='Group',
        y='Average Democracy Score',
        title='Average Democracy Scores by Same-sex Marriage Status',
        color='Group',
        color_discrete_sequence=['#636EFA', '#EF553B']
    )

    # Add text labels
    for i, row in avg_scores.iterrows():
        fig.add_annotation(
            x=row['Group'],
            y=row['Average Democracy Score'],
            text=f"{row['Average Democracy Score']:.2f}",
            showarrow=False,
            yshift=10
        )

    st.plotly_chart(fig, key='democracy_bar_chart_1')
        
    # Run t-test
        
    # Get democracy scores for countries with and without marriage
    scores_with_marriage = merged_df[merged_df['Same-sex marriage'] == 'Yes']['Democracy Index'].dropna()
    scores_without_marriage = merged_df[merged_df['Same-sex marriage'] == 'No']['Democracy Index'].dropna()

    # Calculate statistics from data
    marriage_allowed = merged_df[merged_df['Same-sex marriage'] == 'Yes']['Democracy Index'].mean()
    marriage_not_allowed = merged_df[merged_df['Same-sex marriage'] == 'No']['Democracy Index'].mean()
    mean_difference = marriage_allowed - marriage_not_allowed

    # Run two-sample t-test
    t_stat, p_value = ttest_ind(scores_with_marriage, scores_without_marriage, equal_var=False)

    # Show detailed statistical analysis
    st.markdown(f"""
    ### Statistical Analysis
    A two-sample t-test was conducted to compare the average democracy scores between countries that recognize same-sex marriage and those that do not.

    Results:
    - Mean democracy score (same-sex marriage recognized): {marriage_allowed:.2f}
    - Mean democracy score (not recognized): {marriage_not_allowed:.2f}
    - Mean difference: {mean_difference:.2f} points
    - T-statistic: {t_stat:.2f}
    - P-value: {p_value:.4f}

    Interpretation:
    The results indicate a statistically significant difference in democracy scores between the two groups (t(df) = {t_stat:.2f}, p = {p_value:.4f}), with countries recognizing same-sex marriage exhibiting substantially higher average democracy scores. This result is significant at the α = 0.05 level, suggesting a strong association between democratic governance and the legal recognition of same-sex marriage.
    """)

# Correlation Analysis
with st.expander("Correlation Analysis Between LGBTQ+ Rights"):
    st.markdown("""
    This heatmap shows the relationships between different LGBTQ+ rights across countries. 
    While many LGBTQ rights are highly correlated with each other, others, like recognition of same-sex unions and adoption by same-sex couples, are less correlated. This indicates that some rights are more important than others, likely because of their impact on LGBTQ+ people's lives.
    """)

    # Select columns for correlation analysis (excluding non-binary columns)
    analysis_columns = ['Same-sex marriage', 'Recognition of same-sex unions', 
                        'Adoption by same-sex couples', 
                        'LGBT people allowed to serve openly in military?',
                        'Anti-discrimination laws concerning sexual orientation',
                        'Laws concerning gender identity/expression']
    
    # Convert Yes/No to binary values
    binary_df = df[analysis_columns].replace({'Yes': 1, 'No': 0, 'Unknown': None})
    
    # Calculate correlation matrix
    corr_matrix = binary_df.corr()
    
    # Create interactive heatmap
    fig = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu',
        range_color=[0, 1],
        color_continuous_midpoint=0.5  # Center the color scale at 0.5
    )
    
    # Update layout for better interactivity
    fig.update_layout(
        hovermode='closest',
        clickmode='event+select',
        dragmode='select'
    )
    
    # Update colorbar
    fig.update_coloraxes(
        showscale=True,
        colorbar_title_text='Correlation',
        colorbar_title_side='right'
    )
    
    st.plotly_chart(fig, key='correlation_heatmap')