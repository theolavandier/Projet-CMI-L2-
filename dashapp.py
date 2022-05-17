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

###data.setup(cur)
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
sidebar = html.Div(
    [
		html.H2("TISSANDIER LAVANDIER", className="display-4", style = NOMS),
		html.Hr(),
		html.P(
			"Forêt Pyrénnées", className="lead"
		),
  
		dbc.Nav(
			[
				dbc.NavLink("Histogramme", href="/", active="exact"),
				dbc.NavLink("Piechart", href="/piechart", active="exact"),
				dbc.NavLink("Distribution Marginale", href="/distmarge", active="exact"),
				dbc.NavLink("Animation", href="/animation", active="exact"),
				dbc.NavLink("Line Graph", href="/linegraph", active="exact"),
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
    
	if pathname == "/":
		
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

@app.callback(Output('linegrap','figure'),
              Input('dropdown6', 'value'))

def linegraph_update(dropdown_values_stations):
    if dropdown_values_stations == None:
        raise PreventUpdate 
    
    linegraph = data.prepare_data_linegraph(con, dropdown_values_stations)
    return view.GUI.build_linegraph(linegraph)


if __name__ == '__main__': 
	app.run_server(debug=True)






con.commit()
con.close()