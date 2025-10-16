# UT2004 Omnip)o(tents Match Scrapers
Python scripts to scrape UT2004 player statistics from Omnip)o(tent's UTStatsDB page and print them to .csv files for further analysis. Generates multiple .csv files that can be freely altered and analyzed. Comes with two scrapers--one for node statistics and another for combat statistics--alongside cleaning scripts that will make both tables primed and ready for EDA. The Cleaning scripts aren't mandatory for the 

## Requirements

1. Python is needed to run the script
2. Visual Studo Code (preferred, as you can view both the code and the .csv files together)
3. The Debug Visualizer extension (if using VSC to create visualizations using this data)
4. Dependencies:
     requests, re, bs4 (beautifulsoup4), pandas, datetime, urllib.parse, matplotlib.pyplot, sklearn.cluster (optional, if you want to do data analysis right within the Cleaning scripts)

## How to Use

**YOU MUST RUN THE SCRIPTS IN THE ORDER LISTED BELOW** (if looking to use both the scrapers and the cleaners). If you end up running the Cleaning scripts more than once, you will need to go back and re-process the Scraping scripts (I will probably be tweaking the code in the near future so that each script can be repeatedly ran without needing to do this).

1. PlayerStatsScraper and ObjStatsScraper
2. PlayerStatsCleaning and ObjStatsCleaning

To Use (Scrapers): simply run each script in the order mentioned above. The scripts will automatically pull select matches from UTStatsDB (https://www.omnipotents.com/utstats2/) into their own .csv file, then use that file to scrape player combat statistics and player node statistics into separate .csv files containing raw data. Said files are then preliminarily trimmed and loaded into third .csv files that are ready for the Cleaning scripts.

To Use (Cleaners): simply run each script in the order mentioned above. They will automatically pull and clean up both of the final .csv files the Scrapers had created, then will combine repeated player stats into a single row while averaging out their statistics. By the end, you will have two cleaned .csv files that can be further analyzed: "objstats.csv" and "playerstats.csv".
