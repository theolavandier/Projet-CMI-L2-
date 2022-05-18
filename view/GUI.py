from re import A
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import dash_table

def build_dropdown_menu_options(item_list, iddropdown):
    options = [{'label': x, 'value':x} for x in item_list]
    return dcc.Dropdown(id = '{}'.format(iddropdown),
                        options=options,
                        value=item_list,
                        multi=True)                        

def build_radioitems(id, item_list):
    return dcc.RadioItems(id="{}".format(id),
                        value=item_list[0], 
        options=item_list,)

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
	pie = px.pie(data, values=data.Ntot, names=data.Station, 
    title='Pourcentage de gland par station en fonction des années et des deux valleys',
    color_discrete_sequence=px.colors.qualitative.Pastel1)
	return pie
        
def build_histogramme(data):
	histogramme = px.bar(data, x=data.Year , y=data.AVG_Ntot, color=data.Station, barmode="group", 
    title = "Histogramme de la Moyenne de Ntot pour chaque Station en fonction des années (le tout trié par valleys)")
	return histogramme

def build_distmarge(data):
    dm = px.scatter(data, x=data.Range, y=data.rate_Germ, color=data.rate_Germ, marginal_y="violin",
           marginal_x="box", trendline="ols", template="simple_white", 
           title="Distribution Marginale sur le ratio de glands ayant germés en fonction du rang de l'altitude (le tout trié par valleys)")
    return dm

def build_animation(data):
	animation = px.bar(
            data, x=data.Station, y=data.AVG_Ntot, color=data.Station, 
            animation_frame=data.Year, range_y=[0,10000], 
            title="Evolution de la moyenne des Ntot par Station au fil des années, depuis 2015 (le tout trié par valleys)")
	return  animation

def build_linegraph(data):
    fig = px.line(data, x=data.VH, y=data.AVG_Mtot, color=data.Station,  text="code",
    title="Moyenne de la masse de glands (Mtot) produite par chaque arbre en fonction du volume du houppier (VH)", 
    color_discrete_sequence=px.colors.qualitative.Set3_r)
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.update_traces(textposition="bottom right")
    return fig

def build_3dplot(data, radiovalue):
    fig = px.line_3d(data, x=data.DD, y=data.Year, z=radiovalue, color=data.Year, 
    title="Graphique 3D de {} en fonction de l'année et du jour de la récolte en jour julien (le tout trié par stations)".format(radiovalue),
    color_discrete_sequence=px.colors.qualitative.Prism)
    return fig

def build_scatterplot(data):
    fig = px.scatter(data, x=data.DD, y=data.Mtot, color=data.oneacorn,
                 size=data.Ntot, hover_data=['code'], 
                 title ="Scatter Plot représentant le Mtot de chaque récolte en fonction du jour de la récolte")
    return fig

def build_boxplot(data):
    fig = px.box(data, x=data.Year, y=data.Mtot,color=data.Year,
    title="Représentation des Mtot par récolte sous la forme de Boxplot, en fonction des années")
    return fig

def build_map(data):
    px.set_mapbox_access_token('pk.eyJ1IjoidGxhdmFuZGllciIsImEiOiJjbDNibjEyaWYwZDJ0M2lwNDZiNXhtazN1In0.spDyDVYEfhMsAT1CbWjkrA')
    fig = px.scatter_mapbox(data, lat=data.lat, lon=data.lon, color=data.AVG_oneacorn, size=data.SUM_Ntot, hover_name=data.Station, hover_data=['SUM_Mtot', 'AVG_Mtot'],
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=5,
                  title ="Carte représentant les Station et certaines de leurs données, en fonction de leur position")
    
    return fig