import nfl_data_py as nfl
from pylab import mpl, plt
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '0.05'
plt.rcParams['grid.color'] = '0.25'
#plt.rcParams['axes.grid'] = True

season = 2024
s_type='REG'
def wide_receiver(week, sort=None):
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
        
    data = nfl.import_weekly_data([season], ['week', 'player_name', 'position',
                                             'targets', 'target_share','receptions','receiving_yards',
                                             'receiving_yards_after_catch', 'receiving_epa',
                                             'fantasy_points', 'air_yards_share','wopr', 'racr',
                                             'player_id'], downcast=False)
    data = data.rename(columns={'player_name':'player', 'targets':'tgts', 'target_share':'tgt_share',
                               'receptions':'rec','receiving_yards':'yds', 
                                'receiving_yards_after_catch':'yds_ac', 'fantasy_points':'points',
                               'air_yards_share':'air_yds','player_id':'id', 'receiving_epa':'rec_epa'})
    data['pct_yac'] = (data['yds_ac']/data['yds'])
    data['pct_rec'] = data['rec'] / data['tgts']
    data = data[['week', 'player', 'position', 'tgts',  'rec', 'pct_rec', 'tgt_share', 
                 'yds', 'yds_ac', 'pct_yac', 'points','rec_epa', 'air_yds', 'wopr', 'racr','id']]
    pos = ['WR']
    data = data[data['position'].isin(pos)]
    wk = week
    data = data[data['week'].isin(wk)]
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

    if sort is not None:
        data = data.sort_values(sort, ascending=False)
        pos = ['WR']
        data = data[data['position'].isin(pos)]
        wk = week
        data = data[data['week'].isin(wk)]
        data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
        data.set_index('week', inplace=True)

    

    return data

def tight_end(week, sort=None):
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    data = nfl.import_weekly_data([season], ['week', 'player_name', 'position',
                                    'targets', 'target_share','receptions','receiving_yards',
                                    'receiving_yards_after_catch', 'fantasy_points','air_yards_share',
                                    'wopr', 'racr', 'receiving_epa', 'player_id'],downcast=False)
    data = data.rename(columns={'player_name':'player', 'targets':'tgts', 'target_share':'tgt_share',
                               'receptions':'rec','receiving_yards':'yds', 
                                'receiving_yards_after_catch':'yds_ac', 'fantasy_points':'points',
                                'air_yards_share':'air_yds', 'player_id':'id','receiving_epa':'rec_epa'})
    data['pct_yac'] = (data['yds_ac']/data['yds'])
    data['pct_rec'] = data['rec'] / data['tgts']
    data = data[['week', 'player', 'position', 'tgts', 'rec','tgt_share', 'pct_rec',
                 'yds', 'yds_ac', 'pct_yac', 'points', 'air_yds','wopr', 'racr', 'rec_epa', 'id']]
    pos = ['TE']
    data = data[data['position'].isin(pos)]
    wk = week
    data = data[data['week'].isin(wk)]
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    data.set_index('week', inplace=True)
    if sort is not None:
        data = data.sort_values(sort, ascending=False)
    
    return data



def running_back(week, sort=None):
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    data = nfl.import_weekly_data([season], ['week', 'recent_team', 'player_name', 'position', 'carries',
                                             'rushing_yards', 'receiving_yards',
                                             'fantasy_points', 'target_share', 'rushing_epa',
                                             'receptions','player_id'],
                                 downcast=False)
    data = data.rename(columns={'player_name':'player', 'rushing_yards':'rush_yds', 
                                'receiving_yards':'rec_yds', 'fantasy_points':'points',
                                'target_share':'tgt_share', 'player_id':'id',
                               'rushing_epa':'EPA'})
    data['yds_total'] = data['rush_yds'] + data['rec_yds']
    data['YPC'] = data['rush_yds'] / data['carries']
    data = data[['week','player','recent_team', 'position', 'carries', 'rush_yds', 'rec_yds','yds_total',
                 'YPC','tgt_share','points','receptions','EPA','id']]
    pos = ['RB']
    data = data[data['position'].isin(pos)]
    wk = week
    data = data[data['week'].isin(wk)]
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    data.set_index('week', inplace=True)
    if sort is not None:
        data = data.sort_values(sort, ascending=False)
    
    return data

def quarterback(week, sort):
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    data = nfl.import_weekly_data([season], ['week', 'player_name', 'position','passing_yards',
                                           'passing_tds', 'interceptions', 'sack_fumbles',
                                  'rushing_yards', 'fantasy_points', 'attempts',
                                            'completions'], downcast=False)
    data = data.rename(columns={'player_name':'player', 'passing_yards':'pass_yds',
                                'passing_tds':'tds', 'interceptions':'int', 
                                'rushing_yards':'rush_yds', 'fantasy_points':'points',
                               'sack_fumbles':'fumbles', 'completions':'comp',
                               'attempts':'att'})
    data['tdto'] = data['tds']/(data['int']+data['fumbles'])
    data['comp_pct'] = data['comp'] / data['att']
    data['YPA'] = data['pass_yds'] / data['att']
    data = data[['week', 'player', 'position','comp','att', 'comp_pct','pass_yds',
                 'YPA', 'rush_yds',  'tds', 'int','fumbles','tdto','points']]
    data = data.sort_values(sort, ascending=False)
    pos = ['QB']
    data = data[data['position'].isin(pos)]
    wk = week
    data = data[data['week'].isin(wk)]
    data.set_index('week', inplace=True)
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

    return data


