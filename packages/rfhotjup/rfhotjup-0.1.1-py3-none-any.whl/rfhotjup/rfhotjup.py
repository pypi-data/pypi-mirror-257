import pandas as pd
import sqlite3
import os

location = os.path.dirname(os.path.realpath(__file__))
name_path = os.path.join(location, 'database', 'predicted_radio_fluxes.db')

def get_stellar_system_param():
    con = sqlite3.connect(name_path)
    star_planet_system_df = pd.read_sql_query("SELECT * from Star_Planet_System", con)
    return star_planet_system_df

def get_star_param():
    con = sqlite3.connect(name_path)
    star_df = pd.read_sql_query("SELECT * from Star", con)
    return star_df

def get_stellar_wind_param():
    con = sqlite3.connect(name_path)
    stellar_wind_df = pd.read_sql_query("SELECT * from Stellar_wind", con)
    return stellar_wind_df

def get_planet_param():
    con = sqlite3.connect(name_path)
    planet_df = pd.read_sql_query("SELECT * from Planet", con)
    return planet_df