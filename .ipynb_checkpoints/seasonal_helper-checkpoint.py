import pandas as pd
import nfl_data_py as nfl
import numpy as np

year = [2023]

def season_data(year, columns=None,position=None):
    data = nfl.import_seasonal_data([year], 'REG')
    name = nfl.import_weekly_data([year], ['player_id', 'player_name', 'position','recent_team']
                                  , downcast=False)
    data = pd.merge(data, name[['player_id','player_name', 'position','recent_team']],
                    on='player_id',how='left')
    data = data.drop_duplicates(subset=['player_id']).reset_index(drop=True)
    data = data.rename(columns={'player_name':'player'})
    data.set_index('player', inplace=True)
    if columns is not None:
        data = data[columns]
    if position is not None:
        data = data.loc[data['position'] == position]
    return data

def wr_annual(year, type=None):
    data = season_data(year, columns=['season','recent_team', 'position','targets', 'receptions',
                                         'receiving_yards','receiving_tds', 'receiving_fumbles',
                                         'receiving_air_yards', 'receiving_yards_after_catch',
                                         'receiving_epa', 'target_share', 'air_yards_share',
                                        'wopr_x', 'fantasy_points','player_id', 'games'],position='WR')
    data = data.rename(columns={'position':'pos','targets':'tgts','receptions':'rec',
                                'receiving_yards':'rec_yds','receiving_tds':'tds',
                                'receiving_fumbles':'fum', 'receiving_air_yards':'air_yds',
                                'receiving_epa':'epa','target_share':'tgt_share',
                               'receiving_yards_after_catch':'rec_yac', 
                               'fantasy_points':'points','recent_team':'team',
                               'air_yards_share':'air_yds_share','player_id':'id',
                               'games':'GP'})
    data['GP'].replace(0, 1, inplace=True)
    data['% rec'] = data['rec'] / data['tgts']
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    
    if type is not None:
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        data = data.fillna(1)
        df1 = data[['season', 'team', 'pos','id', 'GP']]
        df2 = data[['tgts', 'rec','rec_yds', 'tds','fum','air_yds','rec_yac','epa',
                    'tgt_share','air_yds_share','wopr_x','points',
                    '% rec']].apply(lambda x: x / data['GP'])
        data = df1.join(df2, how='inner')
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
        

    return data

def te_annual(year, type=None):
    data = season_data(year, columns=['season', 'recent_team','position','targets', 'receptions',
                                         'receiving_yards','receiving_tds', 'receiving_fumbles',
                                         'receiving_air_yards', 'receiving_yards_after_catch',
                                         'receiving_epa', 'target_share', 'air_yards_share',
                                        'wopr_x','fantasy_points','player_id', 'games'],position='TE')
    data = data.rename(columns={'position':'pos','targets':'tgts','receptions':'rec',
                                'receiving_yards':'rec_yds','receiving_tds':'tds',
                                'receiving_fumbles':'fum', 'receiving_air_yards':'air_yds',
                                'receiving_epa':'epa','target_share':'tgt_share',
                               'receiving_yards_after_catch':'rec_yac','fantasy_points':'points',
                               'recent_team':'team', 'air_yards_share':'air_yds_share',
                               'player_id':'id', 'games':'GP'})
    data['GP'].replace(0, 1, inplace=True)
    data['% rec'] = data['rec'] / data['tgts']
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    
    if type is not None:
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        data = data.fillna(1)
        df1 = data[['season','GP', 'team','id', 'pos']]
        df2 = data[['tgts', 'rec','rec_yds', 'tds','fum','air_yds','rec_yac','epa',
                    'tgt_share','air_yds_share','wopr_x','points']].apply(lambda x: x / data['GP'])
        data = df1.join(df2, how='inner')
        data['% rec'] = data['rec'] / data['tgts']
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

    return data


def rb_annual(year, type=None):
    data = season_data(year, columns=['season', 'recent_team', 'position', 'carries',
                                      'rushing_yards','rushing_tds','rushing_first_downs',
                                      'rushing_epa','receptions','receiving_yards',
                                      'receiving_tds','fantasy_points', 'player_id',
                                     'target_share', 'games'],position='RB')
    data = data.rename(columns={'recent_team':'team','position':'pos','rushing_tds':'rush_td',
                                'rushing_fumbles_lost':'fumbles','rushing_first_downs':'first_downs',
                                'rushing_epa':'epa','receptions':'rec','receiving_yards':'rec_yds',
                                'receiving_tds':'rec_td','fantasy_points':'points','rushing_yards':'rush_yds',
                               'player_id':'id', 'target_share':'tgt_share', 'games':'GP'})
    data['GP'].replace(0, 1, inplace=True)
    data['TD'] = data['rec_td'] + data['rush_td']
    data['YPC'] = data['rush_yds']/data['carries']
    data_ = data.reset_index()
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    if type is not None:
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        data = data.fillna(1)
        df1 = data_[['player', 'GP','season', 'team', 'pos', 'YPC', 'id']]
        df2 = data_[['id','team','carries', 'rush_yds', 'rush_td', 
                    'first_downs', 'epa', 'rec','rec_yds', 'rec_td',
                    'points', 'TD', 'tgt_share']] 
        data = pd.merge(df1, df2, on=['id', 'team'], how='inner')
        num_cols = ['carries', 'rush_yds', 'rush_td', 
                    'first_downs', 'epa', 'rec','rec_yds', 'rec_td',
                    'points', 'TD', 'tgt_share']
        data[num_cols] = data[num_cols].apply(lambda x: x / data['GP'])
        data.set_index('player', inplace=True)
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)    
    return data



def qb_annual(year, type=None):
    data = season_data(year,columns=['season', 'recent_team','position',
                                        'attempts', 'completions', 'passing_yards',
                                        'passing_tds','interceptions','sacks',
                                        'passing_air_yards','passing_epa',
                                        'rushing_yards','player_id',
                                       'fantasy_points', 'games', 'rushing_tds'],position='QB')
    data['games'] = data['games'].astype(float)
    data = data.rename(columns={'recent_team':'team', 'passing_yards':'pass_yds',
                                'passing_tds':'pass_tds', 'interceptions':'int',
                                'passing_epa':'pass_epa', 'rushing_yards':'rush_yds',
                                'player_id':'id', 'position':'pos', 
                               'passing_air_yards':'air_yds', 'fantasy_points':'points',
                               'games':'GP', 'rushing_tds':'rush_td'})
    data['GP'].replace(0, 1, inplace=True)
    data['comp_pct'] = (data['completions'] / data['attempts']) * 100
    data['YPA'] = (data['pass_yds'] / data['attempts'])
    data['tdint'] = (data['pass_tds'] / data['int'])
    data['tds'] = data['rush_td'] + data['pass_tds']
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    if type is not None:
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        data = data.fillna(1)
        df1 = data[['season', 'team','GP', 'pos', 'id', 'comp_pct', 'YPA', 'tdint']]
        df2 = data[['attempts', 'completions', 'pass_yds', 'rush_yds',
                    'tds', 'int', 'air_yds', 'pass_epa', 'points']].apply(lambda x: x / data['GP'])
        data = df1.join(df2, how='inner')
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
 
    return data









