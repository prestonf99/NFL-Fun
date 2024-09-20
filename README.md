# NFL Stats / Fantasy Helper

## Overview
This project was designed to analyze NFL data using nfl_data_py and create graphics that are useful for fantasy football players & football fans. There are various scripts in this repository to handle various tasks such analyzing week-to-week performance data, analyzing your fantasy roster, and viewing teams' historical performance vs. betting lines. 

## Project Structure

1. `Library.ipynb`: Jupyter notebook that shows all available uses. 
2. `my_roster.py`: Users can upload their fantasy rosters into this file to view the defenses they're up against on the week. 
3. `seasonal_helper.py`: organizes players annual performance by position. 
4. `week_to_week.py`: organizes weekly data by position and also has some plots to evaluate RB & WR performance. 
5. `tables.py`: outputs are tables by position that create a visual graphic of players' performance (by position) on a week-to-week basis.  
6. `run_season.py`: processes YTD data & ranks the defenses across the league, uploads your roster, and creates a table that allows the user to analyze the defenses your fantasy players are up against on the week. 
7. `betting.py`: In development. Currently can tell you teams performances vs. the over by season, the league's performance against various spreads, and specific teams performances vs. various spreads over the last 10 years.
8. `nfl.csv`: Needed to pull the 2024 pbp data out of nflfastR and manually upload it into a csv due to nfl_data_py not supporting it currently. Updated weekly. 

## Setup

    git clone https://github.com/prestonf99/NFL-Fun.git
    cd nfl-betting-analysis
Install the necessary python packages
    
    pip install -r requirements.txt

## Usage

Every current use is in `library.ipynb`. Take a look through it and use whatever you'd like! It's designed to be executed in a jupyter notebook. 

