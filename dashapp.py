import sqlite3
import model.data as data
import view.GUI
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

con = sqlite3.connect('Pyrenees.db' ,check_same_thread=False)
cur = con.cursor()

#data.setup_table(cur)
#data.csv_into_table(cur)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])   #initialising dash app


SIDEBAR_STYLE = {
	"position": "fixed",
	"top": 0,
	"left": 0,
	"bottom": 0,
	"width": "19rem",
	"padding": "2rem 1rem",
	"background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
	"margin-left": "18rem",
	"margin-right": "2rem",
	"padding": "2rem 1rem",
}
GLAND = {
	"margin-left": "3rem",
	"margin-right": "2rem",
	"padding": "2rem 1rem",
	"height": "200px",
	"width": "150px",
}

NOMS = {
	"font-size": "25px",
}
fin = {
	"position": "absolute",
	"top": "95%",
	"left": "90%",
  	"transform" : "translate(-50%, -50%)",

}
sidebar = html.Div(
    [
		html.H2("TISSANDIER LAVANDIER", className="display-4", style = NOMS),
		html.Hr(),
		html.P(
			"Forêt Pyrénnées", className="lead"
		),
  
		dbc.Nav(
			[
				dbc.NavLink("Presentation", href="/presentation", active="exact"),
				dbc.NavLink("Histogramme", href="/", active="exact"),
				dbc.NavLink("Piechart", href="/piechart", active="exact"),
				dbc.NavLink("Distribution Marginale", href="/distmarge", active="exact"),
				dbc.NavLink("Animation", href="/animation", active="exact"),
				dbc.NavLink("Line Graph", href="/linegraph", active="exact"),
				dbc.NavLink("3d Plot", href="/3dplot", active="exact"),
				dbc.NavLink("doublegraphe", href="/graphdouble", active="exact"),
			],
		
			vertical=True,	
			pills=True,
		),
		html.A([
			html.Img(src='/assets/gland.png', style=GLAND)
		],
		href="https://fr.wikipedia.org/wiki/Ch%C3%AAne_p%C3%A9doncul%C3%A9"),
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
	Input("url", "pathname")
)
def render_page_content(pathname):
    
	if pathname == "/presentation":
		return html.H1("Bienvenue sur notre site !"), html.Span("Nous avons réalisé plusieurs présentations. En voici la liste :"),\
			html.Div("-Un histogramme qui reprend les données qui nous étaient fourni par notre professeur."),\
				html.Div("-Une piechart que nous avons faite nous-même composée de deux dropdowns."),\
					html.Div("-Une distribution marginale que nous avons aussi réalisée composée d'un seul dropdown sur les vallleys."),\
						html.Div("-Une animation avec pour dropdown les valleys mais aussi une animation qui parcours les années."),\
							html.Div("-Un graphique de type line compoé d'un dropdown sur sur les stations mais on retrouve aussi un curcesseur sur le graphique pour retrouver les données plus facilement."),\
								html.Div("-Un grahique de type 3D avec un dropdown sur les stations."),\
									html.Div("-Et pout finir nous avons une double animation avec une carte, on y retrouve un dropdown sur les stations avec la possibilité de choisir le graphique qu'on veut et une carte qui évolue en fonctions des stations sélectionnées."),\
										html.Br(),\
											html.Br(),\
												html.Div("Nous voulions remercier notre professeur Mr. MELANCON pour nous avoir fait découvrir dash, plotly,... Mais aussi por son aide dans la réalisation de nos projets"),\
													html.H2("Nous vous souhaitons une bonne découverte de notre site, et surtout n'oubliez pas d'appuyer sur le gland !"),\
														html.Div("Lavandier Théo & Tissandier Mathilde", style=fin)
										
							
												




	elif pathname == "/":
		
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con,cur),"dropdown3"),
				view.GUI.init_graph("histogramme")
			])
	elif pathname == "/distmarge":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con,cur),"dropdown4"),
				view.GUI.init_graph("distmarge")
			])
	elif pathname == "/piechart":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con,cur),"dropdown1"),
				view.GUI.build_dropdown_menu_options(data.get_year(con,cur),"dropdown2"),
				view.GUI.init_graph("piechart")
			])
	elif pathname == "/animation":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con,cur),"dropdown5"),
				view.GUI.init_graph("animation")
			])
	elif pathname == "/linegraph":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_stations(con,cur),"dropdown6"),
				view.GUI.init_graph("linegraph")
			])
	elif pathname == "/3dplot":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_stations(con,cur),"dropdown7"),
				view.GUI.init_graph("3dplot")
			])
	elif pathname == "/graphdouble":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_stations(con,cur),"dropdown8"),
				view.GUI.build_radioitems('scatterradio'),
				view.GUI.init_graph("scatterplot"),
                view.GUI.build_slider("slider"),
				view.GUI.build_map("map")
			])
	else:
		return html.Div(
			[
				html.H1("404: Not found", className="text-danger"),
				html.Hr(),
				html.P(f"The pathname {pathname} was not recognised..."),
			]
		)


