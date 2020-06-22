import pandas as pd
import matplotlib.pyplot as plt
import warnings
import numpy as np
import seaborn as sns
warnings.filterwarnings('ignore')
sns.set(color_codes=True)


def plot_xgcount(data1,data2,team1,team2,GAMEID,hteam,ateam):
    fig,ax = plt.subplots(figsize=(12,7))
    shot_len1 = len(data1['shot_count'])
    shot_len2 = len(data2['shot_count'])
    max_shot_count =  shot_len1 if (shot_len1 > shot_len2) else shot_len2
    xticks = range(max_shot_count+2)
    yticks = np.arange(0.0,1.1,0.1)
    yrange = (yticks[0], yticks[-1])
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_ylim(yrange)
    ax.plot(data1['shot_count'],data1['shot_statsbomb_xg'],'o-',c='tomato',label=f'{team1}')
    ax.plot(data2['shot_count'],data2['shot_statsbomb_xg'],'o-',c='cornflowerblue',label=f'{team2}')
    for i,row in data1.iterrows():
        if row['shot_outcome_name'] == 'Goal':
            ax.text(row['shot_count']+0.1,row['shot_statsbomb_xg']+0.04,s=f'{team1} Scores')
    for i,row in data2.iterrows():
        if row['shot_outcome_name'] == 'Goal':
            ax.text(row['shot_count']+0.1,row['shot_statsbomb_xg']+0.04,s=f'{team2} Scores')
    ax.legend([f'{team1}',f'{team2}'])
    ax.set_xlabel('Shot Count')
    ax.set_ylabel('xG')
    ax.set_title(f'{hteam} vs {ateam}')

    return fig,ax


MATCH_FILE = "/Users/sidthakur08/Github/arsenal-invincibles/data/matches.csv"
match_data = pd.read_csv(MATCH_FILE)
weeks = match_data['match_week'].values
count = 0


for GAMEID in weeks:
    try:
        print(f"Getting gameweek {GAMEID}")

        if GAMEID == 35:
            if count == 0:
                EVENT_FILE = f"/Users/sidthakur08/Github/arsenal-invincibles/data/games/Arsenal-{GAMEID}.csv"
                home_team = match_data[match_data['match_week']==GAMEID]['home_team_home_team_name'].values[0]
                away_team = match_data[match_data['match_week']==GAMEID]['away_team_away_team_name'].values[0]
                count = 1
            else:
                EVENT_FILE = f"/Users/sidthakur08/Github/arsenal-invincibles/data/games/Arsenal-{GAMEID}_1.csv"
                home_team = match_data[match_data['match_week']==GAMEID]['home_team_home_team_name'].values[1]
                away_team = match_data[match_data['match_week']==GAMEID]['away_team_away_team_name'].values[1]
        else:
            EVENT_FILE = f"/Users/sidthakur08/Github/arsenal-invincibles/data/games/Arsenal-{GAMEID}.csv"
            home_team = match_data[match_data['match_week']==GAMEID]['home_team_home_team_name'].values[0]
            away_team = match_data[match_data['match_week']==GAMEID]['away_team_away_team_name'].values[0]

        gdata = pd.read_csv(EVENT_FILE)
        
        team1 = 'Arsenal'
        team2 = home_team if away_team == 'Arsenal' else away_team

        team1_shots = gdata[(gdata['type_name']=='Shot') & (gdata['team_name']==team1)].dropna(axis=1).reset_index(drop=True)
        team2_shots = gdata[(gdata['type_name']=='Shot') & (gdata['team_name']==team2)].dropna(axis=1).reset_index(drop=True)

        plot_team1 = pd.DataFrame(team1_shots,columns=['shot_outcome_name','shot_statsbomb_xg'])
        plot_team1['shot_count'] = [i+1 for i in range(len(team1_shots))]
        plot_team2 = pd.DataFrame(team2_shots,columns=['shot_outcome_name','shot_statsbomb_xg'])
        plot_team2['shot_count'] = [i+1 for i in range(len(team2_shots))]

        c1 = 0
        for i in plot_team1['shot_outcome_name']:
            if i == 'Goal':
                plot_team1.loc[count,'shot_if_goal'] = 1
            else:
                plot_team1.loc[count,'shot_if_goal'] = 0
            c1+=1

        c2 = 0
        for i in plot_team2['shot_outcome_name']:
            if i == 'Goal':
                plot_team2.loc[count,'shot_if_goal'] = 1
            else:
                plot_team2.loc[count,'shot_if_goal'] = 0
            c2+=1

        fig,ax = plot_xgcount(plot_team1,plot_team2,team1,team2,GAMEID,home_team,away_team)
        fig.savefig(f"/Users/sidthakur08/Github/arsenal-invincibles/performance/shots-wise/xGvsCount/{team1}vs{team2}-{GAMEID}.pdf")
    except Exception as e:
        print(e)