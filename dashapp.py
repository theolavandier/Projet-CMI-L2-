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
		view.GUI.build_dropdown_menu(data.get_valley(cur), 'dropdown'),
        view.GUI.build_dropdown_menu(data.get_year(cur), 'dropdown2'),
		html.Hr(),
		dcc.Graph(id = 'pie_chart')

	]
)

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

if __name__ == '__main__': 
	app.run_server(debug=False)






con.commit()
con.close()