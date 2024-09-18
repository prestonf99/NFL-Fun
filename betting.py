import nfl_data_py as nfl
import warnings
warnings.simplefilter('ignore')
import pandas as pd
from pylab import mpl, plt
plt.style.use('dark_background')
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '0.05'
plt.rcParams['grid.color'] = '0.25'


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
        