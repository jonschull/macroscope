# ### Operating principles
# * read in dump.json as mazvy gives it. This will allow him to take responsiblity for updating or appending to dump.json.
# * Create new columns in dedicated cells; 
# * do not rewrite or drop original columns (to facilitate bug testing; unless memory becomes a problem)
#

# ### notes
# # #! conda install plotly
# # #! pip install markdownify
# #to use in jupyter requires the jupyterlab/plotly-extension
#
# `to use jupytext https://jupytext.readthedocs.io/en/latest/examples.html
#     use the terminals and extensions sidebar to 
#         pip install the jupytext extension using the extension manager
#     install juptext
#         use the terminals and extensions sidebar to pair your ipynb with a light script`
#     
#

# # code

noFigs=False


import plotly.express as px
import pandas as pd

df = pd.read_json('dump.json')
df.columns

df['threadY'] = (df.id - round(df.id) * 100000)
df['name'] = [user.replace('(Legacy) ', '') for user in df['user']] 
df['text'] = [tup.name + ' ' + str(tup.datetime)[:19] for tup in df.itertuples()] #Jon Schull 2013-07-10 20:01:06


# # Markdown

from IPython.display import Markdown
from markdownOfThread import markdownOfThread
#Markdown(markdownOfThread(df,9))

df['threadY'] = (df.id - round(df.id) * 100000)
df['name'] = [user.replace('(Legacy) ', '') for user in df['user']] 
df['text'] = [tup.name + ' ' + str(tup.datetime)[:19] for tup in df.itertuples()] # Jon Schull 2013-07-10 20:01:06


df['IDcolor']=round(df['id']%10) #ten discrete colors.  
df['IDcolor'] = df['IDcolor'].astype(str) #needed for discrete colorscale?
df['threadPos'] = 0.01 + 100*(df.id - round(df.id))  #for sizing.  Grows with the post's position in the thread with a minimum size of 0.01

# +
#make UniqueNameNumbers
#names = df['user']
uniqueNames = []
for name in df.name:
    name = name.replace('(Legacy) ', '')
    if name not in uniqueNames:
        uniqueNames.append(name)
        
from collections import OrderedDict
uniqueNameNumbers = UNN = OrderedDict()
for i,name in enumerate( uniqueNames ):
    UNN[name] = i

UNNs = []
for name in df.name:
        UNNs.append(UNN[ name.replace('(Legacy) ','')])
#UNNs

df['UNN'] = UNNs
df['UNNcolor'] = df['UNN'] % 10
df['UNNcolor'] = df['UNNcolor'].astype(str)
df['smThreadPos'] = df.threadPos / 1000
# -
# # ThreadsFig, colored by threadID

# +
fig = px.scatter(df, x='datetime', y='id', hover_data=['id'], color='IDcolor', size='threadPos', height=400, hover_name='name', opacity=0.4, template='plotly_dark')
fig.update_layout(showlegend=False)
fig.update_yaxes(title_text='Successive Threads')
fig.update_xaxes(
     rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow')  
)

threadsFig = fig
#fig
# -



# # PeopleFig




# +
fig = px.scatter(df,x='datetime', y='UNN', hover_data=['id'], color='IDcolor',size='smThreadPos', height=400, hover_name='text', opacity=0.3, template='plotly_dark')
fig.update_layout(showlegend=False)
fig.update_yaxes(title_text='People ordered by first post')
fig.update_xaxes(
     rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow')  
)

peopleFig = fig
#peopleFig
# -

# # bothfig with custom xAxis

# +
#make customAxis 

df = df.sort_values('datetime')
#jonrows = df.query('UNN==0')
recs = df.to_dict('records')  

tickIDs = []
ticktext = []
for i, row in enumerate(recs):
    if i==0: 
        tickIDs.append(row['id'])
        ticktext.append(row['datetime'])
    else:
        if row['datetime'].day != recs[i-1]['datetime'].day:
            tickIDs.append(row['id'])
            ticktext.append(row['datetime'])

