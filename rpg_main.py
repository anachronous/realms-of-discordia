# main logic for discord based rpg, will be called in main.py

import pandas as pd
import os
import math

# use stats from elden ring
COLUMNS = ['name', 'level', 'vigor', 'mind', 'endurance', 'strength', 'dexterity', 'intelligence', 'faith', 'arcane']

def setup(server_id):
    # setup database for server that is used to track player data using pandas
    if (server_id in os.listdir('data')):
        print('Database already exists for server: ', server_id)
        return
    # create folder for server
    os.mkdir('data/' + server_id)
    
    dataframe = pd.DataFrame(columns=COLUMNS)
    dataframe['max_stamina'] = math.floor(80 + 25*((dataframe['endurance'] - 1.0) / 14))
    dataframe['max_hp'] = math.floor(300 + 500*(((dataframe['vigor'] - 1.0) / 24)**1.5))
    dataframe['max_fp'] = math.floor(50 + 45*((dataframe['mind'] - 1.0) / 14))
    
    # save dataframe to csv
    dataframe.to_csv('data/' + server_id + '/players.csv', index=False)
    
    print('Database created for server: ', server_id)
    print('Database saved to: ', 'data/' + server_id + '/players.csv')
    
def add_player(server_id, player_name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane):
    # add player to database
    if (server_id not in os.listdir('data')):
        print('Database does not exist for server: ', server_id)
        return
    
    # load database
    dataframe = pd.read_csv('data/' + server_id + '/players.csv')
    
    # check if player already exists
    if (player_name in dataframe['name'].values):
        print('Player already exists in database: ', player_name)
        return
    
    dataframe = dataframe.concat([pd.DataFrame([[player_name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane]], columns=COLUMNS)])
    
    # save dataframe to csv
    dataframe.to_csv('data/' + server_id + '/players.csv', index=False)
    
    print('Player added to database: ', player_name)

def remove_player(server_id, player_name):
    # remove player from database
    if (server_id not in os.listdir('data')):
        print('Database does not exist for server: ', server_id)
        return
    
    # load database
    dataframe = pd.read_csv('data/' + server_id + '/players.csv')
    
    # check if player exists
    if (player_name not in dataframe['name'].values):
        print('Player does not exist in database: ', player_name)
        return
    
    dataframe = dataframe[dataframe['name'] != player_name]
    
    # save dataframe to csv
    dataframe.to_csv('data/' + server_id + '/players.csv', index=False)
    
    print('Player removed from database: ', player_name)
    
