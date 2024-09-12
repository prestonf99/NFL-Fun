import seasonal_helper as sh
import nfl_data_py as nfl
import pandas as pd
import week_to_week as wk
import warnings
warnings.simplefilter('ignore')

def wr_comp(week):
    raw = wk.wide_receiver([week])
    raw = raw.rename(columns={'tgts':'wk tgts','rec':'wk rec', 'pct_rec':'wk % rec','tgt_share':'wk tgt %',
                              'yds':'wk yds', 'points':'wk points', 'air_yds':'wk airyds', 'wopr':'wk wopr',
                              'rec_epa':'wk epa'})
    raw = raw.drop(columns={'yds_ac','pct_yac','racr'})
    ann = sh.wr_annual([2023], type='')
    data = ann.rename(columns={'tgts':'Avg tgts','rec':'Avg rec','rec_yds':'Avg RecYds','air_yds_share':'Avg AirYds',
                               'epa':'Avg EPA','wopr_x':'Avg wopr','points':'Avg Points', '% rec':'Avg % Rec',
                              'tgt_share':'Avg Tgt %'})
    data = data.drop(columns=['tds','fum','rec_yac','air_yds'])
    merged = pd.merge(data, raw, on='id',how='inner')
    data_reset = data.reset_index()
    merged = pd.merge(merged, data_reset[['id', 'player']], left_on='id', right_on='id', how='left')
    merged = merged.rename(columns={'player_y':'player'})
    merged.set_index('player', inplace=True)
    merged = merged.drop(columns=['id', 'position','week', 'season'])
    df = merged
    df = df.sort_values('wk points', ascending=False)
    data = df[['pos', 'team','Avg tgts', 'wk tgts', 'Avg rec', 'wk rec', 'Avg % Rec', 'wk % rec', 
             'Avg RecYds', 'wk yds', 'Avg AirYds', 'wk airyds', 'Avg EPA', 'wk epa',
             'Avg wopr', 'wk wopr', 'Avg Points', 'wk points', 'Avg Tgt %', 'wk tgt %']]
    return data

def wr_usage(week):
    data = wr_comp(week)
    data = data.sort_values('wk tgts', ascending=False)
    data['Tgt Diff'] = ((data['wk tgts'] - data['Avg tgts']) / data['Avg tgts']) * 100
    data['Air Yards diff'] = ((data['wk airyds'] - data['Avg AirYds']) / data['Avg AirYds']) * 100
    data['Team Tgt Share Chg'] = ((data['wk tgt %'] - data['Avg Tgt %']) / data['Avg Tgt %']) * 100
    data =data[['team','Tgt Diff','Air Yards diff','Team Tgt Share Chg',
                'wk points']]
    data = data.rename(columns={'wk points':'Fantasy Points'})
    data = data.reset_index()

    styled_data = data.style \
        .background_gradient(cmap='RdYlGn', subset=['Tgt Diff', 'Team Tgt Share Chg', 'Air Yards diff'], vmin=-100, vmax=100) \
        .background_gradient(cmap='RdYlGn', subset=['Fantasy Points'], vmin=0, vmax=20) \
        .applymap(lambda _: 'background-color: grey', subset=['player', 'team']) \
        .format({
            'Tgt Diff': '{:.1f}%',             # Display as percentage with 0 decimal places
            'Air Yards diff': '{:.1f}%',       # Display as percentage with 0 decimal places
            'Team Tgt Share Chg': '{:.1f}%',    # Display as percentage with 0 decimal places
            'Fantasy Points': '{:.2f}'            # Keep Fantasy Points as float with 2 decimal places
        }) \
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', 'grey'), ('color', 'black'), ('font-weight', 'bold'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('padding', '5px')]}  # Optional: add padding to table cells
        ])

    print(f"Differences vs. 2023 Season Average. Week {week} Data.")
    return styled_data


