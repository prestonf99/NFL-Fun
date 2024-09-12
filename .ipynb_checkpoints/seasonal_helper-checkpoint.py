import pandas as pd
import nfl_data_py as nfl

year = [2023]

def season_data(year, columns=None,position=None):
    data = nfl.import_seasonal_data(year, 'REG')
    name = nfl.import_weekly_data([2023], ['player_id', 'player_name', 'position','recent_team']
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
                                        'wopr_x', 'fantasy_points','player_id'],position='WR')
    data = data.rename(columns={'position':'pos','targets':'tgts','receptions':'rec',
                                'receiving_yards':'rec_yds','receiving_tds':'tds',
                                'receiving_fumbles':'fum', 'receiving_air_yards':'air_yds',
                                'receiving_epa':'epa','target_share':'tgt_share',
                               'receiving_yards_after_catch':'rec_yac', 
                               'fantasy_points':'points','recent_team':'team',
                               'air_yards_share':'air_yds_share','player_id':'id'})
    data['% rec'] = data['rec'] / data['tgts']
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    
    if type is not None:
        df1 = data[['season', 'team', 'pos','id']]
        df2 = data[['tgts', 'rec','rec_yds', 'tds','fum','air_yds','rec_yac','epa',
                    'tgt_share','air_yds_share','wopr_x','points','% rec']] / 17
        data = df1.join(df2, how='inner')
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
        

    return data

def te_annual(year, type=None):
    data = season_data(year, columns=['season', 'recent_team','position','targets', 'receptions',
                                         'receiving_yards','receiving_tds', 'receiving_fumbles',
                                         'receiving_air_yards', 'receiving_yards_after_catch',
                                         'receiving_epa', 'target_share', 'air_yards_share',
                                        'wopr_x','fantasy_points','player_id'],position='TE')
    data = data.rename(columns={'position':'pos','targets':'tgts','receptions':'rec',
                                'receiving_yards':'rec_yds','receiving_tds':'tds',
                                'receiving_fumbles':'fum', 'receiving_air_yards':'air_yds',
                                'receiving_epa':'epa','target_share':'tgt_share',
                               'receiving_yards_after_catch':'rec_yac','fantasy_points':'points',
                               'recent_team':'team', 'air_yards_share':'air_yds_share',
                               'player_id':'id'})
    data['% rec'] = data['rec'] / data['tgts']
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    
    if type is not None:
        df1 = data[['season', 'team','id', 'pos']]
        df2 = data[['tgts', 'rec','rec_yds', 'tds','fum','air_yds','rec_yac','epa',
                    'tgt_share','air_yds_share','wopr_x','points']] / 17
        data = df1.join(df2, how='inner')
        data['% rec'] = data['rec'] / data['tgts']
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

    return data


def rb_annual(year, type=None):
    data = season_data(year, columns=['season', 'recent_team', 'position', 'carries',
                                      'rushing_yards','rushing_tds','rushing_first_downs',
                                      'rushing_epa','receptions','receiving_yards',
                                      'receiving_tds','fantasy_points', 'player_id',
                                     'target_share'],position='RB')
    data = data.rename(columns={'recent_team':'team','position':'pos','rushing_tds':'rush_td',
                                'rushing_fumbles_lost':'fumbles','rushing_first_downs':'first_downs',
                                'rushing_epa':'epa','receptions':'rec','receiving_yards':'rec_yds',
                                'receiving_tds':'rec_td','fantasy_points':'points','rushing_yards':'rush_yds',
                               'player_id':'id', 'target_share':'tgt_share'})
    data['TD'] = data['rec_td'] + data['rush_td']
    data['YPC'] = data['rush_yds']/data['carries']
    data_ = data.reset_index()
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    if type is not None:
        df1 = data_[['player','season', 'team', 'pos', 'YPC', 'id']]
        df2 = data_[['id','team','carries', 'rush_yds', 'rush_td', 
                    'first_downs', 'epa', 'rec','rec_yds', 'rec_td',
                    'points', 'TD', 'tgt_share']] 
        data = pd.merge(df1, df2, on=['id', 'team'], how='inner')
        num_cols = ['carries', 'rush_yds', 'rush_td', 
                    'first_downs', 'epa', 'rec','rec_yds', 'rec_td',
                    'points', 'TD', 'tgt_share']
        data[num_cols] = data[num_cols].div(17)
        data.set_index('player', inplace=True)
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)    
    return data










