import pandas as pd
import os
import math

# use stats from elden ring
COLUMNS = ['name', 'level', 'vigor', 'mind', 'endurance', 'strength', 'dexterity', 'intelligence', 'faith', 'arcane']
EQUIPMENT_COLUMNS = ['weapon', 'armor', 'accessory']

def setup(server_id):
    # setup database for server that is used to track player data using pandas
    server_path = os.path.join('data', server_id)
    if os.path.exists(server_path):
        print('Database already exists for server:', server_id)
        return
    
    # create folder for server
    os.makedirs(server_path)
    
    dataframe = pd.DataFrame(columns=COLUMNS + EQUIPMENT_COLUMNS)
    
    # Initialize derived columns with default values
    dataframe['max_stamina'] = 0
    dataframe['max_hp'] = 0
    dataframe['max_fp'] = 0
    
    # Initialize equipment columns with default values
    dataframe['weapon'] = ''
    dataframe['armor'] = ''
    dataframe['accessory'] = ''
    
    # save dataframe to csv
    save_dataframe(server_path, dataframe)
    
    print('Database created for server:', server_id)
    print('Database saved to:', os.path.join(server_path, 'players.csv'))

def load_player_data(server_id):
    server_path = os.path.join('data', server_id)
    if not os.path.exists(server_path):
        print('Database does not exist for server:', server_id)
        return None, None
    
    dataframe = pd.read_csv(os.path.join(server_path, 'players.csv'))
    return server_path, dataframe

def player_exists(dataframe, player_name):
    return player_name in dataframe['name'].values

def save_dataframe(server_path, dataframe):
    dataframe.to_csv(os.path.join(server_path, 'players.csv'), index=False)

def add_player(server_id, player_name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane):
    # add player to database
    server_path, dataframe = load_player_data(server_id)
    if dataframe is None:
        return
    
    # check if player already exists
    if player_exists(dataframe, player_name):
        print('Player already exists in database:', player_name)
        return
    
    new_player = pd.DataFrame([[player_name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane, '', '', '']], columns=COLUMNS + EQUIPMENT_COLUMNS)
    
    # Calculate derived columns
    new_player['max_stamina'] = math.floor(80 + 25 * ((endurance - 1.0) / 14))
    new_player['max_hp'] = math.floor(300 + 500 * (((vigor - 1.0) / 24) ** 1.5))
    new_player['max_fp'] = math.floor(50 + 45 * ((mind - 1.0) / 14))
    
    dataframe = pd.concat([dataframe, new_player], ignore_index=True)
    
    # save dataframe to csv
    save_dataframe(server_path, dataframe)
    
    print('Player added to database:', player_name)

def remove_player(server_id, player_name):
    # remove player from database
    server_path, dataframe = load_player_data(server_id)
    if dataframe is None:
        return
    
    # check if player exists
    if not player_exists(dataframe, player_name):
        print('Player does not exist in database:', player_name)
        return
    
    dataframe = dataframe[dataframe['name'] != player_name]
    
    # save dataframe to csv
    save_dataframe(server_path, dataframe)
    
    print('Player removed from database:', player_name)

def add_equipment(server_id, player_name, equipment_type, equipment_name):
    # add equipment to player
    server_path, dataframe = load_player_data(server_id)
    if dataframe is None:
        return
    
    # check if player exists
    if not player_exists(dataframe, player_name):
        print('Player does not exist in database:', player_name)
        return
    
    # update equipment
    dataframe.loc[dataframe['name'] == player_name, equipment_type] = equipment_name
    
    # save dataframe to csv
    save_dataframe(server_path, dataframe)
    
    print(f'Equipment {equipment_name} added to player {player_name} in slot {equipment_type}')

def remove_equipment(server_id, player_name, equipment_type):
    # remove equipment from player
    server_path, dataframe = load_player_data(server_id)
    if dataframe is None:
        return
    
    # check if player exists
    if not player_exists(dataframe, player_name):
        print('Player does not exist in database:', player_name)
        return
    
    # remove equipment
    dataframe.loc[dataframe['name'] == player_name, equipment_type] = ''
    
    # save dataframe to csv
    save_dataframe(server_path, dataframe)
    
    print(f'Equipment removed from player {player_name} in slot {equipment_type}')