ticktext= [str(tt)[:10] for tt in ticktext]


downsample = 20
ticktext = [tt for i,tt in enumerate(ticktext) if i%downsample == 0 ]
tickIDs = [id for i, id in enumerate(tickIDs)  if i%downsample == 0 ]

            
customXaxis=dict(
                             tickmode = 'array',
                             tickvals = tickIDs,
                             ticktext = ticktext
                   )

            
fig = px.scatter(df, y='UNN', x='id',hover_data=['id'], color='IDcolor', height=400, size='smThreadPos', hover_name='text', opacity=0.3, template='plotly_dark')
fig.update_layout(showlegend=False,
                  xaxis = customXaxis
                 )
fig.update_yaxes(title_text='People ordered by first post')
fig.update_xaxes(title_text='Successive Threads over time.', 
                 rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow'),
                )

bothFig = fig

#bothFig
# -
# # Dash App! 
# requires the dash jupyter_lab extension in Jupyter be pip installed and enabled in Extension Mgr

# # inJupyter?
# ## when used with the jupytext extension, this is intended to allow me to run 
# python macrosmodule.py (ipython doen't work because of the extensions own clever check own  )
# and 

import jupyterlab_dash #https://github.com/plotly/jupyterlab-dash
#TEMP
import dash
app = dash.Dash(__name__)







import dash
import dash_html_components as html


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import visdcc


from dash.dependencies import Input, Output, State

# +
app = dash.Dash(__name__)


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
                        html.H1('These are data from G+ and Wikifactory...'),
                        html.Br(),
                        html.Span('Filter posts by Content or Author:  '),            
                        Cfilter,
                        dcc.Markdown("""
* **Mouse over** a data point to see author and date.
* **Click** on a data point to view the Thread.
* **(Soon:) Click on the Participate button** to visit the live thread at [hub.e-nable.org](hub.e-nable.org).
                        """),
                    
                        visdcc.Run_js(id = 'javascript'),
                        dbc.Row([     dbc.Col([
                                            html.H1('People'),
                                            dcc.Graph(id='peopleFig', figure=peopleFig),
                                            html.P('Horizontal Bands are People. Dots are posts.'),

                                            ]
                                    ),
                                            
                                      dbc.Col([
                                            html.H1('Threads'),
                                            dcc.Graph(id='threadFig', figure=threadsFig),
                                            html.P('Horizontal Bands are Threads. Dots are posts.'),

                                      ]
                                    )
                                ]),
                        
                        html.H1('People and Threads'),
                        html.P('Horizontal Banda are People.  Vertical columns of the same color are Threads.'),
                        dcc.Graph(id='bothFig', figure=bothFig)
                    ]),
             ])
    ],className="mt-4",)




app = dash.Dash(__name__, external_stylesheets=['assets/bootstrap-grid.min'])  ### now uses css in assets dir?
app.layout = html.Div(body)



@app.callback(
    Output('HoverBox' , 'children'),
    [Input('threadFig', 'clickData'),
     Input('peopleFig', 'clickData'),
     Input('bothFig'  , 'clickData')
    ]
)


def updateSpan(tdata, pdata, bdata):
    ctx = dash.callback_context
    if ctx.triggered:
        if ctx.triggered[0]['value']:
            source =       ctx.triggered[0]['prop_id'].split('.')[0]
            customdata =   ctx.triggered[0]['value']['points'][0]['customdata'][0]
            return f"""{source} {customdata} 
            
            
            {markdownOfThread(df, float(customdata))}
            
            """
    return 'nothing yet'
    

    
import sys    
inJupyter = sys.argv[-1].endswith('json')
print(f'inJupyter: {inJupyter}')

if inJupyter:
    if not 'viewer' in globals().keys():
        viewer = jupyterlab_dash.AppViewer() #create the viewer once
    viewer.show(app)
else:
    if __name__ == "__main__":
        app.run_server(debug=True)

# -
globals().keys()


viewer

viewer.show(app)

viewer

viewer.terminate()


viewer





