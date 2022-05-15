import sqlite3
import model.data as data
import view.GUI
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

con = sqlite3.connect('Pyrenees.db')
cur = con.cursor()

data.setup(cur)
app = dash.Dash()   #initialising dash app

app.layout = html.Div(id = 'parent', children = [
		html.H1(id = 'piechart', children = 'Graphique sous forme de piechart ', style = {'textAlign':'center',\
												'marginTop':40,'marginBottom':40}),
		view.GUI.build_dropdown_menu(data.get_valley()),
		html.Hr(),
		dcc.Graph(id = 'timeline_plot')

	]
)

@app.callback(Output(component_id='timeline_plot', component_property= 'figure'),
			  [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_values_valley, dropdown_values_year):
    if dropdown_values_valley and dropdown_values_year == None:
        raise PreventUpdate
    all_valleys = data.get_valleys()
    timeline_data = data.prepare_data_piechart(dropdown_values_valley)
    valleys = list(map(lambda x: all_valleys[x][0], dropdown_values_valley))
    all_years = data.get_year()
    years=list(map(lambda x: all_years[x][0], dropdown_values_year))
    return (view.GUI.build_timeline_graph_piechart(timeline_data, valleys), view.GUI.build_timeline_graph_piechart(timeline_data, years))

if __name__ == '__main__': 
	app.run_server(debug=True)






con.commit()
con.close()