def rb_usage(week):
    #only need weeks
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    data = nfl.import_weekly_data([season], ['week', 'player_name', 'position', 'carries', 
                                             'targets', 'fantasy_points'], downcast=False)
    data = data.rename(columns={'player_name':'player', 'position':'pos',
                                'targets':'tgts', 'fantasy_points':'points'})
    data['usage'] = data['tgts'] + data['carries']
    data['urank'] = data['usage'].rank(method='min', ascending=False)
    data['prank'] = data['points'].rank(method='min', ascending=False)
    data = data[['week', 'player', 'pos', 'carries', 'tgts', 'usage', 'points',
                'urank', 'prank']]
    data = data.sort_values('usage', ascending=False)
    pos = ['RB']
    data = data[data['pos'].isin(pos)]
    data.set_index('week', inplace=True)
    
    return data

def plot_rb_usage(data, type, amount):
    # data input - takes data from ps.rb_usage
    # type - 'bar', 'both', or 'scatter'
    # week - integer for nfl week
    # amount - int. Number of players you want to look at. 
    week = data.index.values[:1]
    if type == 'bar':
        plt.figure(figsize=(10,6))
        plt.barh(data['player'].head(amount), data['usage'].head(amount), label='Total Usage', color='b',
                alpha=0.75)
        plt.barh(data['player'].head(amount), data['carries'].head(amount), color='m',
                alpha=0.75, label='Carries')
        plt.axvline(data['usage'].head(amount).mean(), color='black', label='Sample Mean Usage', 
                    lw=1.5, linestyle='--', alpha=0.75)
        plt.scatter(data['points'].head(amount), data['player'].head(amount), color='goldenrod', 
                    label='Fantasy Points', marker='*',zorder=5)
        plt.gca().invert_yaxis()
        plt.xticks(rotation=90)
        plt.yticks(fontsize=8.5)
        plt.xlabel('Usage')
        plt.title(f'Running Back Usage: Top {amount} Week {week}')
        plt.legend();

    if type == 'scatter':
        data['usage_z'] = (data['usage'] - data['usage'].mean())/ data['usage'].std()
        data['points_z'] = (data['points'] - data['points'].mean()) / data['points'].std()
        high_usage_points = data[(data['usage_z'] > 1) & (data['points_z'] > 1)]
        plt.figure(figsize=(10, 6))
        plt.scatter(data['urank'].head(amount), data['prank'].head(amount), label='All players')
        plt.scatter(high_usage_points['urank'], high_usage_points['prank'], color='red', label='High usage & points')
        data.head(amount).apply(lambda row: plt.text(row['urank'], row['prank'], row['player'], fontsize=8), axis=1)
        plt.title(f'RB Usage & Fantasy Points Ranks: Top {amount} Week {week}')
        plt.xlabel('Usage Rank')
        plt.ylabel('Points Rank')
        plt.legend()
        plt.grid(True);

    if type == 'both':
        plt.figure(figsize=(10, 10))
        plt.subplot(211)
        plt.barh(data['player'].head(amount), data['usage'].head(amount), label='Total Usage', color='b',
                alpha=0.75)
        plt.barh(data['player'].head(amount), data['carries'].head(amount), color='m',
                alpha=0.75, label='Carries')
        plt.axvline(data['usage'].head(amount).mean(), color='black', label='Sample Mean Usage', 
                    lw=1.5, linestyle='--', alpha=0.75)
        plt.scatter(data['points'].head(amount), data['player'].head(amount), color='goldenrod', 
                    label='Fantasy Points', marker='*',zorder=5)
        plt.gca().invert_yaxis()
        plt.xticks(rotation=90)
        plt.yticks(fontsize=8.5)
        plt.xlabel('Usage')
        plt.title(f'Running Back Usage: Top {amount} Week {week}')
        plt.legend();
        plt.subplot(212)
        data['usage_z'] = (data['usage'] - data['usage'].mean())/ data['usage'].std()
        data['points_z'] = (data['points'] - data['points'].mean()) / data['points'].std()
        high_usage_points = data[(data['usage_z'] > 1) & (data['points_z'] > 1)]
        plt.scatter(data['urank'].head(amount), data['prank'].head(amount), label='All players')
        plt.scatter(high_usage_points['urank'], high_usage_points['prank'], color='red', label='High usage & points')
        data.head(amount).apply(lambda row: plt.text(row['urank'], row['prank'], row['player'], fontsize=8), axis=1)
        plt.title(f'RB Usage & Fantasy Points Ranks: Top {amount} Week {week}')
        plt.xlabel('Usage Rank')
        plt.ylabel('Points Rank')
        plt.legend()
        plt.grid(True);
                