@app.callback(Output('histogramme','figure'),
              Input('dropdown3', 'value'))

def histogramme_update(dropdown_values_valley):
    if dropdown_values_valley == None:
        raise PreventUpdate 
    
    histogramme = data.prepare_data_histogramme(con, dropdown_values_valley)
    return view.GUI.build_histogramme(histogramme)

@app.callback(Output('distmarge','figure'),
              Input('dropdown4', 'value'))

def distmarge_update(dropdown_values_valley):
    if dropdown_values_valley == None:
        raise PreventUpdate 
    
    distmarge = data.prepare_data_distmarge(con, dropdown_values_valley)
    return view.GUI.build_distmarge(distmarge)

@app.callback(Output('piechart','figure'),
			  [Input('dropdown1','value'),
              Input('dropdown2', 'value')])
def piechart_update (dropdown_values_valley, dropdown_values_year):
	if dropdown_values_valley == None or dropdown_values_year == None:
		raise PreventUpdate
	
	piechart = data.prepare_data_piechart(con, dropdown_values_valley,dropdown_values_year)
	return view.GUI.build_piechart(piechart)


@app.callback(Output('animation','figure'),
              Input('dropdown5', 'value'))

def animation_update(dropdown_values_valley):
    if dropdown_values_valley == None:
        raise PreventUpdate 
    animation = data.prepare_data_animation(con, dropdown_values_valley)
    return view.GUI.build_animation(animation)

@app.callback(Output('linegraph','figure'),
              [Input('dropdown6', 'value')])

def linegraph_update(dropdown_values_stations):
	if dropdown_values_stations == None:
		raise PreventUpdate 
	else:
		linegraph = data.prepare_data_linegraph(con, dropdown_values_stations)
			
		return view.GUI.build_linegraph(linegraph)

@app.callback(Output('3dplot','figure'),
              [Input('dropdown7', 'value')])

def plot3d_update(dropdown_values_stations):
	if dropdown_values_stations == None:
		raise PreventUpdate 
	else:
		plot3d = data.prepare_data_3dplot(con, dropdown_values_stations)
		return view.GUI.build_3dplot(plot3d)

@app.callback(Output('scatterplot','figure'),
              [Input('dropdown8', 'value'),
              Input('scatterradio', 'value'),
              Input('slider', 'value')])

def scatter_update(dropdown_values_stations, radiovalue, slidervalue):
    if dropdown_values_stations == None:
        raise PreventUpdate 
    else:
        if radiovalue == 'scatterplot':
            df = data.prepare_data_scatter(con, dropdown_values_stations, slidervalue)
            return view.GUI.build_scatterplot(df)
        else :
            df = data.prepare_data_scatter(con, dropdown_values_stations, slidervalue)
            return view.GUI.build_boxplot(df)

@app.callback(Output('map','figure'),
              [Input('dropdown8', 'value')])

def map_update(dropdown_values_stations):
	if dropdown_values_stations == None:
		raise PreventUpdate 
	else:
		df = data.prepare_data_map(con, dropdown_values_stations)
		return view.GUI.build_map(df)

if __name__ == '__main__': 
	app.run_server(debug=True)

con.commit()
con.close()
