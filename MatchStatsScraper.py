import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urljoin

## PULL ALL BIG MATCHES OVER THE PAST MONTH (ROUGHLY) ##

# Pull all of the pages containing the tabular data
urls = [
    'https://www.omnipotents.com/utstats2/index.php?stats=matches',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=2',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=3',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=4',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=5',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=6',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=7',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=8',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=9',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=10',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=11',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=12',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=13',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=14',
    'https://www.omnipotents.com/utstats2/index.php?stats=matches&page=15' 
]    

# Format the timestamp to match the website
datecolumn = "Date"
dateformat = "%a, %b %d %Y, %I:%M:%S %p"

# Pull all data from the past 30 days
today = datetime.today()
cutoff = today - timedelta(days=30)

# Empty list shell. Will be used to combine all the tables 
all_data = []

# Scrape the table for the necessary data
for url in urls:
    print(f"Scraping {url}...")
    try:

        # Obtain the HTML once
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        html = r.text

        # Read the data into pandas and select the desired table
        matches = pd.read_html(url)
        matchtable = matches[1]

        # Set the first row as the header
        matchtable.columns = matchtable.iloc[0]
        matchtable = matchtable[1:]
        matchtable = matchtable.reset_index(drop=True)

        # Convert the date column to datetime
        matchtable[datecolumn] = pd.to_datetime(matchtable[datecolumn], format=dateformat, errors="coerce")

        # Convert the Plrs column to numeric so that the table can be properly filtered
        matchtable['Plrs'] = pd.to_numeric(matchtable['Plrs'], errors='coerce')
        matchtable.dropna(subset=['Plrs'], inplace=True)

        # Grab the hyperlink URLs from the Date column in order to display the match number
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find_all("table")[1]
        links = []
        for a in table.select("tr td:nth-child(1) a"):
            abs_url = urljoin(url, a.get("href"))
            links.append(abs_url)

        # Ensure the lengths match
        if len(links) == len(matchtable):
            matchtable["MatchURL"] = links
        else:
            # Contingency that populates NaNs for mismatches
            matchtable["MatchURL"] = pd.Series(links).reindex(matchtable.index)

        # Filtered table pulling all matches with 16 or more players (AKA 50% of a traditional server size)
        fm = matchtable[(matchtable['Plrs'] >= 16) & (matchtable[datecolumn] >= cutoff)]

        # Preview the top of each table to confirm proper formatting
        print(fm.head())

        all_data.append(fm)
    
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Join all the filtered rows into one dataframe
fm_df = pd.concat(all_data, ignore_index=True)

print("\nFiltered matches with 14 players or more over the past 30 days:")
print(fm_df)

# Create a CSV file containing the table
fm_df.to_csv("bigmatches.csv", index = False)
print("Saved bigmatches.csv. Ctrl + click the timestamp to view the raw statistics (opens the match's UTStatsDB page in your browser).")

# -------------------------------------------------------------- #
## PULL THE PLAYER STATISTICS OF ALL THE SELECTED BIG MATCHES ##

# Load the new CSV file in
md = pd.read_csv("bigmatches.csv")

# Pull the match IDs from the CSV file
if "match_id" not in md.columns:
    md["match_id"] = md["MatchURL"].str.extract(r"match=(\d+)").astype(int)

# Convert missing (NaN) values in the bigmatches.csv data to integer
match_ids = md["match_id"].dropna().astype(int)

print(f"Scraping stats from populated games...")

# Base elements necessary to complete the scrape and print into a CSV file
baseurl = "https://www.omnipotents.com/utstats2/matchstats.php?match="
all_tables = []

# Perform the scrape of ONLY the player statistics contained within the match pages inside bigmatches.csv
for match_id in match_ids:
    url = f"{baseurl}{match_id}"
    try:
        print(f"Fetching {url}...")
        r = requests.get(url, timeout = 10)
        r.raise_for_status

        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[9]
        all_tables.append(df)
    except Exception as e: # For missing data due to UTStatsDB issues
        print(f"Failed to fetch match {match_id}: {e}")
    
# Concatenate/join all of the scraped data into one big table
if all_tables:
    playerstats = pd.concat(all_tables, ignore_index=True)
    playerstats = playerstats.drop_duplicates(keep="first")
    playerstats.to_csv("playerstatsraw.csv", index=False)
    print("Saved all player stats for the indicated matches to playerstatsraw.csv")
else:
    print("No data collected.")

# -------------------------------------------------------------- #
## CLEAN AND ORGANIZE THE TABLE FOR ANALYSIS ##

# Load in the data and preview it
ps = pd.read_csv("playerstatsraw.csv")
print(ps.head(10))

# Trim off redundant/erroneous rows/columns. Preview it again to see the changes
ps = ps.iloc[2:]
ps = ps[~ps["0"].str.contains("Totals", case=False, na=False)]
ps = ps.reset_index(drop=True)
ps = ps.drop(columns=["2", "18"])
print(ps.head(50))

# Re-organize by player name in case-insensitive alphabetical order
psabc = ps.sort_values(
    by="1",
    key=lambda col: col.str.lower()
)
print(psabc.head(100))

# Return original column names to the table (remove the nondescript numbers)
psabc.columns = ["RankInMatch", "PlayerName", "FinalScore", "Frags", "Kills", "Deaths", "Suicides", "Efficiency", "AvgScorePerHour", "AvgTimeToLive", "TimePlayingInMatch", "KillingSpree", "Rampage", "Dominating", "Unstoppable", "Godlike", "WickedSick"]
print(psabc.head(10))

# Export to a separate CSV file
psabc.to_csv("playerstats.csv", index=False)