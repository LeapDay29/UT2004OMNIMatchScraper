import requests
import re
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Read in the player stats and preview
stats = pd.read_csv("playerstats.csv")
print(stats.head(10))

# View basic information about the data
print(stats.describe)
print(stats.dtypes)

# Remove instances of "Player" in PlayerName (aka unknown/anonymous users)
stats = stats[~stats['PlayerName'].str.contains('Player', case=False, na=False)]

# Function that converts the time-based columns into a program-readable format
def parse_time(t):
    if pd.isna(t):
        return pd.NaT
    match = re.match(r'(?:(\d+)m)?\s*(?:(\d+)s)?', str(t))
    if match:
        minutes = int(match.group(1)) if match.group(1) else 0
        seconds = int(match.group(2)) if match.group(2) else 0
        total_seconds = minutes * 60 + seconds
        return pd.to_timedelta(total_seconds, unit='s')
    return pd.NaT

tdcols = ["AvgTimeToLive", "TimePlayingInMatch"]
for col in tdcols:
    stats[col] = stats[col].apply(parse_time)

# Change necessary columns from "object" to their appropriate types. View the columns afterwards to verify
numcols = ["RankInMatch", "FinalScore", "Frags", "Kills", "Deaths", "Suicides", "AvgScorePerHour", "KillingSpree", "Rampage", "Dominating", "Unstoppable", "Godlike", "WickedSick"]
tdcols = ["AvgTimeToLive", "TimePlayingInMatch"]  
stats[numcols] = stats[numcols].apply(pd.to_numeric, errors="coerce")
stats[tdcols] = stats[tdcols].apply(pd.to_timedelta, errors="coerce")

'''The goal of this analysis exercise is to eventually build a ranking algorithm/ELO system based on the skill levels of each player. 
To do this, we need to find which statistics are the greatest indicators of player pereformance. Before we can do this, we need to 
understand the characteristics and relationships in the data.'''

## To simplify the dataset, first combine each player into a single row, taking the mean of each numeric and time-based column to determine their average performances.

# Create separate objects based on the column type
numcols = stats.select_dtypes(include=["float64", "int64"]).columns
tdcols = stats.select_dtypes(include=["timedelta64[ns]"]).columns

# Group each of these items for each player by their average numeric and timedelta columns. Note that timedelta is rounded to the nearest second
numstats = stats.groupby("PlayerName", as_index=False)[numcols].mean()
timestats = stats.groupby("PlayerName", as_index=False)[tdcols].mean(numeric_only=False).apply(lambda col: col.dt.floor("s") if col.dtype == "timedelta64[ns]" else col)

# Merge the two items back together
statsavgs = pd.merge(numstats, timestats, on="PlayerName", how="outer")

# Convert the time-based columns to hours-minutes-seconds
def format_timedelta(td):
    if pd.isna(td):
        return None
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

for col in tdcols:
    statsavgs[col] = statsavgs[col].apply(format_timedelta)

# View the changes
print(statsavgs.head(25))
print(statsavgs.dtypes)

# Round the numeric columns to 2 decimal places
numstats = statsavgs.select_dtypes(include=["float64"]).columns
statsavgs[numstats] = statsavgs[numstats].round(2)

statsavgs.to_csv("playerstats.csv", index=False)

'''We now have a usable array of data that is ready for analysis.'''
