import requests
import re
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Read in the player stats and preview
objstats = pd.read_csv("objstats.csv")
print(objstats.head(10))

# View basic information about the data
print(objstats.describe)
print(objstats.dtypes)

# Remove instances of "Player" in PlayerName (aka unknown/anonymous users)
stats = objstats[~objstats['PlayerName'].str.contains('Player', case=False, na=False)]

# Change necessary columns from "object" to their appropriate types. View the columns afterwards to verify
numcols = ["RankInMatch", "FinalScore", "NodesBuilt", "NodesDestr", "WIPNodesDestr"] 
stats[numcols] = stats[numcols].apply(pd.to_numeric, errors="coerce")

## To simplify the dataset, first combine each player into a single row, taking the mean of each numeric column to determine their average performances.

# Create a separate object based on the column type
numcols = stats.select_dtypes(include=["number"]).columns

# Group for each player by their average numeric columns
avgstats = stats.groupby("PlayerName", as_index=False)[numcols].mean()

# View the changes
print(avgstats.head(25))
print(avgstats.dtypes)

# Round the numeric columns to 2 decimal places
avgstats[numcols] = avgstats[numcols].round(2)

avgstats.to_csv("objstats.csv", index=False)

'''We now have a usable array of data that is ready for analysis.'''
