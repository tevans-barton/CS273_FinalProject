import pandas as pd
import numpy as np

def get_data():
    # Read in raw data
    tourney = pd.read_csv('data/raw/MNCAATourneyCompactResults.csv')
    reg_season = pd.read_csv('data/raw/MRegularSeasonDetailedResults.csv')
    teams = pd.read_csv('data/raw/MTeams.csv')

    #Clean regular season stats
    reg_season_stats = clean_regular_season(reg_season)

    #Just look at games from the first round
    round1_tourney = tourney[tourney['DayNum'].isin([136,137])].reset_index(drop = True)

    #Merge regular season stats with tournery winners, and classify those as 1s
    tourney_winners = round1_tourney[['Season', 'WTeamID']].merge(reg_season_stats, left_on = ['Season', 'WTeamID'], right_on = ['Season', 'TeamID'], how = 'inner')
    tourney_winners['Target'] = 1

    #Merge regular season stats with tourney losers, and classify those as 0s
    tourney_losers = round1_tourney[['Season', 'LTeamID']].merge(reg_season_stats, left_on = ['Season', 'LTeamID'], right_on = ['Season', 'TeamID'], how = 'inner')
    tourney_losers['Target'] = 0

    #Drop unnecessary columns
    tourney_winners = tourney_winners.drop('WTeamID', axis = 1)
    tourney_losers = tourney_losers.drop('LTeamID', axis = 1)

    #Combine data vertically
    data = pd.concat([tourney_winners, tourney_losers])
    data = data.reset_index(drop = True)
    
    #Get team names for easier identification
    data['Team'] = data['TeamID'].map(teams.set_index('TeamID')['TeamName'].to_dict())
    data = data[['Team', 'TeamID', 'Season', 'Points', 'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM','FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF', 'Games', 'Target']]
    data.to_csv('data/final.csv', index = False)
    return data

def clean_regular_season(df):
    #Grab winning and losing data separately
    wins = df[['Season', 'WTeamID', 'WScore', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']]
    losses = df[['Season', 'LTeamID', 'LScore', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']]

    #Rename columns
    wins.columns = ['Season', 'TeamID', 'Score', 'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF']
    losses.columns = ['Season', 'TeamID', 'Score', 'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF']

    #Group and sum to get all of the teams total stats for the year
    w_grouped = wins.groupby(['Season', 'TeamID']).aggregate(['sum', 'count'])
    l_grouped = losses.groupby(['Season', 'TeamID']).aggregate(['sum', 'count'])
    w_grouped.columns = ['_'.join(map(str, col)) for col in w_grouped.columns.values]
    l_grouped.columns = ['_'.join(map(str, col)) for col in l_grouped.columns.values]
    w_grouped = w_grouped[['Score_sum', 'FGM_sum', 'FGA_sum', 'FGM3_sum', 'FGA3_sum', 'FTM_sum', 'FTA_sum', 'OR_sum','DR_sum', 'Ast_sum', 'TO_sum', 'Stl_sum', 'Blk_sum', 'PF_sum', 'PF_count']]
    w_grouped.columns = ['Points', 'FGM', 'FGA', 'FGM3', 'FGA3','FTM', 'FTA', 'OR','DR', 'Ast', 'TO','Stl', 'Blk', 'PF', 'Games']
    l_grouped = l_grouped[['Score_sum', 'FGM_sum', 'FGA_sum', 'FGM3_sum', 'FGA3_sum', 'FTM_sum', 'FTA_sum', 'OR_sum','DR_sum', 'Ast_sum', 'TO_sum', 'Stl_sum', 'Blk_sum', 'PF_sum', 'PF_count']]
    l_grouped.columns = ['Points', 'FGM', 'FGA', 'FGM3', 'FGA3','FTM', 'FTA', 'OR','DR', 'Ast', 'TO','Stl', 'Blk', 'PF', 'Games']
    reg_season_stats = w_grouped.add(l_grouped, fill_value = 0)
    reg_season_stats = reg_season_stats.reset_index(drop = False)
    reg_season_stats = reg_season_stats.dropna().reset_index(drop = True)

    #Make all stats per game
    for c in ['Points', 'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF']:
        reg_season_stats[c] = reg_season_stats[c] / reg_season_stats['Games']

    return reg_season_stats
    
