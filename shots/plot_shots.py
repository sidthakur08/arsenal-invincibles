import pandas as pd
import matplotlib.pyplot as plt
import FCPython
from remove_string import convert_to_int
import numpy as np
from ast import literal_eval
import warnings
warnings.filterwarnings("ignore")

# setting the dimension of the pitch (default)
pitchX = 120
pitchY = 80

# plotting the shots for one team
def plot_shots_arsenal(shots,c,against):
    (fig,ax) = FCPython.createPitch(pitchX,pitchY,'yards','black')
    plt.figure(figsize=(12,8))
    for i,shot in shots.iterrows():
        x = shot['location'][0]
        y = shot['location'][1]
        goal = shot['shot_outcome_name'] == 'Goal'
        team_name = shot['team_name']
        circle_size =  np.sqrt(shot['shot_statsbomb_xg']*15)
        if goal:
            shot_circle = plt.Circle((pitchX-x,y),color=c,radius=circle_size)
            #plt.text((x+1),(pitchY-y+1),shot['player_name'])
            label_text = f"{shot['player_name']}({np.round(shot['shot_statsbomb_xg'],decimals=3)})"
            ax.annotate(label_text,(pitchX-x-10,y+2))
        else:
            shot_circle = plt.Circle((pitchX-x,y),color=c,radius=circle_size)
            shot_circle.set_alpha(.2)
        ax.add_patch(shot_circle)
    ax.set_title(f'{team_name} vs {against}')
    return (fig,ax)

# plotting the shots for both the teams on one pitch
def plot_shots_two(shots,home_team,away_team):
    (fig,ax) = FCPython.createPitch(pitchX,pitchY,'yards','black')
    plt.figure(figsize=(12,8))
    for i,shot in shots.iterrows():
        x = shot['location'][0]
        y = shot['location'][1]
        goal = shot['shot_outcome_name'] == 'Goal'
        team_name = shot['team_name']
        circle_size =  np.sqrt(shot['shot_statsbomb_xg']*15)
        if home_team.lower()=='arsenal':
            home_c = 'red'
            away_c = 'blue'
        else:
            home_c = 'blue'
            away_c = 'red'
        if (home_team.lower() == team_name.lower()):
            if goal:
                shot_circle_home = plt.Circle((x,pitchY-y),color=home_c,radius=circle_size)
                #plt.text((x+1),(pitchY-y+1),shot['player_name'])
                label_text = f"{shot['player_name']}({np.round(shot['shot_statsbomb_xg'],decimals=3)})"
                ax.annotate(label_text,(x-10,pitchY-y+2))
            else:
                shot_circle_home = plt.Circle((x,pitchY-y),color=home_c,radius=circle_size)
                shot_circle_home.set_alpha(.2)
            ax.add_patch(shot_circle_home)
        elif (away_team.lower() == team_name.lower()):
            if goal:
                shot_circle_away = plt.Circle((pitchX-x,y),color=away_c,radius=circle_size)
                label_text = f"{shot['player_name']}({np.round(shot['shot_statsbomb_xg'],decimals=3)})"
                ax.annotate(label_text,(pitchX-x-10,y+2))
            else:
                shot_circle_away = plt.Circle((pitchX-x,y),color=away_c,radius=circle_size)
                shot_circle_away.set_alpha(.2)
            ax.add_patch(shot_circle_away)
    title = f'{home_team.upper()} vs {away_team.upper()}'
    ax.set_title(title)
    ax.legend([shot_circle_home,shot_circle_away],[home_team.capitalize(),away_team.capitalize()],loc=1)
    return (fig,ax)

# getting the matches data for the season
MATCH_FILENAME = f'/Users/sidthakur08/GitHub/arsenal-invincibles/data/matches.csv'
match_data = pd.read_csv(MATCH_FILENAME)
weeks = match_data['match_week'].values
count = 0

# iterating through the gameweeks
for GAMEID in weeks:
    try:
        print(f'getting gameweek {GAMEID}')
        # two fixtures were present in gameweek 35 ,i.e., tottenham and birmingham
        if GAMEID == 35:
            if count == 0:
                count = 1
                print("Getting first match for gameweek 35")
                EVENT_FILENAME = f'/Users/sidthakur08/Github/arsenal-invincibles/data/games/Arsenal-{GAMEID}.csv'
                home_team = match_data[match_data['match_week']==GAMEID]['home_team_home_team_name'].values[0]
                away_team = match_data[match_data['match_week']==GAMEID]['away_team_away_team_name'].values[0]
            else:
                print("Getting second match for gameweek 35")
                EVENT_FILENAME = f'/Users/sidthakur08/Github/arsenal-invincibles/data/games/Arsenal-{GAMEID}_1.csv'
                home_team = match_data[match_data['match_week']==GAMEID]['home_team_home_team_name'].values[1]
                away_team = match_data[match_data['match_week']==GAMEID]['away_team_away_team_name'].values[1]
        else:
            EVENT_FILENAME = f'/Users/sidthakur08/Github/arsenal-invincibles/data/games/Arsenal-{GAMEID}.csv'
            home_team = match_data[match_data['match_week']==GAMEID]['home_team_home_team_name'].values[0]
            away_team = match_data[match_data['match_week']==GAMEID]['away_team_away_team_name'].values[0]
        
        # reading the event data for the match
        event_data = pd.read_csv(EVENT_FILENAME)
        
        # getting the shots data
        shots = event_data[event_data['type_name']=='Shot']
        shots = shots.dropna(axis=1).reset_index(drop=True)
        shots['location'] = convert_to_int(shots['location'])

        # getting shots by arsenal
        arsenal_shots = shots[shots['team_name']=='Arsenal']

        # getting the team facing arsenal
        ag = home_team if away_team == 'Arsenal' else away_team

        # calling functions to plot the shots
        fig1,ax = plot_shots_arsenal(arsenal_shots,'red',against= ag)
        fig2,ax = plot_shots_two(shots,home_team,away_team)

        # saving the plots
        print(f'saving gameweek {GAMEID}')
        fig1.savefig(f'/Users/sidthakur08/Github/arsenal-invincibles/shots/game_shots/arsenal/vs {ag} - {GAMEID}.pdf')
        fig2.savefig(f'/Users/sidthakur08/Github/arsenal-invincibles/shots/game_shots/game/{home_team.capitalize()} vs {away_team.capitalize()} - {GAMEID}.pdf')
    except Exception as e:
        print(f"passing gameweek {GAMEID}")
        print(str(e))
        pass