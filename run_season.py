import pandas as pd
import warnings
warnings.simplefilter('ignore')
import my_roster as mr
import nfl_data_py as nfl

def get_data(type=None):
    df = pd.read_csv('nfl.csv')
    raw = df[df['season_type'].isin(['REG'])]
    data = raw[['play_id', 'game_id', 'posteam', 'defteam', 'play_type', 'yards_gained',
            'receiving_yards', 'rushing_yards','posteam_score_post']]
    #data = data[data['defteam'].isin([team])]
    data = data[data['play_type'].isin(['pass', 'run'])]
    data = data.rename(columns={'yards_gained':'yards_allowed', 'posteam':'offense',
                               'defteam':'defense'})
    game_summary = data.groupby(['game_id', 'defense', 'offense']).agg({
        'yards_allowed': 'sum',     # Total yards allowed
        'rushing_yards': 'sum',     # Total rushing yards
        'receiving_yards': 'sum',   # Total receiving yards
        'posteam_score_post': 'max',# Final score after all plays
        'play_id': 'count'          # Total number of plays
    }).reset_index()
    
    game_summary = game_summary.rename(columns={
        'defense':'team',
        'offense':'opp',
        'yards_allowed': 'total_yards_allowed',
        'rushing_yards': 'rush_yards_allowed',
        'receiving_yards': 'receiving_yards_allowed',
        'posteam_score_post': 'points_allowed',
        'play_id': 'plays'
    })
    
    season_summary = game_summary.groupby('team').mean(numeric_only=True)
    season_summary['TY Rank'] = season_summary['total_yards_allowed'].rank(ascending=True)
    season_summary['RY Rank'] = season_summary['rush_yards_allowed'].rank(ascending=True)
    season_summary['RecY Rank'] = season_summary['receiving_yards_allowed'].rank(ascending=True)
    season_summary['PA Rank'] = season_summary['points_allowed'].rank(ascending=True)
    season_summary = season_summary.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    season_summary = season_summary[['total_yards_allowed', 'TY Rank', 'rush_yards_allowed', 'RY Rank',
                                     'receiving_yards_allowed', 'RecY Rank', 'points_allowed', 'PA Rank',
                                     'plays']]
    


    if type is not None:
        return game_summary
    else:
        return season_summary




def get_prior_matchup(team=None, opp=None):
    data = get_data('')
    if team is not None:
        data = data[data['team'].isin([team])]
    if opp is not None:
        data = data[data['opp'].isin([opp])]

    return data


def get_schedule(team=None, week=None):
    data = nfl.import_schedules([2024])
    data = data[['game_id', 'week', 'away_team', 'home_team']]
    if team is not None:
        data = data[(data['home_team'].isin([team])) | 
        (data['away_team'].isin([team]))
        ]
        
    if week is not None:
        data = data[data['week'].isin([week])]
        
    return data

def my_roster(week):
    data = pd.DataFrame()
    data['player'] = mr.players
    data['team'] = mr.team
    data['week'] = week
    data = data[['player', 'week', 'team']]
    schedule = get_schedule(team=None, week=week)
    merged_home = data.merge(schedule[['home_team', 'away_team']], left_on='team',
                            right_on='home_team', how='left')
    merged_away = data.merge(schedule[['home_team', 'away_team']], left_on='team',
                            right_on='away_team', how='left')
    merged_home['opponent'] = merged_home['away_team']
    merged_away['opponent'] = merged_away['home_team']
    final_data = pd.concat([merged_home[['player', 'week', 'team', 'opponent']],
                        merged_away[['player', 'week', 'team', 'opponent']]])
    final_data = final_data.drop_duplicates()
    final_data = final_data.reset_index(drop=True)
    final_data.dropna(inplace=True)
    data = final_data

    return data

def fantasy_matchups(week, style=None, sort=None):
    stats = get_data()
    stats = stats.rename(columns={'total_yards_allowed':'Yards Allowed', 'rush_yards_allowed':'Avg RushYds',
                              'receiving_yards_allowed':'Avg RecYds', 'points_allowed':'PA/PG'})
    data = my_roster(week)
    merged = pd.merge(data, stats, left_on='opponent', right_on='team', how='left')
    merged = merged.drop(columns={'plays'})
    merged = merged.rename(columns={'team_x':'team'})
    data = merged
    if sort is not None:
        data = data.sort_values(sort, ascending=False)
    else:
        data = data.sort_values('Yards Allowed', ascending=False)

    if style is None:
        data = data.style \
            .background_gradient(cmap='RdYlGn_r', subset=['TY Rank', 'RY Rank', 'RecY Rank', 'PA Rank'], vmin=1, vmax=32)\
            .background_gradient(cmap='RdYlGn_r', subset=['Yards Allowed'], vmin=310, vmax=390) \
            .background_gradient(cmap='RdYlGn_r', subset=['Avg RushYds'], vmin=90, vmax=140) \
            .background_gradient(cmap='RdYlGn_r', subset=['Avg RecYds'], vmin=190, vmax=270) \
            .background_gradient(cmap='RdYlGn_r', subset=['PA/PG'], vmin=15, vmax=26) \
            .applymap(lambda _: 'background-color: grey', subset=['player', 'week', 'team']) \
            .applymap(lambda _: 'background-color: grey; font-weight: bold; color: black', subset=['opponent']) \
            .format({'Yards Allowed':'{:.0f}', 'TY Rank':'{:.0f}', 'Avg RushYds':'{:.0f}', 'Avg RecYds':'{:.0f}',
                        'RY Rank':'{:.0f}', 'RecY Rank':'{:.0f}', 'PA/PG':'{:.0f}', 'PA Rank':'{:.0f}' })\
            .set_table_styles([
                {'selector': 'thead th', 'props': [('background-color', 'grey'), ('color', 'black'),
                                                   ('font-weight', 'bold'), ('text-align', 'center')]},
                {'selector': 'td', 'props': [('padding', '5px')]},
            ])
        
    print(f' Data vs. 2024 YTD Data')   

    return data