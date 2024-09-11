import json
import discord
from discord import app_commands
import rpg_main

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

### Slash Commands ###

# ping command
@tree.command(name = "ping", description = "replies with Pong!")
async def ping(interaction):
    await interaction.response.send_message("Pong!")
    
# set up the database for the server
@tree.command(name = "setup", description = "sets up the game database for the server")
async def setup(interaction):
    rpg_main.setup(str(interaction.guild_id))
    await interaction.response.send_message("Database setup complete for server: " + str(interaction.guild_id))
    
# new_player command
@tree.command(name = "new_player", description = "registers you as a new player")
async def new_player(interaction):
    # each player starts at level 1 with 10 in each stat, name is the player's username
    rpg_main.add_player(str(interaction.guild_id), str(interaction.user.id), 1, 10, 10, 10, 10, 10, 10, 10, 10)
    
    # Create and send embed with stats
    embed = create_player_embed(str(interaction.guild_id), str(interaction.user.id), interaction.user.name, interaction.user.avatar_url)
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="discordia rewrite"))
    print("Ready!")
    
# we run the bot with the token from the json file
client.run(json.load(open("config.json"))["token"])

def create_player_embed(server_id, user_id, username, avatar_url):
    # Fetch player data
    player_data = rpg_main.get_player(server_id, user_id)
    
    # Create embed
    embed = discord.Embed(title="Character Stats", color=discord.Color.blue())
    embed.set_author(name=username)
    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text="Realms of Discordia")
    
    # Add fields
    embed.add_field(name="**Level**", value=player_data['level'], inline=False)
    embed.add_field(name="Max HP", value=player_data['max_hp'], inline=True)
    embed.add_field(name="Max FP", value=player_data['max_fp'], inline=True)
    embed.add_field(name="Max Stamina", value=player_data['max_stamina'], inline=True)
    embed.add_field(name="Vigor", value=player_data['vigor'], inline=True)
    embed.add_field(name="Mind", value=player_data['mind'], inline=True)
    embed.add_field(name="Endurance", value=player_data['endurance'], inline=True)
    embed.add_field(name="Strength", value=player_data['strength'], inline=True)
    embed.add_field(name="Dexterity", value=player_data['dexterity'], inline=True)
    embed.add_field(name="Intelligence", value=player_data['intelligence'], inline=True)
    embed.add_field(name="Faith", value=player_data['faith'], inline=True)
    embed.add_field(name="Arcane", value=player_data['arcane'], inline=True)
    
    return embed