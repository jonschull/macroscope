## Standalone dashapp that uses DummyData from getDummyData

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import visdcc
import pandas as pd

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1('These are data from G+ and Wikifactory.'),
    html.Span('Filter posts by title or author:  '),
    dcc.Input(id='filter',
        placeholder='Filter by title or author...',
        type='text',
        value=''
    ),  
    html.P('Mouse over a data point to see the title.  Click on a data point go to a URL.'),

    visdcc.Run_js(id = 'javascript'),
    
    dcc.Graph(id='graph')
    
])

from PeopleAndPostsOver import df


""" The populaterizer filters and populates the graph. 
    It gets its input from filter
"""               
@app.callback(
    Output('graph', 'figure'),
    [Input('filter','value')
    ])
def populaterizer(value): 
    
    #filter!
    query = df.texts.str.contains(value, case=False)         
    newdf = df[query]

    #populate
    return dict(
        data = [
            dict(x =          newdf['timeInt'], 
                 y =          newdf['ys'],
                 customdata = newdf['customs'],
                 hovertext =  newdf['texts'], 
                 hoverinfo = 'text', #could be changed for Date and Name
                 name = 'name',
                 mode = 'markers',
                 marker = dict(size=8,
                            symbol='square',
                            color=newdf['colors'],
                            opacity = 0.5,
                            colorscale='Jet'
                        )
             )
        ],
        
        layout =  dict(
                        clickmode ='event',
                        hovermode ='closest',
                        title="People and Posts over time",
                        xaxis_title="Time",
                        yaxis_title="People",
                        xaxis= dict(range= [min(df['timeInt']),
                                            max(df['timeInt'])
                                           ]),
                        height=800,
                        width=1200
                      ),
        )


""" showclick is the window opener.  
"""               

@app.callback(
    Output('javascript', 'run'),
    [Input('graph', 'clickData')])
def showclick(clickdata):
    if clickdata:
        url = clickdata['points'][0]['customdata']
        print(url)
        return f"window.open('{url}')"
    return
  
if __name__ == '__main__':
    app.run_server(debug=True)
    