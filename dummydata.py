## Standalone dashapp that uses DummyData from getDummyData

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import visdcc
import pandas as pd

app = dash.Dash(__name__)

html.H1('These are dummy data with dummy titles.'),

app.layout = html.Div([
    html.Button('populate', id = 'populater'),
    html.H1('These are dummy data with dummy titles.'),
    html.Span('Filter posts by title:  '),
    dcc.Input(id='filter',
        placeholder='Filter by author...',
        type='text',
        value=''
    ), 
    html.Br(),
    html.Span('Filter posts by author:  '),
    dcc.Input(id='authorFilter',
        placeholder='Filter by title...',
        type='text',
        value=''
    ), 
    html.P('Mouse over a data point to see the title.  Click on a data point go to a URL.'),

    visdcc.Run_js(id = 'javascript'),
    
    dcc.Graph(id='graph')
    
])

from getDummyData import postData 
df=postData

""" The populaterizer filters and populates the graph. 
    It gets its input from filter
"""               
@app.callback(
    Output('graph', 'figure'),
    [Input('populater', 'n_clicks'), Input('filter','value')
    ])
def populaterizer(clicks,value): 
    
    #filter!
    query = df.texts.str.contains(value, case=False) 
    newdf = df[query]
    
    #populate
    return dict(
        data = [
            dict(x =          newdf['xs'], 
                 y =          newdf['ys'],
                 customdata = newdf['customs'],
                 hovertext =  newdf['texts'], 
                 hoverinfo = 'text', #could be changed for Date and Name
                 name = 'name',
                 mode = 'markers',
                 marker = dict(size=8,
                            symbol='square',
                            color=newdf['colors'],
                            opacity = 0.5)
             )
        ],
        
        layout =  dict(
                        clickmode ='event',
                        hovermode ='closest'
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
    