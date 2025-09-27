# UT2004 Omnip)o(tents Match Scraper
Python script to scrape UT2004 player statistics from Omnip)o(tent's UTStatsDB page and print them to .csv files for further analysis. Generates 3 .csv files:

1. A list of matches played over (roughly) the past month that included at least 16 players
2. A raw, uncleaned file of player statistics
3. A trimmed and cleaned version of the player statistics with updated column names and organized in alphabetical order by player name

## Requirements

1. Python is needed to run the script
2. Visual Studo Code (preferred, as you can view both the code and the .csv files together)
3. Dependencies:
     requests, re, bs4 (beautifulsoup4), pandas, datetime, urllib.parse

## How to Use
a
Simply click the Run button. The script will automatically pull select matches from UTStatsDB (https://www.omnipotents.com/utstats2/) into its own .csv file, then use that file to scrape player statistics into a raw .csv file. Said raw file is subsequently cleaned and loaded into an improved .csv file that is ready for data analysis.
