from dash import Dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import json
from django_plotly_dash import DjangoDash
import pickle
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


url = 'https://instances.social/api/1.0/instances/list'
key = 'Authorization: bearer xVyfYF0mSOnYS6Zlx34racvGlZwRxGKJsMAPYJndBpcyVCWOxrEUK6WZOg4r3Cmbboz1Jzkp9s2jibqYLQRNtCtKNGkqoA74e7O9TrWUuprX8dGlyrxrwa1Lrq8AKES0'

params = {'min_users': '0' , 'count': '0'} 

response = requests.get(url, params,
                        headers={'Authorization':'Bearer xVyfYF0mSOnYS6Zlx34racvGlZwRxGKJsMAPYJndBpcyVCWOxrEUK6WZOg4r3Cmbboz1Jzkp9s2jibqYLQRNtCtKNGkqoA74e7O9TrWUuprX8dGlyrxrwa1Lrq8AKES0'})

data_dict = response.json()
a = pd.DataFrame(data_dict['instances'])
a = a.drop(a[a['name'] == 'you-think-your-fake-numbers-are-impressive.well-this-instance-contains-all-living-humans.lubar.me'].index)



#a = pd.read_pickle('static/data/instances')


num_cols = ['users', 'statuses', "connections"]
a[num_cols] = a[num_cols].apply(pd.to_numeric, errors = 'coerce')
 
a = a.dropna(subset="name")
links={}

a['link'] = a.apply(lambda row: "[" + str(row['name']) + "]" + "(https://" + str(row['name']) + ")", axis=1)

#a['infolink'] = a.apply(lambda row: "[More Info]" + "(/instance/?id=" + str(row['id']) + ")", axis=1)

a['infolink'] = a.apply(lambda row: "[More Info]" + "(/instance/?id=" + str(row['name']) + ")", axis=1)

#a = a[["link","users","statuses", "connections", "infolink"]]

df = pd.DataFrame({'information': [v for v in a['info'].to_dict().values()]})
dfs = pd.json_normalize(df.information)
a = pd.merge(a, dfs, left_index=True, right_index=True)
a['languages'] = a['languages'].astype(str)
a['prohibited_content'] = a['prohibited_content'].astype(str)
a['categories'] = a['categories'].astype(str)


#a = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app = DjangoDash('dash_table') 
#app.layout = Table(a)


app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{
            'label': id,
            'value': id
        } for id in a.columns]
    ),
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal'
        },
        id='datatable-interactivity',
        columns=[
            {'id': x, 'name': "name", 'presentation': 'markdown', "deletable": True} if x == 'link' or x=='infolink' else {'id': x, 'name': x, "deletable": True} for x in a[["link","users","statuses", "connections", "infolink"]].columns
            #{'id': i, 'name': i, 'presentation': 'markdown'} for i in a.columns
        ],
        css=[{
        'selector': '.dash-spreadsheet td div',
        'rule': '''
            line-height: 8px;
            max-height: 25px; min-height: 25px; height: 25px;
            display: block;
            overflow-y: hidden;
            textAlign: center;
        '''
    }],
        #data=[{"html": '<a href="' + "/" + i + '">'+ i + '</a>'} for i in a["name"]], 
        markdown_options={"html": True},
        data=a.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        #selected_columns=[],
        #selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 20,
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity', 'columns'),
    [Input('dropdown', 'value')],
    [State('datatable-interactivity', 'columns')]
)
def update_columns(value, columns):
    if value is None or columns is None:
        raise PreventUpdate

    inColumns = any(c.get('id') == value for c in columns)

    if inColumns == True:
        raise PreventUpdate

    columns.append({
        'label': value,
        'id': value,
        "deletable": True
    })

    return columns