def plot_ypc(week, amount):
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    data = nfl.import_weekly_data([season], ['week', 'player_name', 'position', 'carries',
                                          'rushing_yards', 'receiving_yards',
                                          'fantasy_points', 'target_share'],
                                 downcast=False)
    data = data.rename(columns={'player_name':'player', 'rushing_yards':'rush_yds', 
                                'receiving_yards':'rec_yds', 'fantasy_points':'points',
                                'target_share':'tgt_share'})
    data['yds_total'] = data['rush_yds'] + data['rec_yds']
    data['YPC'] = data['rush_yds'] / data['carries']
    data = data[['week','player', 'position', 'carries', 'rush_yds', 'rec_yds','yds_total',
                 'YPC','tgt_share','points']]
    data = data.sort_values('YPC', ascending=False)
    pos = ['RB']
    data = data[data['position'].isin(pos)]
    wk = week
    data = data[data['week'].isin(wk)]
    data = data.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
    data.set_index('week', inplace=True)
    plt.figure(figsize=(10, 6))
    plt.barh(data['player'].head(amount), data['YPC'].head(amount), label='Yards Per Carry',
             color='orange')
    plt.barh(data['player'].head(amount), data['carries'].head(amount), label='Carries',
            facecolor='none', edgecolor='blue', linewidth=0.75)
    plt.barh(data['player'].head(amount), data['points'].head(amount), label='Fantasy Points',
             facecolor='red', alpha=0.25, edgecolor='none')
    plt.axvline(data['YPC'].head(amount).mean(), color='m', linestyle='--', alpha=0.75,
               label='Mean Yards Per Carry')
    plt.yticks(fontsize=8.5)
    plt.gca().invert_yaxis()
    plt.title(f'Top {amount} Running Backs Yards Per Carry Week {week}')
    plt.legend();

def wr_plots(data, type, amount):
    week = data.index.values[:1]
    if type == 'wopr':
        data = data.head(amount)
        plt.figure(figsize=(10, 6))
        plt.scatter(data['wopr'], data['points'])
        plt.xlabel('Weighted Opportunity Rating')
        plt.ylabel('Fantasy Points')
        data.apply(lambda row: plt.text(row['wopr'], row['points'], row['player'], fontsize=8.5), axis=1)
        plt.title(f'Week {week} Weighted Opportunity Rating vs. Fantasy Points (Top {amount})')
        plt.grid(True);
        print("WOPR=1.5 * Target Market Share + 0.7 * Air Yards Market Share")
        print("Measures volume, want lots of targets and high air yards. Ideally 70 or higher")
    if type == 'racr':
        data = data.head(amount)
        plt.figure(figsize=(10, 6))
        plt.scatter(data['racr'], data['points'])
        plt.xlabel('Reciever Air Conversion Yards')
        plt.ylabel('Fantasy Points')
        data.apply(lambda row: plt.text(row['racr'], row['points'], row['player'], fontsize=8.5), axis=1)
        plt.title(f'Week {week} Reciever Air Conversion Yards vs. Fantasy Points (Top {amount})')
        plt.grid(True);
        print("RACR = Recieving Yards / Air Yards")
        print("Efficient player's ratio is generally 1 or higher")
    if type == 'tgt':
        data = data.sort_values('tgt_share', ascending=False)
        data = data.head(amount)
        plt.figure(figsize=(10, 6))
        plt.scatter(data['tgt_share'], data['points'])
        data.apply(lambda row: plt.text(row['tgt_share'], row['points'], row['player'], fontsize=8.5), axis=1)
        plt.xlabel('Tgt Share (%)')
        plt.ylabel('Fantasy Points')
        plt.grid(True)
        plt.title(f'Week {week} WR Target Share & Fantasy Points - Top {amount}')


def receiver_rating(week, amount):
    if week == all:
        week = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    data = nfl.import_weekly_pfr('rec', [2024])
    data = data[['week', 'pfr_player_name', 'receiving_rat']]
    data = data.rename(columns={'pfr_player_name':'player', 'receiving_rat':'rec_rat'})
    data = data.sort_values('rec_rat', ascending=False)
    mean_value = data['rec_rat'].mean()
    data = data.head(amount)
    data.set_index('week', inplace=True)
    plt.figure(figsize=(10, 6))
    plt.barh(data['player'], data['rec_rat'], facecolor='gray', edgecolor='black')
    plt.axvline(mean_value, color='b', linestyle='--', lw=0.75, alpha=0.75, label='Mean Rec. Rating')
    plt.gca().invert_yaxis()
    plt.xlabel('Receiver Rating')
    plt.title(f'NFL Week {week}: Top {amount} Receiver PFR Rating')
    plt.legend(loc='lower right')



