import sqlite3
import os

def setup(server_id):
    server_path = os.path.join('data', server_id)
    if os.path.exists(server_path):
        print("Database already exists for server:", server_id)
        return
    
    os.makedirs(server_path)
    
    database_file = os.path.join(server_path, 'players.db')
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        server_id TEXT,
        name TEXT,
        level INTEGER,
        vigor INTEGER,
        mind INTEGER,
        endurance INTEGER,
        strength INTEGER,
        dexterity INTEGER,
        intelligence INTEGER,
        faith INTEGER,
        arcane INTEGER,
        weapon TEXT,
        armor TEXT,
        accessory TEXT,
        max_stamina INTEGER,
        max_hp INTEGER,
        max_fp INTEGER,
        PRIMARY KEY (server_id, name)
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print('Database setup complete for server:', server_id)

def get_database_file(server_id):
    return os.path.join('data', server_id, 'players.db')

def add_player(server_id, player_name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane):
    database_file = get_database_file(server_id)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM players WHERE server_id = ? AND name = ?', (server_id, player_name))
    if cursor.fetchone():
        print('Player already exists in database:', player_name)
        conn.close()
        return
    
    max_stamina = 80 + 25 * ((endurance - 1.0) / 14)
    max_hp = 300 + 500 * (((vigor - 1.0) / 24) ** 1.5)
    max_fp = 50 + 45 * ((mind - 1.0) / 14)
    
    cursor.execute('''
    INSERT INTO players (server_id, name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane, weapon, armor, accessory, max_stamina, max_hp, max_fp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (server_id, player_name, level, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane, '', '', '', max_stamina, max_hp, max_fp))
    
    conn.commit()
    conn.close()
    
    print('Player added to database:', player_name)

def remove_player(server_id, player_name):
    database_file = get_database_file(server_id)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM players WHERE server_id = ? AND name = ?', (server_id, player_name))
    
    conn.commit()
    conn.close()
    
    print('Player removed from database:', player_name)

def add_equipment(server_id, player_name, equipment_type, equipment_name):
    database_file = get_database_file(server_id)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM players WHERE server_id = ? AND name = ?', (server_id, player_name))
    if not cursor.fetchone():
        print('Player does not exist in database:', player_name)
        conn.close()
        return
    
    cursor.execute(f'UPDATE players SET {equipment_type} = ? WHERE server_id = ? AND name = ?', (equipment_name, server_id, player_name))
    
    conn.commit()
    conn.close()
    
    print(f'Equipment {equipment_name} added to player {player_name} in slot {equipment_type}')

def remove_equipment(server_id, player_name, equipment_type):
    database_file = get_database_file(server_id)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM players WHERE server_id = ? AND name = ?', (server_id, player_name))
    if not cursor.fetchone():
        print('Player does not exist in database:', player_name)
        conn.close()
        return
    
    cursor.execute(f'UPDATE players SET {equipment_type} = ? WHERE server_id = ? AND name = ?', ('', server_id, player_name))
    
    conn.commit()
    conn.close()
    
    print(f'Equipment removed from player {player_name} in slot {equipment_type}')
    

def get_database_file(server_id):
    return os.path.join('data', server_id, 'players.db')

def get_player(server_id, player_name):
    database_file = get_database_file(server_id)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM players WHERE server_id = ? AND name = ?', (server_id, player_name))
    player = cursor.fetchone()
    
    conn.close()
    
    if player:
        keys = ['server_id', 'name', 'level', 'vigor', 'mind', 'endurance', 'strength', 'dexterity', 'intelligence', 'faith', 'arcane', 'weapon', 'armor', 'accessory', 'max_stamina', 'max_hp', 'max_fp']
        return dict(zip(keys, player))
    else:
        return None