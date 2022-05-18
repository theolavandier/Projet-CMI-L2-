import pandas as pd
import csv 
import sqlite3
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

def setup_table(cur):

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
        lat REAL,
        lon REAL,
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

def csv_into_table(cur):
    with open('./model/Repro_IS.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            query = 'SELECT (id) FROM stations WHERE Station="{}"'.format(row['Station'])
            result = cur.execute(query)        
            if result.fetchone() == None:
                query = 'INSERT INTO stations (Station, Range, Altitude, lat, lon, id_valley) VALUES ("{}", {}, {} , 0 , 0 , 0);'.format(row['Station'], row['Range'], row['Altitude'])
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

    query = 'UPDATE stations SET lat = 43.2642616 WHERE Station = "Josbaig"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = -0.7114511 WHERE Station = "Josbaig"'   
    cur.execute(query)  
    query = 'UPDATE stations SET lat = 43.0563951 WHERE Station = "Peguere"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = 1.2767851 WHERE Station = "Peguere"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lat = 45.2023158 WHERE Station = "Laveyron"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = 4.8144436 WHERE Station = "Laveyron"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 43.2269 WHERE Station = "Papillon"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = 1.2877 WHERE Station = "Papillon"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 42.8894933 WHERE Station = "Gabas"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = -0.4280869 WHERE Station = "Gabas"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 42.8549763 WHERE Station = "Artouste"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = -0.3097375 WHERE Station = "Artouste"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 42.7879051 WHERE Station = "Gedre-Bas"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = 0.01888 WHERE Station = "Gedre-Bas"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 43.2325985 WHERE Station = "Ibos"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = 0.0045982 WHERE Station = "Ibos"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 43.85337 WHERE Station = "Le-Hourcq"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = -0.9254837 WHERE Station = "Le-Hourcq"'   
    cur.execute(query)
    query = 'UPDATE stations SET lat = 43.1226157 WHERE Station = "Bager"'   
    cur.execute(query) 
    query = 'UPDATE stations SET lon = -0.5275369 WHERE Station = "Bager"'   
    cur.execute(query)




def get_valley(con,cur):
	query="SELECT Valley, id FROM valley"
	cursor = cur
	df = pd.read_sql(query, con)
	return df['Valley'].tolist()

def get_arbre(con,cur):
	query="SELECT code, id FROM arbre"
	cursor = cur
	df = pd.read_sql(query, con)
	return df['code'].tolist()

def get_recolte(con,cur):
	query="SELECT ID, id_r FROM récolte"
	cursor = cur
	df = pd.read_sql(query, con)
	return df['ID'].tolist()

def get_year(con,cur):
	query="SELECT DISTINCT Year, id_r FROM récolte GROUP BY Year"
	cursor = cur
	df = pd.read_sql(query, con)
	return df['Year'].tolist()

def get_stations(con,cur):
    query="SELECT Station, id FROM stations"
    cursor = cur
    df = pd.read_sql(query, con)
    return df['Station'].tolist()



def prepare_data_piechart(con,valley_list,year_list):
    if valley_list == None and year_list == None:
        raise PreventUpdate
    else:
        if (len(valley_list) == 1 and len(year_list) == 1):
            valley = valley_list[0] 
            year = year_list[0]
            query = "SELECT Station, Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley )\
                 WHERE Valley='{}' AND Year='{}' ".format(valley, year)
        elif (len(valley_list) == 1):
            valley = valley_list[0]
            query = "SELECT Station, Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley )\
                 WHERE Valley='{}' AND Year IN {} ".format(valley, tuple(year_list))
        elif (len(year_list)==1):
            years = year_list[0]
            query = "SELECT Station, Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley )\
                 WHERE Valley IN {} AND Year = '{}' ".format(tuple(valley_list), years)
        else:
            query = "SELECT Station, Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley )\
                 WHERE Valley IN {} AND Year IN {}".format(tuple(valley_list), tuple(year_list))
            
        df = pd.read_sql(query, con)
        return df


def prepare_data_histogramme(con, valley_list):
    if valley_list == None :
        raise PreventUpdate
    else:
        if (len(valley_list) == 1):
            valley = valley_list[0]
            query = "SELECT Station, Year, AVG(Ntot) as Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Valley='{}' GROUP BY Station, Year".format(valley)
        else:
            query = "SELECT Station, Year, AVG(Ntot) as Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Valley IN {} GROUP BY Station, Year".format(tuple(valley_list))
        
        df = pd.read_sql(query, con)
        return df


def prepare_data_distmarge(con, valley_list):
    if valley_list == None:
        raise PreventUpdate
    else:
        if (len(valley_list) == 1):
            valley = valley_list[0]
            query = "SELECT Range, rate_Germ FROM (SELECT Range , rate_Germ , Valley FROM stations, récolte, valley, arbre WHERE rate_Germ  != 'NA' AND arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Valley= '{}'".format(valley)
        else:
            query = "SELECT Range, rate_Germ FROM (SELECT Range , rate_Germ , Valley FROM stations, récolte, valley, arbre WHERE rate_Germ  != 'NA' AND arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Valley IN {}".format(tuple(valley_list))
        df = pd.read_sql(query, con)
        return df

def prepare_data_animation(con, valley_list):
    if valley_list == None :
        raise PreventUpdate
    else:
        if (len(valley_list) == 1):
            valley = valley_list[0]
            query = "SELECT Station, Year, AVG(Ntot) as Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Valley='{}' AND Year > 2014 GROUP BY Station, Year".format(valley)
        else:
            query = "SELECT Station, Year, AVG(Ntot) as Ntot FROM (SELECT Station, Year, Ntot, Valley FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Valley IN {} AND Year > 2014 GROUP BY Station, Year".format(tuple(valley_list))
        
        df = pd.read_sql(query, con)
        return df.sort_values(by=['Year','Station'])

def prepare_data_linegraph(con, station_list):
    if station_list == None :
        raise PreventUpdate
    else:
        if (len(station_list) == 1):
            station = station_list[0]
            query = "SELECT VH, AVG(Mtot) as AVG_Mtot, code FROM (SELECT Station, VH, Mtot, code FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Station='{}' GROUP BY VH".format(station)
        else:
            query = "SELECT VH, AVG(Mtot) as AVG_Mtot, code FROM (SELECT Station, VH, Mtot, code FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Station IN {} GROUP BY VH".format(tuple(station_list))
        
        df = pd.read_sql(query, con)
        return df


def prepare_data_3dplot(con, station_list):
    if station_list == None :
        raise PreventUpdate
    else:
        if (len(station_list) == 1):
            station = station_list[0]
            query = "SELECT Year ,DD, AVG(Ntot) as AVG_Ntot FROM (SELECT Station, DD, Ntot, Year FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Station='{}' GROUP BY Year, DD".format(station)
        else:
            query = "SELECT Year ,DD, AVG(Ntot) as AVG_Ntot FROM (SELECT Station, DD, Ntot, Year FROM stations, récolte, valley, arbre WHERE arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Station IN {} GROUP BY Year, DD".format(tuple(station_list))
        
        df = pd.read_sql(query, con)
        return df

def prepare_data_scatter(con, station_list, range):
    if station_list == None :
        raise PreventUpdate
    else:
        if (len(station_list) == 1):
            station = station_list[0]
            query = "SELECT Year ,Mtot, Ntot, oneacorn, code, DD FROM (SELECT Station, Year ,Mtot, Ntot, oneacorn, code, DD FROM stations, récolte, valley, arbre WHERE oneacorn != 'NA' AND Mtot >= {} AND Mtot <= {} AND arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Station='{}' ".format(range[0],range[1], station)
        else:
            query = "SELECT Year ,Mtot, Ntot, oneacorn, code, DD FROM (SELECT Station, Year ,Mtot, Ntot, oneacorn, code, DD FROM stations, récolte, valley, arbre WHERE oneacorn != 'NA' AND Mtot >= {} AND Mtot <= {} AND arbre.id = récolte.id_arbre AND stations.id = arbre.id_station AND valley.id = stations.id_valley ) WHERE Station IN {} ".format(range[0],range[1], tuple(station_list))
        
        df = pd.read_sql(query, con)
        return df