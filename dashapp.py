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

data.setup(cur)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])   #initialising dash app


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
		html.H2("TISSANDIER LAVANDIER", className="display-4"),
		html.Hr(),
		html.P(
			"Forêt Pyrénnées", className="lead"
		),
		dbc.Nav(
			[
				dbc.NavLink("Histogramme", href="/", active="exact"),
				dbc.NavLink("Piechart", href="/piechart", active="exact"),
				dbc.NavLink("prof", href="/prof", active="exact"),
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
		dropdown3 = view.GUI.build_dropdown_menu3(data.get_valley(cur))
		graph = view.GUI.init_graph('histogramme')
		return [
			html.Div([
				dropdown3, graph
			])
		]
	elif pathname == "/piechart":
		dropdown1 = view.GUI.build_dropdown_menu1(data.get_valley(cur)),
		dropdown2 = view.GUI.build_dropdown_menu2(data.get_year(cur)),
		pie_chart = view.GUI.init_graph('pie_chart')
		return [
			html.Div([
				dropdown1,dropdown2,pie_chart
			])
		]
  
	elif pathname == "/prof":
		dropdown = view.GUI.build_dropdown_menu(data.get_stations(cur)),
		graph2 = view.GUI.init_graph('timeline_plot')
		return [
			html.Div([
				dropdown, graph2
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




'''
app.layout = html.Div(id = 'parent', children = [
		html.H1(id = 'piechart', children = 'Graphique sous forme de piechart ', style = {'textAlign':'center',\
												'marginTop':40,'marginBottom':40}),
		view.GUI.build_dropdown_menu(data.get_valley(cur), 'dropdown'),
        view.GUI.build_dropdown_menu(data.get_year(cur), 'dropdown2'),
		html.Hr(),
		dcc.Graph(id = 'pie_chart')

	]
)'''
@app.callback(Output('histogramme','figure'),
              Input('dropdown3', 'value'))

def histogramme_update(dropdown_values_valley):
    if dropdown_values_valley == None:
        raise PreventUpdate 
    
    histogramme = data.prepare_data_histogramme(con, dropdown_values_valley)
    return view.GUI.build_histogramme(histogramme)


@app.callback(Output('pie_chart','figure'),
			  [Input('dropdown1','value'),
              Input('dropdown2', 'value')])

def pie_chart_update(dropdown_values_valley, dropdown_values_year):
    if dropdown_values_valley or dropdown_values_year == None:
        raise PreventUpdate 
    all_valleys = data.get_valley(cur)
    
    valleys = list(map(lambda x: all_valleys[x-1][0], dropdown_values_valley))
    all_years = data.get_year(cur)
    years=list(map(lambda x: all_years[x-1][0], dropdown_values_year))
    
    pie_data = data.prepare_data_piechart(con, dropdown_values_valley, dropdown_values_year)
    return view.GUI.build_piechart(pie_data)


@app.callback(Output(component_id='timeline_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_values):
    if dropdown_values == None:
        raise PreventUpdate
    all_stations = data.get_stations(cur)
    timeline_data = data.prepare_data(dropdown_values)
    stations = list(map(lambda x: all_stations[x-1][0], dropdown_values))
    return view.GUI.build_timeline_graph(timeline_data, stations)
    

'''
@app.callback(
    Output("dm", "figure"),
    [Input("dropdown3", "value")])
def update_dist_marg(valley):
    
    sub_df, attributes = model.data.extract_df3(valley)
    return view.GUI.build_dist_marg(sub_df, attributes)
'''

if __name__ == '__main__': 
	app.run_server(debug=True)






con.commit()
con.close()