# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 17:12:59 2022

@author: mathi
"""

import plotly.express as px
from dash import dcc



def figure_pie(df, attributes):
    x,y = attributes
    fig_new= px.pie(df, values='x', names='y', title='Pourcentage de gland par station en fonction des années')
    
    return fig_new

def build_dropdown_menu_2(menu_items):
    return dcc.Dropdown(
        id="dropdown2",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[0],
        clearable=False,
    )


def init_graph_2():
    return dcc.Graph(id="pie-chart")