def wr_performance(week):
    data = wr_comp(week)
    data = data.sort_values('wk yds', ascending=False)
    data['Rec Diff'] = ((data['wk rec'] - data['Avg rec']) / data['Avg rec']) * 100
    data['Yds Diff'] = ((data['wk yds'] - data['Avg RecYds']) / data['Avg RecYds']) * 100
    data['EPA Diff'] = ((data['wk epa'] - data['Avg EPA']) / data['Avg EPA']) * 100
    data['WOPR Diff'] = ((data['wk wopr'] - data['Avg wopr']) / data['Avg wopr'] ) * 100
    data['Points Diff'] = ((data['wk points'] - data['Avg Points']) / data['Avg Points']) * 100
    data = data.rename(columns={'wk rec':'Receptions', 'wk yds':'Receiving Yards','wk epa':'Weeks EPA',
                                'wk wopr':'WOPR', 'wk points':'Fantasy Points'})
    data = data[['team','Receptions', 'Rec Diff', 'Receiving Yards', 'Yds Diff', 'Weeks EPA', 'EPA Diff',
                 'WOPR', 'WOPR Diff', 'Fantasy Points', 'Points Diff']]
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    data = data.reset_index()
    styled_data = data.style \
        .background_gradient(cmap='RdYlGn', subset=['Rec Diff','Yds Diff', 'EPA Diff',
                                                    'WOPR Diff'], vmin=-100, vmax=100) \
        .background_gradient(cmap='RdYlGn', subset=['Receiving Yards'], vmin=0, vmax=150) \
        .background_gradient(cmap='RdYlGn', subset=['Points Diff'], vmin=-40, vmax=150) \
        .background_gradient(cmap='RdYlGn', subset=['WOPR'], vmin=0, vmax=1) \
        .background_gradient(cmap='RdYlGn', subset=['Receptions'], vmin=0, vmax=7) \
        .background_gradient(cmap='RdYlGn', subset=['Weeks EPA'], vmin=-4, vmax=8) \
        .background_gradient(cmap='RdYlGn', subset=['Fantasy Points'], vmin=0, vmax=24) \
        .applymap(lambda _: 'background-color: grey', subset=['player', 'team']) \
        .format({
            'Rec Diff': '{:.1f}%', 'Yds Diff': '{:.1f}%','EPA Diff': '{:.1f}%', 'WOPR Diff': '{:.1f}%',
            'Points Diff': '{:.1f}%','Fantasy Points':'{:.2f}','Receiving Yards':'{:.2f}','Weeks EPA':'{:.2f}',
            'WOPR':'{:.2f}',
        }) \
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', 'grey'), ('color', 'black'), 
                                               ('font-weight', 'bold'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('padding', '5px')]} 
        ])

    print(f"Differences vs. 2023 Season Average. Week {week} Data.")
    
    return styled_data

def rb_comp(week):
    raw = wk.running_back([week])
    raw = raw.rename(columns={'carries':f'W{week} Carries','rush_yds':f'W{week} RushYd',
                              'rec_yds':f'W{week} RecYd','yds_total':f'W{week} Yards',
                              'YPC':f'W{week} YPC','tgt_share':f'W{week} TGT%',
                              'points':f'W{week} Points', 'EPA':f'W{week} EPA',
                             'receptions':f'W{week}Rec'})
    raw[f'W{week} Carries'] = raw[f'W{week} Carries'].astype('float64')
    year = 23
    data = sh.rb_annual([2023], type='')
    data = data.drop(columns={'rush_td', 'first_downs', 'rec_td','TD', 'team'})
    data[f'{year} Yds/Gm'] = data['rush_yds'] + data['rec_yds'] 
    data = data.rename(columns={'YPC':f'{year} YPC', 'carries':f'{year} Car/Gm',
                               'rush_yds':f'{year} RushYd/Gm','epa':f'{year} EPA',
                               'rec':f'{year} Rec/Gm', 'rec_yds':f'{year} RecYd/Gm',
                               'points':f'{year} PPG', 'tgt_share':f'{year} TGT%'})
    merged = pd.merge(data, raw, on=['id'], how='inner')
    data_reset = data.reset_index()
    merged = pd.merge(merged, data_reset[['id', 'player']], left_on='id',right_on='id',how='left')
    merged = merged.rename(columns={'player_y':'player'})
    merged.set_index('player', inplace=True)
    merged = merged.drop(columns=['id', 'position', 'player_x','season'])
    merged = merged.sort_values('W1 Points', ascending=False)
    data = merged[['pos', 'recent_team', '23 YPC', 'W1 YPC', '23 Car/Gm','W1 Carries', '23 RushYd/Gm',
                   'W1 RushYd', '23 RecYd/Gm', 'W1 RecYd', '23 Yds/Gm', 'W1 Yards', '23 PPG',
                  'W1 Points', '23 TGT%', 'W1 TGT%', '23 EPA', 'W1 EPA']]
    data = data.rename(columns={'recent_team':'team'})
    
    return data

