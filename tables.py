import seasonal_helper as sh
import nfl_data_py as nfl
import pandas as pd
import week_to_week as wk
import warnings
warnings.simplefilter('ignore')

def wr_comp(week):
    raw = wk.wide_receiver([1])
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


