import pandas as pd
import sqlite3

con = sqlite3.connect('Pyrennees.db')
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS valley (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Valley TEXT NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Stations TEXT NOT NULL,
    Range REAL,
    Altitude REAL,
    valley_id INTEGER,
    FOREIGN KEY (valley_id) REFERENCES valley(id)
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS arbre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    Species TEXT NOT NULL,
    VH REAL,
    H REAL,
    SH REAL,
    station_id INTEGER,
    FOREIGN KEY (station_id) REFERENCES stations(id)
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS récolte (
    id_r INTEGER PRIMARY KEY AUTOINCREMENT,
    ID TEXT NOT NULL,
    harv_num REAL,
    DD REAL,
    harv REAL,
    Year INTEGER,
    Date DATETIME,
    Mtot REAL,
    Ntot REAL,
    Ntot1 REAL,
    oneacorn REAL,
    tot_Germ REAL,
    M_Germ REAL, 
    N_Germ REAL, 
    rate_Germ REAL,
    arbre_id INTEGER,
    FOREIGN KEY (arbre_id) REFERENCES arbre(id)
    );
''')

data = pd.read_csv('Repro_IS.csv', sep=';') 
data.to_sql('Repro_data', con, if_exists='replace', index=False)

valley_list = ['Valley']
v = data[valley_list]
stations_list = ['Station', 'Range', 'Altitude']
s = data[stations_list]
tree_list = ['code', 'Species', 'VH', 'H', 'SH']
t=data[tree_list]
harvest_list = ['ID', 'harv_num', 'DD', 'harv', 'Year', 'Date', 'Mtot', 'Ntot', 'Ntot1', 'oneacorn', 'tot_Germ', 'M_Germ', 'N_Germ', 'rate_Germ']
h = data[harvest_list]

v.to_sql('valley', con, if_exists='append', index=False)
s.to_sql('stations', con, if_exists='append', index=False)
t.to_sql('arbre', con, if_exists='append', index=False)
h.to_sql('recolte', con, if_exists='append', index=False)



df = pd.read_csv('Repro_IS.csv', sep=';')
select_column = 'Valley'
select_column_Year = 'Year'
select_column_Station = 'Station'

def get_unique_values():
    return df[select_column].unique()

def get_unique_values1():
    return df[select_column_Year].unique()

def get_unique_values2():
    return df[select_column_Station].unique()

def get_unique_values3():
    return df[select_column_Station].unique()

def get_unique_values4():
    return df[select_column_Year].unique()

def get_unique_values5():
    return df[select_column_Year].unique()


def extract_df(value):
    mask = df[select_column] == value
    df_valley = df[mask]
    # attributes used to specify grouping (and view)
    x_att = 'Year'
    y_att = 'Ntot'
    z_att = 'Station'

    df_agreg = df_valley[[x_att, y_att, z_att]].groupby(by=[x_att, z_att]).sum()
    df_agreg = df_agreg.reset_index()
    return df_agreg, (x_att, y_att, z_att)

def extract_df1(value_dropdown_valley, value_dropdown_year):
    mask_year = df[select_column_Year] == value_dropdown_year
    df_valley = df[mask_year]
    
    mask_valley = df_valley[select_column] == value_dropdown_valley
    df_valley = df_valley[mask_valley]
    # attributes used to specify grouping (and view)
    x_att = 'Year'
    y_att = 'Ntot'
    z_att = 'Station'

    df_agreg = df_valley[[x_att, y_att, z_att]].groupby(by=[x_att, z_att]).sum()
    df_agreg = df_agreg.reset_index()
    return df_agreg, (x_att, y_att, z_att)

def extract_df2(value_dropdown_stations):
    mask_stations = df[select_column_Station] == value_dropdown_stations
    df_stations = df[mask_stations]
    # attributes used to specify grouping (and view)
    x_att = 'tot_Germ'
    y_att = 'N_Germ'
    z_att = 'Altitude'
    t_att = 'Ntot'
    m_att = 'Station'
    return df_stations, (x_att, y_att, z_att,t_att,m_att)

def extract_df3(value_dropdown_stations):
    mask_stations = df[select_column_Station] == value_dropdown_stations
    df_stations = df[mask_stations]
    # attributes used to specify grouping (and view)
    x_att = 'Year'
    y_att = 'Mtot'
    z_att = 'tot_Germ'
    return df_stations, (x_att, y_att, z_att)

def extract_df4(value_dropdown_year):
    mask_years = df[select_column_Year] == value_dropdown_year
    df_years = df[mask_years]
    # attributes used to specify grouping (and view)
    x_att = 'Ntot'
    y_att = 'Station'
    z_att = 'Altitude'
    t_att = "plotly_dark"
    return df_years, (x_att, y_att, z_att, t_att)

def extract_df5(value_dropdown_year):
    mask_years = df[select_column_Year] == value_dropdown_year
    df_years = df[mask_years]
    # attributes used to specify grouping (and view)
    x_att = 'VH'
    y_att = 'Ntot'
    z_att = 'Station'
    return df_years, (x_att, y_att, z_att)