def rb_usage(week):
    data = rb_comp(week)
    year = 23
    data = data.sort_values(f'W{week} Carries', ascending=False)
    data['Car. Dif'] = ((data[f'W{week} Carries'] - 
                         data[f'{year} Car/Gm']) / data[f'{year} Car/Gm']) * 100
    data['RecYd Dif'] = ((data[f'W{week} RecYd'] - 
                     data[f'{year} RecYd/Gm']) / data[f'{year} RecYd/Gm']) * 100
    data['TGT% Dif'] = ((data[f'W{week} TGT%'] - 
                 data[f'{year} TGT%']) / data[f'{year} TGT%']) * 100
    data['EPA Dif'] = ((data[f'W{week} EPA'] - 
             data[f'{year} EPA']) / abs(data[f'{year} EPA'])) * 100
    data[f'W{week} TGT%'] = data[f'W{week} TGT%'] * 100
    data = data[['team', f'W{week} Carries', 'Car. Dif', f'W{week} RecYd',
                 'RecYd Dif', f'W{week} TGT%', 'TGT% Dif', f'W{week} EPA', 'EPA Dif',
                 f'W{week} Points']]
    data = data.reset_index()
    data = data.style \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} Carries', f'W{week} Points'], vmin=0, vmax=25) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} RecYd'], vmin=10, vmax=50) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} TGT%'], vmin=5, vmax=24) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} EPA'], vmin=-5, vmax=5) \
        .background_gradient(cmap='RdYlGn', subset=['Car. Dif', 'RecYd Dif', 'TGT% Dif'], vmin=-100, vmax=100) \
        .background_gradient(cmap='RdYlGn', subset=['EPA Dif'], vmin=-400, vmax=400) \
        .applymap(lambda _: 'background-color: grey', subset=['player', 'team']) \
        .format({f'W{week} Carries': '{:.1f}', 'Car. Dif':'{:.1f}%', 'RecYd Dif':'{:.1f}%',
                 'TGT% Dif':'{:.1f}%', 'EPA Dif':'{:.1f}%',f'W{week} RecYd': '{:.1f}',
                 f'W{week} TGT%': '{:.1f}%', f'W{week} Points': '{:.1f}',
                 f'W{week} EPA': '{:.1f}'
                }) \
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', 'grey'), ('color', 'black'), 
                                               ('font-weight', 'bold'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('padding', '5px')]} 
        ])
    print(f"Differences vs. 2023 Season Average, Week {week} Data.")

    return data

def rb_performance(week):
    data = rb_comp(week)
    year = 23
    data = data.sort_values(f'W{week} Points', ascending=False)
    data['Points Diff'] = ((data[f'W{week} Points'] - 
                            data[f'{year} PPG']) / (data[f'{year} PPG'])) * 100
    data['RushYd Diff'] = ((data[f'W{week} RushYd'] - 
                            data[f'{year} RushYd/Gm']) / (data[f'{year} RushYd/Gm'])) * 100
    data['Yards Diff'] = ((data[f'W{week} Yards'] - 
                            data[f'{year} Yds/Gm']) / (data[f'{year} Yds/Gm'])) * 100
    data['YPC Diff'] = ((data[f'W{week} YPC'] - 
                            data[f'{year} YPC']) / (data[f'{year} YPC'])) * 100
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    data = data[['team',f'W{week} YPC', 'YPC Diff', f'W{week} RushYd', 'RushYd Diff', 
               f'W{week} Yards', 'Yards Diff', f'W{week} Points', 'Points Diff']]
    data = data.reset_index()
    styled_data = data.style \
        .background_gradient(cmap='RdYlGn', subset=['YPC Diff'], vmin=-35, vmax=30) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} YPC'], vmin=0, vmax=7) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} RushYd',f'W{week} Yards'],vmin=0, vmax=150) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} Points'], vmin=0, vmax=25) \
        .background_gradient(cmap='RdYlGn', subset=['RushYd Diff', 'Yards Diff', 'Points Diff'], vmin=-100, vmax=100) \
        .applymap(lambda _: 'background-color: grey', subset=['player', 'team']) \
        .format({'RushYd Diff':'{:.1f}%','Yards Diff':'{:.1f}%','Points Diff':'{:.1f}%',
                 'YPC Diff':'{:.1f}%', f'W{week} YPC':'{:.1f}', f'W{week} RushYd':'{:.1f}',
                 f'W{week} RushYd':'{:.1f}', f'W{week} Yards':'{:.1f}',f'W{week} Points':'{:.1f}'
                
                }) \
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', 'grey'), ('color', 'black'), 
                                               ('font-weight', 'bold'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('padding', '5px')]} 
        ])

    return styled_data


