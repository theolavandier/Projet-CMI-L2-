from re import A
import plotly.express as px

from dash import dcc
from dash import dash_table

def build_dropdown_menu(item_list, iddropdown):
    options = [{'label': x, 'value':x} for x in item_list]
    return dcc.Dropdown(id = '{}'.format(iddropdown),
                        options=options,
                        value=item_list[0],
                        multi=True)

def build_dropdown_menu_options(item_list, iddropdown):
    options = [{'label': x, 'value':x} for x in item_list]
    return dcc.Dropdown(id = '{}'.format(iddropdown),
                        options=options,
                        value=item_list,
                        multi=True)

def init_graph(id_graph):
    return dcc.Graph(id="{}".format(id_graph))

def build_piechart(data):
	pie = px.pie(data, values=data.Ntot, names=data.Station, title='Pourcentage de gland par station en fonction des années et des deux stations')
	return pie
        

def build_histogramme(data):
	histogramme = px.bar(data, x=data.Year , y=data.Ntot, color=data.Station, barmode="group", title = "Histogramme type fourni")
	return histogramme

def build_distmarge(data):
    dm = px.scatter(data, x=data.Range, y=data.rate_Germ, color=data.rate_Germ, marginal_y="violin",
           marginal_x="box", trendline="ols", template="simple_white", title="Distribution Marginale sur le ration de glands ayant germés en fonction du rang de l'altitude")

    return dm

def build_animation(data):
	animation = px.bar(
            data, x=data.Station, y=data.Ntot, color=data.Station, 
            animation_frame=data.Year, range_y=[0,10000])
	return  animation

def build_linegraph(data):
    fig = px.line(data, x=data.VH, y=data.AVG_Mtot, color=data.code, title="layout.hovermode='x unified'")
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    return fig

