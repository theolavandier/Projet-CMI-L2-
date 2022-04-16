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

