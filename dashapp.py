import sqlite3
import model.data as data
import view.GUI
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

con = sqlite3.connect('./model/Pyrenees.db' ,check_same_thread=False)
cur = con.cursor()

#data.setup_table(cur)
#data.csv_into_table(cur)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])   #initialising dash app


SIDEBAR_STYLE = { #CSS pour le style de la barre latérale
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
GLAND = { #CSS pour l'image du gland
	"margin-left": "3rem",
	"margin-right": "2rem",
	"padding": "2rem 1rem",
	"height": "200px",
	"width": "150px",
}

NOMS = { #CSS pour afficher les noms sur la barre latérale
	"font-size": "25px",
}
FIN = { #CSS pour afficher les noms de la page de présentation
	"text-align": "center",
	"text-decoration": "underline",
}
PRESENTATION ={ #CSS pour afficher les images de la page de présentation
	"height": "200px",
	"width": "286px",
}
sidebar = html.Div( #Initialisation d'une barre latérale pour notre site
    [
		html.H2("TISSANDIER LAVANDIER", className="display-4", style = NOMS),
		html.Hr(),
		html.P(
			"Forêt Pyrénnées", className="lead"
		),
  
		dbc.Nav( #Celle ci contient un navigateur qui permet de passer d'un graphique à un autre
			[
				dbc.NavLink("Presentation", href="/", active="exact"),
				dbc.NavLink("Histogramme", href="/histo", active="exact"),
				dbc.NavLink("Piechart", href="/piechart", active="exact"),
				dbc.NavLink("Distribution Marginale", href="/distmarge", active="exact"),
				dbc.NavLink("Animation", href="/animation", active="exact"),
				dbc.NavLink("Line Graph", href="/linegraph", active="exact"),
				dbc.NavLink("3d Plot", href="/3dplot", active="exact"),
				dbc.NavLink("Scatter, Boxplot And Map", href="/scatterandmap", active="exact"),
			],
		
			vertical=True,	
			pills=True,
		),
		html.A([
			html.Img(src='/assets/gland.png', style=GLAND) #afficher le gland
		],
		href="https://charlois.com/le-chene-des-pyrenees/"),#mettre le lien sur le gland
	],	
	style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE) #style sur la barre latérale

app.layout = html.Div([ #Layout de notre application
	dcc.Location(id="url"),
	sidebar,
	content
])

@app.callback(
	Output("page-content", "children"),
	Input("url", "pathname")
)
def render_page_content(pathname): #Fonction qui permet d'actualiser le contenu de la page en fonction de l'url utilisé
    
	if pathname == "/":
		return html.H1("Bienvenue sur notre site !"), html.Span("Nous avons réalisé plusieurs présentations. En voici la liste :"),\
			html.Div("-Un histogramme avec un dropdown."),\
				html.Div("-Une piechart composée de deux dropdowns."),\
					html.Div("-Une distribution marginale composée d'un seul dropdown sur les vallleys."),\
						html.Div("-Un graphique animé avec pour dropdown les valleys mais aussi une animation qui parcours les années."),\
							html.Div("-Un graphique de type line composé d'un dropdown sur les stations mais on retrouve aussi un curseur sur le graphique pour retrouver les données plus facilement."),\
								html.Div("-Un grahique de type 3D avec un dropdown sur les stations et la possibilité de choisir entre deux variables à étudier."),\
									html.Div("-Et pout finir nous avons une double animation avec une carte, on y retrouve un dropdown sur les stations avec la possibilité de choisir le graphique qu'on veut et une carte qui évolue en fonctions des stations sélectionnées."),\
										html.Br(),\
											html.Br(),\
												html.Div("Nous voulions remercier notre professeur Mr. MELANCON pour nous avoir fait découvrir dash, plotly,... Mais aussi pour son aide dans la réalisation de nos projets."),\
													html.H2("Nous vous souhaitons une bonne découverte de notre site, et surtout n'oubliez pas d'appuyer sur le gland !"),\
														html.P([
															html.Img(src='/assets/pyrenees.jpg', style=PRESENTATION),\
																html.Img(src='/assets/pyrenees1.jpg',style=PRESENTATION),\
																	html.Img(src='/assets/pyrenees2.jpg',style=PRESENTATION),\
																		html.Img(src='/assets/pyrenees3.jpg',style=PRESENTATION),\
														]),\
															html.Div("Lavandier Théo & Tissandier Mathilde", style=FIN)
	elif pathname == "/histo":
		
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con),"dropdown3"),
				view.GUI.init_graph("histogramme")
			])
	elif pathname == "/distmarge":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con),"dropdown4"),
				view.GUI.init_graph("distmarge")
			])
	elif pathname == "/piechart":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con),"dropdown1"),
				view.GUI.build_dropdown_menu_options(data.get_year(con),"dropdown2"),
				view.GUI.init_graph("piechart")
			])
	elif pathname == "/animation":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_valley(con),"dropdown5"),
				view.GUI.init_graph("animation")
			])
	elif pathname == "/linegraph":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_stations(con),"dropdown6"),
				view.GUI.init_graph("linegraph")
			])
	elif pathname == "/3dplot":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_stations(con),"dropdown7"),
				view.GUI.build_radioitems('scatterradio2', ["AVG_Mtot", "AVG_Ntot"]),
				view.GUI.init_graph("3dplot")
			])
	elif pathname == "/scatterandmap":
		return html.Div([
				view.GUI.build_dropdown_menu_options(data.get_stations(con),"dropdown8"),
				view.GUI.build_radioitems('scatterradio', ["scatterplot", "boxplot"]),
				view.GUI.init_graph("scatterplot"),
				html.H3("Mtot Range :"),
                view.GUI.build_slider("slider"),
				view.GUI.init_graph("map"),
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
def histogramme_update(dropdown_values_valley): #Fonction qui permet d'actualiser l'histogramme en fonction des valeurs d'un dropdown
    if dropdown_values_valley == None:
        raise PreventUpdate 
    histogramme = data.prepare_data_histogramme(con, dropdown_values_valley)
    return view.GUI.build_histogramme(histogramme)


@app.callback(Output('distmarge','figure'),
              Input('dropdown4', 'value'))
def distmarge_update(dropdown_values_valley): #Fonction qui permet d'actualiser la distribution marginale en fonction des valeurs d'un dropdown
    if dropdown_values_valley == None:
        raise PreventUpdate 
    distmarge = data.prepare_data_distmarge(con, dropdown_values_valley)
    return view.GUI.build_distmarge(distmarge)


@app.callback(Output('piechart','figure'),
			  [Input('dropdown1','value'),
              Input('dropdown2', 'value')])
def piechart_update (dropdown_values_valley, dropdown_values_year): #Fonction qui permet d'actualiser la piechart en fonction des valeurs de deux dropdowns 
	if dropdown_values_valley == None or dropdown_values_year == None:
		raise PreventUpdate
	piechart = data.prepare_data_piechart(con, dropdown_values_valley,dropdown_values_year)
	return view.GUI.build_piechart(piechart)


@app.callback(Output('animation','figure'),
              Input('dropdown5', 'value'))
def animation_update(dropdown_values_valley): #Fonction qui permet d'actualiser l'animation en fonction des valeurs d'un dropdown
    if dropdown_values_valley == None:
        raise PreventUpdate 
    animation = data.prepare_data_animation(con, dropdown_values_valley)
    return view.GUI.build_animation(animation)


@app.callback(Output('linegraph','figure'),
              [Input('dropdown6', 'value')])
def linegraph_update(dropdown_values_stations): #Fonction qui permet d'actualiser le line graph en fonction des valeurs d'un dropdown
	if dropdown_values_stations == None:
		raise PreventUpdate 
	else:
		linegraph = data.prepare_data_linegraph(con, dropdown_values_stations)
		return view.GUI.build_linegraph(linegraph)


@app.callback(Output('3dplot','figure'),
              [Input('dropdown7', 'value'),
			  Input('scatterradio2','value')])
def plot3d_update(dropdown_values_stations, radiovalue): #Fonction qui permet d'actualiser le 3dplot en fonction des valeurs d'un dropdown et d'un scatter radio
	if dropdown_values_stations == None:
		raise PreventUpdate 
	else:
		plot3d = data.prepare_data_3dplot(con, dropdown_values_stations)
		return view.GUI.build_3dplot(plot3d, radiovalue)
		

@app.callback(Output('scatterplot','figure'),
              [Input('dropdown8', 'value'),
              Input('scatterradio', 'value'),
              Input('slider', 'value')])
def scatter_update(dropdown_values_stations, radiovalue, slidervalue): #Fonction qui permet d'actualiser les deux scatters en fonction des valeurs d'un dropdown, d'un scatter radio et d'un slider
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
              [Input('dropdown8', 'value'),
			  Input('slider', 'value')])
def map_update(dropdown_values_stations, slidervalue): #Fonction qui permet d'actualiser la map en fonction des valeurs d'un dropdown et d'un slider
	if dropdown_values_stations == None:
		raise PreventUpdate 
	else:
		df = data.prepare_data_map(con, dropdown_values_stations, slidervalue)
		return view.GUI.build_map(df)

if __name__ == '__main__': 
	app.run_server(debug=True) #Run le serveur

con.commit()
con.close()