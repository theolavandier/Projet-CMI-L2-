import pandas as pd
import csv 
import sqlite3


import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

def setup(cur):

    cur.execute('''
        CREATE TABLE IF NOT EXISTS valley (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Valley TEXT NOT NULL
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Station TEXT NOT NULL,
        Range REAL,
        Altitude REAL,
        id_valley INTEGER,
        FOREIGN KEY (id_valley) REFERENCES valler(id)
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
        id_station INTEGER,
        FOREIGN KEY (id_station) REFERENCES station(id)
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
        id_arbre INTEGER,
        FOREIGN KEY (id_arbre) REFERENCES arbre(id)
        );
    ''')

    with open('./model/Repro_IS.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            query = 'SELECT (id) FROM stations WHERE Station="{}"'.format(row['Station'])
            result = cur.execute(query)        
            if result.fetchone() == None:
                query = 'INSERT INTO stations (Station, Range, Altitude, id_valley) VALUES ("{}", {}, {}, 0);'.format(row['Station'], row['Range'], row['Altitude'])
                cur.execute(query)
                
            query = 'SELECT (id) FROM valley WHERE Valley="{}"'.format(row['Valley'])
            result = cur.execute(query)        
            if result.fetchone() == None:
                query = 'INSERT INTO valley (Valley) VALUES ("{}");'.format(row['Valley'])
                cur.execute(query)

            query = 'SELECT (id) FROM arbre WHERE code="{}"'.format(row['code'])
            result = cur.execute(query)        
            if result.fetchone() == None:
                query = 'INSERT INTO arbre (code, Species, VH, H, SH, id_station) VALUES ("{}", "{}", "{}", "{}", "{}", 0);'.\
                    format(row['code'],row['Species'], row['VH'], row['H'], row['SH'])
                cur.execute(query)

            query = 'SELECT (id_r) FROM récolte WHERE ID="{}"'.format(row['ID'])
            result = cur.execute(query)        
            if result.fetchone() == None:
                query = 'INSERT INTO récolte (ID,harv_num,DD,harv,Year,Date,Mtot,Ntot,Ntot1,oneacorn,tot_Germ, M_Germ,N_Germ,rate_Germ, id_arbre) VALUES\
                     ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", 0);'.\
                         format(row['ID'],row['harv_num'],row['DD'],row['harv'],row['Year'],row['Date'],\
                              row['Mtot'],row['Ntot'],row['Ntot1'],row['oneacorn'],row['tot_Germ'],row['M_Germ'],row['N_Germ'], row['rate_Germ'])
                cur.execute(query)

                
                
                
    with open('./model/Repro_IS.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            query = 'SELECT (id_valley) FROM stations WHERE Station="{}"'.format(row['Station'])
            result = cur.execute(query)        
            if result.fetchone()[0] == 0:
                query = 'UPDATE stations SET id_valley = (SELECT id FROM valley WHERE Valley="{}") WHERE Station ="{}"'.format(row['Valley'],row['Station'] )
                cur.execute(query)
                
            query = 'SELECT (id_station) FROM arbre WHERE code="{}"'.format(row['code'])
            result = cur.execute(query)    
            if result.fetchone()[0] == 0:
                query = 'SELECT id FROM stations WHERE Station="{}"'.format(row['Station'])
                result = cur.execute(query)  
                query = 'UPDATE arbre SET id_station = {} WHERE code ="{}"'.format(result.fetchone()[0], row['code'])
                cur.execute(query)
                
            query ='SELECT (id_arbre) FROM récolte WHERE ID ="{}"'.format(row['ID'])
            result = cur.execute(query)
            if result.fetchone()[0] == 0:
                query = 'SELECT id FROM arbre WHERE code="{}"'.format(row['code'])
                result = cur.execute(query)  
                query = 'UPDATE récolte SET id_arbre = {} WHERE ID ="{}"'.format(result.fetchone()[0], row['ID'])
                cur.execute(query)

def get_stations():
	connexion = sqlite3.connect('Pyrenees.db')
	query="SELECT Station, id FROM station"
	cursor = connexion.cursor()
	result = cursor.execute(query)
	return result.fetchall()

def get_valley():
	connexion = sqlite3.connect('Pyrenees.db')
	query="SELECT Valley, id FROM valley"
	cursor = connexion.cursor()
	result = cursor.execute(query)
	return result.fetchall()

def get_arbre():
	connexion = sqlite3.connect('Pyrenees.db')
	query="SELECT code, id FROM arbre"
	cursor = connexion.cursor()
	result = cursor.execute(query)
	return result.fetchall()

def get_recolte():
	connexion = sqlite3.connect('Pyrenees.db')
	query="SELECT ID, id_r FROM récolte"
	cursor = connexion.cursor()
	result = cursor.execute(query)
	return result.fetchall()

def get_year():
	connexion = sqlite3.connect('Pyrenees.db')
	query="SELECT DISTINCT Year, id_r FROM récolte GROUP BY Year"
	cursor = connexion.cursor()
	result = cursor.execute(query)
	return result.fetchall()


def prepare_data_piechart(valley_list, year_list):
    if valley_list or year_list == None:
        raise PreventUpdate
    else:
        connexion = sqlite3.connect('Pyrenees.db')
        if (len(valley_list) == 1 and len(year_list) == 1):
            valley = valley_list[0] 
            year = year_list[0]
            query = "SELECT récolte.Year, récolte.Ntot, stations.Stations, valley.Valley FROM récolte, arbre, stations, valley\
                WHERE récolte.id_arbre = arbre.id AND arbre.id_station = stations.id AND stations.id_valley = valley.id\
                    AND valley.Valley ='{}' AND récolte.Year = '{}'".format(valley, year)
        else:
            query = "SELECT récolte.Year, récolte.Ntot, stations.Stations, valley.Valley FROM récolte, arbre, stations, valley\
                WHERE récolte.id_arbre = arbre.id AND arbre.id_station = stations.id AND stations.id_valley = valley.id\
                    AND valley.Valley IN '{}' AND récolte.Year IN '{}'".format(tuple(valley_list), tuple(year_list))

        df = pd.read_sql(query, connexion)
        df_agreg = df.groupby(['Station', 'Year'])
        d = df_agreg.to_dict()['Ntot']
        years = sorted(set([x[1] for x in d.keys()]))
        arbres = set([x[0] for x in d.keys()])
        for a in arbres:
            for y in years:
                try:
                    print(d[(a, y)])
                except KeyError:
                    d[(a, y)] = 0
        arbres_columns = {x: [d[(x, y)] for y in years] for x in arbres}
        arbres_columns['year'] = years
        timeline_data = pd.DataFrame(arbres_columns)
        return df_agreg

'''
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
'''