#import libraries
from os import name
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import psycopg2
from mastodontool import settings

conn = psycopg2.connect(
    dbname=settings.DATABASES.get("default",{})["NAME"],
    user=settings.DATABASES.get("default",{})["USER"],
    password=settings.DATABASES.get("default",{})["PASSWORD"],
    host=settings.DATABASES.get("default",{})["HOST"],
)

query = "SELECT * FROM uptime2"

instanceseries = pd.read_sql_query(query, conn)


def dash_plotly_plot(instance):

    conn = psycopg2.connect(
        dbname=settings.DATABASES.get("default",{})["NAME"],
        user=settings.DATABASES.get("default",{})["USER"],
        password=settings.DATABASES.get("default",{})["PASSWORD"],
        host=settings.DATABASES.get("default",{})["HOST"],
    )

    query = "SELECT * FROM uptime2 where instance = '" + instance + "'"

    instanceseries = pd.read_sql_query(query, conn)
    
    #Create graph object Figure object with data
    fig = go.Figure(data = go.Line(name = 'Plot1' + instance, x = instanceseries['date'], y = instanceseries['status']))
    
    #Update layout for graph object Figure
    fig.update_layout(
                      title_text = 'Variable: ' + instance,
                      xaxis_title = 'Variable1',
                      yaxis_title = 'Variable2')
    
    #return fig

#Create DjangoDash applicaiton
app = DjangoDash(name='instance_uptime', instancename='instancename')

#Configure app layout
app.layout = html.Div([
                html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure={
                        'data': [
                            {'x': instanceseries[instanceseries['name']=='instancename'].date, 'y': instanceseries[instanceseries['name']=='instancename'].date, 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': '20 most banned instances'
                        }
                    }
                )
            ], className = 'six columns'),
])
    