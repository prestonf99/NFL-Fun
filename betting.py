import nfl_data_py as nfl
import warnings
warnings.simplefilter('ignore')
import pandas as pd
from pylab import mpl, plt
import numpy as np
plt.style.use('dark_background')
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '0.05'
plt.rcParams['grid.color'] = '0.25'
from imageio import imread


def team_over(year, team=None):
    data = nfl.import_schedules(year)
    raw = data[data['game_type'].isin(['REG'])]
    data = raw[['game_id', 'home_team', 'away_team', 'total', 'total_line']]
    if team is not None:
        data = data[(data['home_team'].isin([team])) | (data['away_team'].isin([team]))]
    data.dropna(inplace=True)
    data['cover_over'] = data['total'] > data['total_line']
    team_cover = data['cover_over'].sum() / len(data)
    return data


def league_over(year):
    # calcolate_leag_over([2023, 2024])
    data = team_over([year])
    home_data = data[['home_team', 'total_line','cover_over']].copy()
    home_data.rename(columns={'home_team':'team'}, inplace=True)
    away_data = data[['away_team', 'total_line', 'cover_over']].copy()
    away_data.rename(columns={'away_team':'team'}, inplace=True)
    data = pd.concat([home_data, away_data])
    team_cover = data.groupby('team')['cover_over'].mean()
    mean_line = data.groupby('team')['total_line'].mean()
    team_cover_percent = team_cover * 100
    data = pd.DataFrame(team_cover_percent)
    data['mean_over'] = mean_line
    data = data.reset_index()
    data = data.sort_values('cover_over')
    plt.figure(figsize=(10, 6))
    plt.barh(data['team'], data['cover_over'], color='b', alpha=0.75)
    plt.scatter(data['mean_over'], data['team'], color='w',marker='.', label='Avg. Line')
    plt.legend(loc='lower right')
    plt.xlabel('Probability of Covering the Over')
    plt.title(f'{year} Data: Probability Team Beats the Over')
    plt.grid(False)


def spread_covers(year):
    raw = nfl.import_schedules([year])
    raw = raw[raw['game_type'].isin(['REG'])]
    data = raw[['game_id', 'home_team', 'away_team', 'home_score', 'away_score','spread_line', 'result']]
    data.dropna(inplace=True)
    home_data = data[['home_team', 'spread_line', 'result']].copy()
    home_data['cover_spread'] = home_data['result'] >= home_data['spread_line']
    home_team_covers = home_data['cover_spread'].sum() / len(home_data)
    away_data = data[['away_team', 'spread_line', 'result']].copy()
    away_data['spread_line'] = away_data['spread_line'] * -1
    away_data['result'] = away_data['result'] * -1
    away_data['cover_spread'] = away_data['result'] >= away_data['spread_line']
    away_team_covers = away_data['cover_spread'].sum() / len(home_data)
    print(f'In the {year} Season, the home team covered the spread {home_team_covers:.2%} of the time')
    print(f'In the {year} Season, the away team covered the spread {away_team_covers:.2%} of the time')


def team_spread_covers(year, plot=None):
    raw = nfl.import_schedules([year])
    raw = raw[raw['game_type'].isin(['REG'])]
    data = raw[['game_id', 'home_team', 'away_team', 'home_score', 'away_score','spread_line', 'result']]
    data.dropna(inplace=True)
    home_data = data[['home_team', 'spread_line', 'result']].copy()
    home_data = data.rename(columns={'home_team':'team'})
    home_data['cover_spread'] = home_data['result'] >= home_data['spread_line']
    home_team_covers = home_data['cover_spread'].sum() / len(home_data)
    away_data = data[['away_team', 'spread_line', 'result']].copy()
    away_data = data.rename(columns={'away_team':'team'})
    away_data['spread_line'] = away_data['spread_line'] * -1
    away_data['result'] = away_data['result'] * -1
    away_data['cover_spread'] = away_data['result'] >= away_data['spread_line']
    away_team_covers = away_data['cover_spread'].sum() / len(home_data)
    cover_h = home_data.groupby('team')['cover_spread'].mean()
    cover_a = away_data.groupby('team')['cover_spread'].mean()
    df = pd.DataFrame(cover_h)
    df = df.rename(columns={'cover_spread':'cover_home'})
    df_ = pd.DataFrame(cover_a)
    df_ = df_.rename(columns={'cover_spread':'cover_away'})
    data = pd.merge(df, df_, on='team', how='inner')
    data = data * 100
    data['season_avg'] = data[['cover_home', 'cover_away']].mean(axis=1)
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

    if plot is None:
        plt.figure(figsize=(10, 8))
        plt.barh(data.index, data['cover_home'], color='w', alpha=0.75, label='Home Games')
        plt.barh(data.index, data['cover_away'], facecolor='None', edgecolor='red', label='Away Games')
        plt.scatter(data['season_avg'],data.index,  marker='.', color='blue', label='Season Avg')
        plt.gca().invert_yaxis()
        plt.title(f'Probability of Covering Spread - {year} Season')
        plt.legend(loc='upper right');


