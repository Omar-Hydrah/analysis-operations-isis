import pandas as pd
import csv

muslim_countries = [
    "Afghanistan", 
    "Bangladesh", 
    "Burkina Faso", 
    "Egypt",
    "Egypt / Russia"
    "Indonesia",
    "Iran",
    "Iraq",
    "Jordan",
    "Kazakhstan",
    "Kuwait",
    "Lebanon",
    "Libya",
    "Malaysia",
    "Nigeria",
    "Pakistan",
    "Philippines"
    "Saudi Arabia",
    "Syria",
    "Tajikistan",
    "Tunisia",
    "Turkey",
    "Yemen"
]

def main():
    df = pd.read_csv('isis_operations.csv')
    df.loc[df["victims"] == "-"] = 0
    df["victims"] = pd.to_numeric(df["victims"], errors='ignore').astype(int)
    df.loc[df["injured"] == "-"] = 0
    df["injured"] = pd.to_numeric(df["injured"], errors='ignore').astype(int)
    data = df.groupby(["country"])[["victims", "injured"]].sum()
    data.to_csv('filtered.csv', sep='\t')
    
    muslim_df = df.loc[df['country'].isin(muslim_countries)]
    muslim_grouped_df = muslim_df.groupby('country')[['victims', 'injured']].sum()
    muslim_victims_sum = muslim_df.groupby('country')[['victims']].sum()["victims"].sum()
    muslim_injured_sum = muslim_df.groupby('country')[['injured']].sum()["injured"].sum() 
    other_df = df.loc[~df['country'].isin(muslim_countries)]
    other_grouped_df = other_df.groupby('country')[['victims', 'injured']].sum()
    other_victims_sum = other_df.groupby('country')[['victims']].sum()['victims'].sum()
    other_injured_sum = other_df.groupby('country')[['injured']].sum()['injured'].sum()

    victims_sum = data.groupby('country')[['victims', 'injured']].sum()['victims'].sum()
    injured_sum = data.groupby('country')[['victims', 'injured']].sum()['victims'].sum()

if __name__ == "__main__":
    main()

