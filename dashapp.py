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
				dbc.NavLink("Piechart", href="/", active="exact"),
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
        dropdown = view.GUI.build_dropdown_menu(data.get_valley(cur), 'dropdown'),
        dropdown2 = view.GUI.build_dropdown_menu(data.get_year(cur), 'dropdown2'),
        graph = view.GUI.init_graph('pie_chart')
        return [
			html.Div([
				dropdown,dropdown2,graph
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

@app.callback(Output('pie_chart','figure'),
			  [Input('dropdown','value'),
              Input('dropdown2', 'value')])

def graph_update(dropdown_values_valley, dropdown_values_year):
    if dropdown_values_valley or dropdown_values_year == None:
        raise PreventUpdate 
    all_valleys = data.get_valleys(cur)
    
    valleys = list(map(lambda x: all_valleys[x-1][0], dropdown_values_valley))
    all_years = data.get_year(cur)
    years=list(map(lambda x: all_years[x-1][0], dropdown_values_year))
    
    pie_data = data.prepare_data_piechart(cur, dropdown_values_valley, dropdown_values_year)
    return view.GUI.build_piechart(pie_data)


'''
@app.callback(
    Output("dm", "figure"),
    [Input("dropdown3", "value")])
def update_dist_marg(valley):
    
    sub_df, attributes = model.data.extract_df3(valley)
    return view.GUI.build_dist_marg(sub_df, attributes)
'''

if __name__ == '__main__': 
	app.run_server(debug=False)






con.commit()
con.close()