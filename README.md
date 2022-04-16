# Projet-CMI-L2-
Théo Lavandier Mathilde Tissandier
hellos
how are you ?

le code Gui :
import plotly.express as px

from dash import dcc 
from dash import dash_table

def build_dropdown_menu(menu_items):
    return dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[0],
        clearable=False,
    )

def init_graph():
    return dcc.Graph(id="bar-chart")

def build_figure(df, attributes):
    x, y, z = attributes
    fig = px.bar(df, x=x, y=y,
                 color=z, barmode="group", title = "Histogramme type fourni")
    return fig

def data_table(dataframe):
    return dash_table.DataTable(data=dataframe.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in dataframe.columns],
                                page_size=30,
                                sort_action="native",
                                sort_mode="multi",
                                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                                )



def build_dropdown_menu_2(menu_items):
    return dcc.Dropdown(
        id="dropdown2",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[-1],
        clearable=False,
    )

def init_graph_2():
    return dcc.Graph(id="pie-chart")

def figure_pie(df, attributes):
    x, y, z = attributes
    fig_new= px.pie(df, values=y, names=z, title='Pourcentage de gland par station en fonction des années et des deux stations')
    
    return fig_new

def build_dropdown_menu_3(menu_items):
    return dcc.Dropdown(
        id="dropdown3",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[0],
        clearable=False,
    )

def init_graph_3():
    return dcc.Graph(id="model-3d")

def figure_3d(df, attributes):
    x, y, z, t, m= attributes
    fig_3d = px.scatter_3d(df, x=x, y=y, z=z,
              color=t, symbol=m, opacity=0.7, title = "Modèle 3D en fonction de la quantité totale de glands mis à germer, le nombre de ceux qui ont gérmé et leur altitude ")
    return fig_3d
    
def build_dropdown_menu_4(menu_items):
    return dcc.Dropdown(
        id="dropdown4",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[0],
        clearable=False,
    )

def init_graph_4():
    return dcc.Graph(id="model-scatter")

def figure_scatter(df, attributes):
    x, y, z= attributes
    fig_scatter = px.scatter(df, x=x, y=y, color=z, title = "Modèle en fonction des années, des Mtot et en utlisant les tot_Germ et pouvant varier en fonction des stations")
    return fig_scatter

def build_dropdown_menu_5(menu_items):
    return dcc.Dropdown(
        id="dropdown5",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[-1],
        clearable=False,
    )

def init_graph_5():
    return dcc.Graph(id="model-barpolar")

def figure_barpolar(df, attributes):
    x, y, z, t = attributes
    fig_barpolar = px.bar_polar(df, r=x, theta=y, color=z, template=t,
                color_discrete_sequence= px.colors.sequential.Plasma_r,title = "Modèle en fonction des stations, des Ntot et en utilisant l'altitude et pouvant varier en fonction des années")
    return fig_barpolar

def build_dropdown_menu_6(menu_items):
    return dcc.Dropdown(
        id="dropdown6",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[-1],
        clearable=False,
    )

def init_graph_6():
    return dcc.Graph(id="model-graph")

def figure_graph(df, attributes):
    x, y, z = attributes
    fig_graph = px.scatter(df, x=x, y=y, color=z, title = "Modèle en fonction du VH et des Ntot pour les stations et pouvant varier en fonction des années")
    return fig_graph


le dashapp :
import model.data
import view.GUI
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

# styling the sidebar
SIDEBAR_STYLE = {
	"position": "fixed",
	"top": 0,
	"left": 0,
	"bottom": 0,
	"width": "16rem",
	"padding": "2rem 1rem",
	"background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
	"margin-left": "18rem",
	"margin-right": "2rem",
	"padding": "2rem 1rem",
}

sidebar = html.Div(
	[
		html.H2("TISSANDIER Mathilde", className="display-4"),
		html.Hr(),
		html.P(
			"Forêt Pyrénnées", className="lead"
		),
		dbc.Nav(
			[
				dbc.NavLink("Histogramme", href="/", active="exact"),
				dbc.NavLink("Tableur", href="/table", active="exact"),
                dbc.NavLink("Pie Char", href="/piecharts", active="exact"),
                dbc.NavLink("Vision 3D", href="/3d", active="exact"),
                dbc.NavLink("Vision Scatter", href="/scatter", active="exact"),
                dbc.NavLink("Vision Bar Polar", href="/barpolar", active="exact"),
                dbc.NavLink("Graphique", href="/graph", active="exact")
			],
			vertical=True,
			pills=True,
		),
	],
	style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)


