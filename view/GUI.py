from re import A
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import pandas as pd

from dash import dcc
from dash import dash_table



def build_dropdown_menu(item_list, iddropdown):
    options = [{'label': x, 'value':x} for x in item_list]
    return dcc.Dropdown(id = '{}'.format(iddropdown),
                        options=options,
                        value=item_list[0],
                        multi=False)


def build_dropdown_menu_single(item_list, iddropdown):
    options = [{'label': x, 'value':x} for x in item_list]
    return dcc.Dropdown(id = '{}'.format(iddropdown),
                        options=options,
                        value=item_list[1],
                        multi=False)

def build_dropdown_menu_options(item_list, iddropdown):
    options = [{'label': x, 'value':x} for x in item_list]
    return dcc.Dropdown(id = '{}'.format(iddropdown),
                        options=options,
                        value=item_list,
                        multi=True)


def build_radioitems(id):
    return dcc.RadioItems(id="{}".format(id),
                        value='scatterplot', 
        options=['scatterplot', 'boxplot'],)

def build_slider(id):
    return dcc.RangeSlider(0, 55000,100,
        marks= {0:'0', 10000:'10k', 20000:'20k', 30000:'30k', 40000:'40k', 50000:'50k', 55000:'55k' },
        count=1,
        value=[0, 55000],
        id='{}'.format(id)
    )

def init_graph(id_graph):
    return dcc.Graph(id="{}".format(id_graph))

def build_piechart(data):
	pie = px.pie(data, values=data.Ntot, names=data.Station, title='Pourcentage de gland par station en fonction des années et des deux valleys')
	return pie
        

def build_histogramme(data):
	histogramme = px.bar(data, x=data.Year , y=data.Ntot, color=data.Station, barmode="group", title = "Histogramme des Ntot en fonction des années pour les stations (le tout trié par valleys)")
	return histogramme

def build_distmarge(data):
    dm = px.scatter(data, x=data.Range, y=data.rate_Germ, color=data.rate_Germ, marginal_y="violin",
           marginal_x="box", trendline="ols", template="simple_white", title="Distribution Marginale sur le ration de glands ayant germés en fonction du rang de l'altitude (le tout trié par valleys)")

    return dm

def build_animation(data):
	animation = px.bar(
            data, x=data.Station, y=data.Ntot, color=data.Station, 
            animation_frame=data.Year, range_y=[0,10000], title="Animation sur les années des Ntot en fonction des stations (le tout trié par valleys)")
	return  animation

def build_linegraph(data):
    fig = px.line(data, x=data.VH, y=data.AVG_Mtot, color=data.code, title="Line graph de la moyenne des Mtot en fonction du volume du houppier pour les codes\
         des arbres (le tout trié par stations)", color_discrete_sequence=px.colors.qualitative.Set3_r)
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    return fig

def build_3dplot(data):
    fig = px.line_3d(data, x=data.DD, y=data.Year, z=data.AVG_Ntot, color=data.Year, title="Graphique 3D de la moyenne des Ntot en fonction de l'année et du jour de la récolte en jour julien (le tout trié par stations)")
    return fig

def build_scatterplot(data):
    fig = px.scatter(data, x=data.DD, y=data.Mtot, color=data.oneacorn,
                 size=data.Ntot, hover_data=['code'], title ="Scatter Plot ??")
    return fig

def build_boxplot(data):
    fig = px.box(data, x=data.Year, y=data.Mtot,color=data.Year, title ="??")
    return fig

def build_map(data):
    px.set_mapbox_access_token('pk.eyJ1IjoidGxhdmFuZGllciIsImEiOiJjbDNibjEyaWYwZDJ0M2lwNDZiNXhtazN1In0.spDyDVYEfhMsAT1CbWjkrA')
    fig = px.scatter_mapbox(data, lat=data.lat, lon=data.lon, color=data.AVG_oneacorn, size=data.SUM_Ntot, hover_name=data.Station, hover_data=['SUM_Mtot', 'AVG_Mtot'],
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=5)
    
    return fig