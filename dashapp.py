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
		html.H2("TISSANDIER LAVANDIER", className="display-4"),
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