app.layout = html.Div([
	dcc.Location(id="url"),
	sidebar,
	content
])

@app.callback(
	Output("page-content", "children"),
	[Input("url", "pathname")]
)
def render_page_content(pathname):
    
    if pathname == "/":
        dropdown = view.GUI.build_dropdown_menu(model.data.get_unique_values())
        graph = view.GUI.init_graph()
        return [
			html.Div([
				dropdown, graph
			])
		]
    elif pathname == "/piecharts":
        dropdown_station = view.GUI.build_dropdown_menu(model.data.get_unique_values())
        dropdown_year = view.GUI.build_dropdown_menu_2(model.data.get_unique_values1())
        graph = view.GUI.init_graph_2()
        return [
            html.Div([
                dropdown_station, graph, dropdown_year
                ])
        ]
    elif pathname == "/table":
		# fetch client info
        return [
				html.H1('Données forêt pyrénnées (tableur)', id='table_view',
						style={'textAlign':'left'}),
				html.Hr(style={'width': '75%', 'align': 'center'}),
				html.Div(id='data_table', children = view.GUI.data_table(model.data.df))
				]
    elif pathname == '/3d' :
        dropdown_station_2 = view.GUI.build_dropdown_menu_3(model.data.get_unique_values2())
        graph = view.GUI.init_graph_3()
        return [
            html.Div([
				dropdown_station_2, graph
            ])
        ]
    elif pathname == '/scatter' :
        dropdown_station_3 = view.GUI.build_dropdown_menu_4(model.data.get_unique_values3())
        graph = view.GUI.init_graph_4()
        return [
            html.Div([
				dropdown_station_3, graph
            ])
        ]
    elif pathname == '/barpolar' :
        dropdown_year_4 = view.GUI.build_dropdown_menu_5(model.data.get_unique_values4())
        graph = view.GUI.init_graph_5()
        return [
            html.Div([
				dropdown_year_4, graph
            ])
        ]
    elif pathname == '/graph' :
        dropdown_year_5 = view.GUI.build_dropdown_menu_6(model.data.get_unique_values5())
        graph = view.GUI.init_graph_6()
        return [
            html.Div([
				dropdown_year_5, graph
            ])
        ]
    else:
        return html.Div(
			[
				html.H1("404: Not found", className="text-danger"),
				html.Hr(),
				html.P(f"The pathname {pathname} was not recognised..."),
			]
		)

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(value):
    sub_df, attributes = model.data.extract_df(value)
    return view.GUI.build_figure(sub_df, attributes)

@app.callback(
    Output("pie-chart", "figure"),
    [Input("dropdown", "value"),
     Input("dropdown2", "value")])
def update_pie_chart(value_dropdown_station, value_dropdown_year):
    sub_df, attributes = model.data.extract_df1(value_dropdown_station, value_dropdown_year)
    return view.GUI.figure_pie(sub_df, attributes)

@app.callback(
    Output("model-3d", "figure"),
    [Input("dropdown3", "value")])
def update_3d(value_dropdown_Station):
    sub_df, attributes = model.data.extract_df2(value_dropdown_Station)
    return view.GUI.figure_3d(sub_df, attributes)

@app.callback(
    Output("model-scatter", "figure"),
    [Input("dropdown4", "value")])
def update_scatter(value_dropdown_Station):
    sub_df, attributes = model.data.extract_df3(value_dropdown_Station)
    return view.GUI.figure_scatter(sub_df, attributes)

@app.callback(
    Output("model-barpolar", "figure"),
    [Input("dropdown5", "value")])
def update_barpolar(value_dropdown_Year):
    sub_df, attributes = model.data.extract_df4(value_dropdown_Year)
    return view.GUI.figure_barpolar(sub_df, attributes)

@app.callback(
    Output("model-graph", "figure"),
    [Input("dropdown6", "value")])
def update_graph(value_dropdown_Year):
    sub_df, attributes = model.data.extract_df5(value_dropdown_Year)
    return view.GUI.figure_graph(sub_df, attributes)

if __name__=='__main__':
	app.run_server()

le data :

import pandas as pd

df = pd.read_csv('model/Repro_IS.csv', sep=';')
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