def te_comp(week):
    year = 23
    raw = wk.tight_end([week])
    raw = raw.rename(columns={'tgts':f'W{week} Tgts', 'rec':f'W{week} Rec', 'tgt_share':f'W{week} Tgt Share',
                              'pct_rec':f'W{week} % Rec', 'yds':f'W{week} Yds','points':f'W{week} Points', 
                              'air_yds':f'W{week} AirYds %','wopr':f'W{week} WOPR','rec_epa':f'W{week} EPA'})
    raw = raw.drop(columns={'yds_ac', 'pct_yac', 'racr'})
    data = sh.te_annual([2023], type='')
    data = data.rename(columns={'tgts':f'{year} Tgts/Wk', 'rec':f'{year} Rec/Wk', 'tgt_share':f'{year} Tgt Share',
                                '% rec':f'{year} % Rec', 'rec_yds':f'{year} Yds/Wk', 'points':f'{year} PPG',
                                'air_yds_share':f'{year} AirYds %', 'wopr_x':f'{year} WOPR', 'epa':f'{year} EPA'})
    data = data.reset_index()
    merged = pd.merge(data, raw, on='id', how='inner')
    data = merged.drop(columns={'player_y', 'id', 'season', 'pos','tds','fum', 'position'})
    data = data.rename(columns={'player_x':'player'})
    data.set_index('player', inplace=True)
    data = data[['team', f'{year} Tgts/Wk', f'W{week} Tgts',f'{year} Rec/Wk', f'W{week} Rec',f'{year} Yds/Wk',
                 f'W{week} Yds',f'{year} EPA', f'W{week} EPA',f'{year} Tgt Share', f'W{week} Tgt Share',
                 f'{year} AirYds %', f'W{week} AirYds %',f'{year} WOPR', f'W{week} WOPR',f'{year} PPG',
                 f'W{week} Points',f'{year} % Rec', f'W{week} % Rec']]
    
    return data


def te_usage(week):
    year = 23
    data = te_comp(week)
    data = data.sort_values(f'W{week} Points', ascending=False)
    data['Tgt Diff'] = ((data[f'W{week} Tgts'] - 
                        data[f'{year} Tgts/Wk']) / data[f'{year} Tgts/Wk']) * 100
    data['Rec Diff'] = ((data[f'W{week} Rec'] - 
                    data[f'{year} Rec/Wk']) / data[f'{year} Rec/Wk']) * 100
    data['Share Diff'] = ((data[f'W{week} Tgt Share'] - 
                    data[f'{year} Tgt Share']) / data[f'{year} Tgt Share']) * 100
    data['AirYds Diff'] = ((data[f'W{week} AirYds %'] - 
                    data[f'{year} AirYds %']) / data[f'{year} AirYds %']) * 100
    data = data[['team', f'W{week} Tgts', 'Tgt Diff', f'W{week} Rec', 'Rec Diff',
                 f'W{week} Tgt Share', 'Share Diff', f'W{week} AirYds %',
                'AirYds Diff', f'W{week} Points']]
    data_ = data.sort_values(f'W{week} Points')
    data_ = data.reset_index()
    styled_data = data_.style \
        .background_gradient(cmap='RdYlGn', subset=['Tgt Diff', 'Rec Diff',
                                                    'Share Diff', 'AirYds Diff'], vmin=-100, vmax=100) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} Tgts',f'W{week} Rec'], vmin=1, vmax=8) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} Tgt Share',f'W{week} AirYds %'], vmin=0, vmax=0.35) \
        .background_gradient(cmap='RdYlGn', subset=[f'W{week} Points'], vmin=0, vmax=15) \
        .applymap(lambda _: 'background-color: grey', subset=['player', 'team']) \
        .format({'Tgt Diff':'{:.1f}%', 'Rec Diff':'{:.1f}%', 'Share Diff':'{:.1f}%',
                f'W{week} Tgt Share':'{:.1%}', f'W{week} AirYds %':'{:.1%}',
                'AirYds Diff':'{:.1f}%', f'W{week} Points':'{:.2f}'
                }) \
        .set_table_styles([
                    {'selector': 'thead th', 'props': [('background-color', 'grey'), ('color', 'black'), 
                                                       ('font-weight', 'bold'), ('text-align', 'center')]},
                    {'selector': 'td', 'props': [('padding', '5px')]} 
                ])

    return styled_data