def wp_books(type=None):
    raw = nfl.import_schedules([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
    data = raw[['game_id', 'home_team', 'away_team', 'home_score', 'away_score', 'spread_line', 'result']]
    home = data[['home_team', 'spread_line', 'result']].copy()
    home['home_cover'] = home['result'] > home['spread_line']
    home = home.rename(columns={'home_team':'team', 'home_cover':'cover'})
    away = data[['away_team', 'spread_line', 'result']].copy()
    away['spread_line'] = -away['spread_line']
    away['result'] = -away['result']
    away['away_cover'] = away['result'] > away['spread_line']
    away = away.rename(columns={'away_team':'team', 'away_cover':'cover'})
    data = pd.concat([home, away], axis=0)
    bin_edges = np.arange(data['spread_line'].min(), data['spread_line'].max() + 1.5, 1.5)
    data['spread_line_binned'] = pd.cut(data['spread_line'], bins=bin_edges, right=False)
    data = data.groupby('spread_line_binned').agg(
        cover_probability=('cover', 'mean'),
        games_played=('cover', 'count')
    ).reset_index()

    if type is not None:
        data['spread_line_binned'] = data['spread_line_binned'].astype(str)
        games_played_normalized = data['games_played'] / data['games_played'].max()
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(data['cover_probability'], data['spread_line_binned'], 
                              c=games_played_normalized,cmap='viridis', alpha=0.9,
                              s=100)
        cbar = plt.colorbar(scatter)
        cbar.set_label('Games Played (Normalized)')
        plt.title('Cover Probability vs Spread Line (2.5pt Bins, Color represents games played)')
        plt.xlabel('Spread Line (Binned)')
        plt.ylabel('Cover Probability')
        plt.xticks(rotation=90, ha='right')
        plt.axvline(0.5, color='grey', alpha=0.75, linestyle='--')
        plt.grid(True)
    else:
        data['spread_line_binned'] = data['spread_line_binned'].astype(str)
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(data['cover_probability'], data['spread_line_binned'], 
                              s=50, color='blue', alpha=0.9, label='Cover Probability')
        plt.title('Cover Probability vs Spread Line (2.5pt Bins)')
        plt.xlabel('Spread Line (Binned)')
        plt.ylabel('Cover Probability')
        for i, row in data.iterrows():
            plt.annotate(
                f'{int(row["games_played"])}',
                (row['cover_probability'],row['spread_line_binned']), 
                textcoords="offset points",  xytext=(0, 5), ha='center')
        plt.axvline(0.5, color='grey', alpha=0.75, linestyle='--')
        plt.grid(True)

def team_image(team):
    team_img = nfl.import_team_desc()
    team_img = team_img[['team_abbr', 'team_logo_espn']]
    team_img = team_img.rename(columns={'team_abbr':'team','team_logo_espn':'logo'})
    logo_url = team_img.loc[team_img['team'] == team, 'logo'].values
    logo_url = logo_url[0]
    return logo_url


def find_spread_line(value, data):
    for i, spread_range in enumerate(data['spread_line_binned']):
        low, high = [float(x) for x in spread_range.strip('[]').replace(')', '').split(', ')]
        if low <= value < high:  
            return data.loc[data['spread_line_binned'] == spread_range, 'spread_line_binned_index'].values[0]
    return None  


def team_covers(team, line=None):
    raw = nfl.import_schedules([2014, 2015, 2016, 2017,2018, 2019,
                                 2020, 2021, 2022, 2023, 2024])
    data = raw[['game_id', 'home_team', 'away_team', 'home_score',
                'away_score', 'spread_line', 'result']]
    data.dropna(inplace=True)
    home = data[['home_team', 'spread_line', 'result']].copy()
    home['home_cover'] = home['result'] > home['spread_line']
    home = home.rename(columns={'home_team':'team', 'home_cover':'cover'})
    away = data[['away_team', 'spread_line', 'result']].copy()
    away['spread_line'] = -away['spread_line']
    away['result'] = -away['result']
    away['away_cover'] = away['result'] > away['spread_line']
    away = away.rename(columns={'away_team':'team', 'away_cover':'cover'})
    data = pd.concat([home, away], axis=0)
    data = data[data['team'].isin([team])]
    bin_edges = np.arange(data['spread_line'].min(), data['spread_line'].max() + 1.5, 1.5)
    data['spread_line_binned'] = pd.cut(data['spread_line'], bins=bin_edges, right=False)
    data = data.groupby('spread_line_binned').agg(
    cover_probability=('cover', 'mean'),
    games_played=('cover', 'count'),
    ).reset_index()
    data['spread_line_binned'] = data['spread_line_binned'].astype(str)
    url = team_image(team)
    img = imread(url)
    fig, ax = plt.subplots(figsize=(10, 6))
    spread_lines = data['spread_line_binned'].unique()
    spread_lines_sorted = sorted(spread_lines, key=lambda x: np.mean([float(i) for i in x.strip('()[]').split(',')])) 
    spread_line_mapping = {val: i for i, val in enumerate(spread_lines_sorted)}
    data['spread_line_binned_index'] = data['spread_line_binned'].map(spread_line_mapping)
    ax.imshow(img, aspect='auto', extent=[-0.1, 1.1, -1, len(spread_lines_sorted)], alpha=0.3, zorder=-1)
    ax.scatter(data['cover_probability'], data['spread_line_binned_index'],
               s=50, color='grey', alpha=0.9, label='Cover Probability')
    ax.set_xlabel('Cover Probability')
    ax.set_ylabel('Spread Line')
    ax.set_title(f'{team} Cover Probability by Spread')
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-1, len(spread_lines_sorted))  # Add some padding on the y-axis
    ax.set_yticks(np.arange(len(spread_lines_sorted)))
    ax.set_yticklabels(spread_lines_sorted)
    for i, row in data.iterrows():
        ax.annotate(f'{int(row["games_played"])}', 
                    (row['cover_probability'], row['spread_line_binned_index']),
                    textcoords="offset points", xytext=(0, 5), ha='center')
    ax.axvline(0.5, color='grey', alpha=0.75, label='50% Prob', linestyle='--')
    ax.grid(True, alpha=0.3)
    if line is not None:
        plt.axhline(find_spread_line(line, data), lw=0.9, alpha=0.8, 
                    color='r', linestyle='--', label='Todays Spread')
    ax.legend();



    
    
        