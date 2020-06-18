import pandas as pd
import matplotlib.pyplot as plt
import FCPython
import numpy as np
import warnings
import remove_string
warnings.filterwarnings("ignore")

statsbombX = 120
statsbombY = 80
highburyX = 109
highburyY = 73

def plot_shots_player(shots):
    (fig,ax) = FCPython.createPitch(highburyX,highburyY,'yards','black')
    plt.figure(figsize=(12,8))
    for i,shot in shots.iterrows():
        x = shot['loc_xN']
        y = shot['loc_yN']
        goal = shot['shot_outcome_name'] == 'Goal'
        p_name = shot['player_name']
        circle_size =  np.sqrt(shot['shot_statsbomb_xg']*15)
        if goal:
            shot_circle = plt.Circle((highburyX-x,y),color='red',radius=circle_size)
        else:
            shot_circle = plt.Circle((highburyX-x,y),color='blue',radius=circle_size)
            shot_circle.set_alpha(.2)
        ax.add_patch(shot_circle)
    ax.set_title(p_name)
    return (fig,ax)

FILENAME = f"/Users/sidthakur08/GitHub/open-data/Arsenal 03:04/all_events.csv"

data = pd.read_csv(FILENAME)

shots_arsenal = data[(data['type_name']=='Shot') & (data['team_name']=='Arsenal')]
shots_arsenal = shots_arsenal.dropna(axis=1).reset_index(drop=True)
shots_arsenal['location'] = remove_string.convert_to_int(shots_arsenal['location'])
shots_arsenal['loc_x'] = [i[0] for i in shots_arsenal['location']]
shots_arsenal['loc_y'] = [i[1] for i in shots_arsenal['location']]
shots_arsenal['loc_xN'] = shots_arsenal.loc_x / statsbombX * highburyX
shots_arsenal['loc_yN'] = shots_arsenal.loc_y / statsbombY * highburyY

for p in shots_arsenal['player_name'].value_counts().keys():
    try:
        print(f"getting shots for {p}")
        player = shots_arsenal[shots_arsenal['player_name'] == p].reset_index(drop=True)
        fig,ax = plot_shots_player(player)
        print(f"saving shots for {p}")
        fig.savefig(f'/Users/sidthakur08/ML/Code/Soccer/Arsenal Invincible/shots/player_shots/goal/{p}_shots.pdf')
    except Exception as e:
        print(e)
