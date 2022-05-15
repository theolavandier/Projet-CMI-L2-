import pandas as pd
import csv 

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

    cur.execute('''
        CREATE TABLE IF NOT EXISTS keytab (
        id_key INTEGER PRIMARY KEY AUTOINCREMENT,
        id_recolte INTEGER,
        id_arbre INTEGER,
        id_station INTEGER,
        id_valley INTEGER,
        FOREIGN KEY (id_recolte) REFERENCES récolte(id_r),
        FOREIGN KEY (id_arbre) REFERENCES arbre(id),
        FOREIGN KEY (id_station) REFERENCES station(id),
        FOREIGN KEY (id_valley) REFERENCES valler(id)
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


            query= 'SELECT id_key FROM keytab, récolte, arbre, stations, valley WHERE\
                 id_recolte=id_r AND récolte.ID = "{}"'.format(row['ID'])
                 
            result = cur.execute(query)        
            if result.fetchone() == None:
                query = 'INSERT INTO keytab (id_recolte, id_arbre, id_station, id_valley) \
                    SELECT id_r, arbre.id, stations.id, valley.id FROM récolte,arbre,stations,valley\
                        WHERE récolte.ID = "{}" and arbre.code = "{}" and stations.Station = "{}" and valley.Valley = "{}";'.format(row['ID'],row['code'],row['Station'],row['Valley'])
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