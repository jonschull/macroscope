#https://dash-bootstrap-components.opensource.faculty.ai
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import visdcc
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
    


Cfilter = dcc.Input(id='Cfilter',
                       placeholder='word or phase...',
                       type='text',
                       value=''
                   )



body = dbc.Container([
        dbc.Row([
                dbc.Col([  html.H2("Selected Thread"),
                           dcc.Markdown('selected thread __goes here__', id='HoverBox')],
                    md=4,
                ),
                dbc.Col([   
                        html.H1('These are data from G+ and Wikifactory.'),
                        html.Br(),
                        html.Span('Filter posts by Content or Author:  '),            
                        Cfilter,
                        dcc.Markdown("""
* **Mouse over** a data point to see author and date.
* **Click** on a data point to view the Thread.
* **(Soon:) Click on the Participate button** to visit the live thread at [hub.e-nable.org](hub.e-nable.org).
                        """),


                        visdcc.Run_js(id = 'javascript'),
                        dcc.Graph(id='graph')
                    ]),
             ])
    ],className="mt-4",)

app = dash.Dash(__name__, external_stylesheets=['assets/bootstrap-grid.min'])  ### now uses css in assets dir?
app.layout = html.Div(body)


df = pd.read_json('dataForGraph.json')
df.sort_values('isoformat')


def graphFromRows(newdf):
    return dict(
        data = [
            go.Scattergl(
                x = newdf['isoformat'],
                y=  newdf['ys'],
                mode='markers',
                marker=dict(
                    size=4,
                    symbol='square',
                    color= newdf['colors'],
                    colorscale='Jet'
                ),
                name='JonTest',
                hovertext =  newdf['texts'],
                hoverinfo = 'text', #could be changed for Date and Name
                customdata= newdf['ID']
            )
        ],

        layout = go.Layout(
            hovermode='closest',
            title="People and Posts over time, colored by Person",
            xaxis_title="Time",
            yaxis_title="People",
            height= 800,
            #width=  400
        )
    ) 


@app.callback( Output('graph', 'figure'), 
              [Input('Cfilter','value')] )

def filter(Cvalue): 
    Cquery = df.body.str.contains(Cvalue, case=False)         
    Aquery = df.username.str.contains(Cvalue, case=False)   

    newdf=df[Cquery | Aquery]
    
    return graphFromRows(newdf)


from markdownize import markdownOfPost, markdownOfThread, getPostsFromThread

@app.callback(
    Output('HoverBox', 'children'),
    [Input('graph', 'clickData')])
def updateSpan(clickData):
    if clickData:
        ID = clickData['points'][0]['customdata']
        return markdownOfThread(ID)


""" showclick is the window opener.  
This worked when customdata was a URL.  Kept here for posterity.

@app.callback(
    Output('javascript', 'run'),
    [Input('graph', 'clickData')])
def showclick(clickdata): #clickdata currently does nothing
    if clickdata:
        url = clickdata['points'][0]['customdata']
        print(url)
        return f"window.open('{url}')"
    return
"""               


if __name__ == "__main__":
    app.run_server(debug=True)
    
    
print('STYLE NEEDS TO BE CONNECTED TO INTERNET')