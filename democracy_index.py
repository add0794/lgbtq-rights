import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_democracy_index_data(url):
    
    # Make the request
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table
    table = soup.find('table')
    
    # Get the headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    
    # Print actual headers for debugging
    print("Actual column headers:", headers)
    
    # Get the rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip header row
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        if row:  # Skip empty rows
            rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    
    # Print first few rows for debugging
    print("\nFirst few rows:")
    print(df.head())
    
    # Clean up the data
    # Use actual column names from the print output
    df = df.rename(columns={
        'Democracy Index 2023': 'Democracy Index',
        'Country (or dependency)': 'Country'
    })
    
    # Convert numeric columns to appropriate types
    # Use actual column names from the print output
    if 'Rank' in df.columns:
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
    if 'Democracy Index' in df.columns:
        df['Democracy Index'] = pd.to_numeric(df['Democracy Index'], errors='coerce')
    
    # Keep only Country and Democracy Index columns
    df = df[['Country', 'Democracy Index']]
    
    return df

# Create DataFrame and save to CSV
if __name__ == "__main__":
    url = "https://worldpopulationreview.com/country-rankings/democracy-index-by-country"
    df = get_democracy_index_data(url)
    df.to_csv('democracy_index.csv', index=False)
    print("Democracy index data saved to democracy_index.csv")
    print("\nFirst few rows:")
    print(df.head())
