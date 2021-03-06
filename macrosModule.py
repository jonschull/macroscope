# + [markdown]
# ### Operating principles

# + [markdown]
# * read in dump.json as mazvy gives it. This will allow him to take responsiblity for updating or appending to dump.json.
# * Create new columns in dedicated cells; 
# * do not rewrite or drop original columns (to facilitate bug testing; unless memory becomes a problem)
#
# ### notes
# `conda install plotly
# pip install markdownify
# to use in jupyter requires the jupyterlab/plotly-extension
#
# o use jupytext https://jupytext.readthedocs.io/en/latest/examples.html
#     use the terminals and extensions sidebar to 
#         pip install the jupytext extension using the extension manager
#     install juptext
#         use the terminals and extensions sidebar to pair your ipynb with a light script`
#     
#     
# TODO: 
# * workwith mazvy on updating and avatar images
# * when showing only one graph, am I updating all three??
#     YES.  Could optimize by saving full graph in browser and by updating only the visible graph
#

# + [markdown]
# # code

# +
import plotly.express as px
import pandas as pd

df = pd.read_json('dump.json')
df.columns

df['threadY'] = (df.id - round(df.id) * 100000)
df['name'] = [user.replace('(Legacy) ', '') for user in df['user']] 
df['text'] = [tup.name + ' ' + str(tup.datetime)[:19] for tup in df.itertuples()] #Jon Schull 2013-07-10 20:01:06

# + [markdown]
# ### Markdown

# +
from IPython.display import Markdown
from markdownOfThread import markdownOfThread
#Markdown(markdownOfThread(df,9))

# ## addTo the dataFrame

df['threadY'] = (df.id - round(df.id) * 100000)
df['name'] = [user.replace('(Legacy) ', '') for user in df['user']] 
df['text'] = [tup.name + ' ' + str(tup.datetime)[:19] for tup in df.itertuples()] # Jon Schull 2013-07-10 20:01:06


df['IDcolor']=round(df['id']%10) #ten discrete colors.  
df['IDcolor'] = df['IDcolor'].astype(str) #needed for discrete colorscale?
df['threadPos'] = 0.01 + 100*(df.id - round(df.id))  #for sizing.  Grows with the post's position in the thread with a minimum size of 0.01


# + [markdown]
# ### make UniqueNameNumbers

# +
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


# + [markdown]
# ## makeCustomXaxis for the bothFig

# +
def makeCustomXaxis(df): #for bothFig
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
    return customXaxis


# ##  makeFig, makeFigs

# # +
def makeFig(df, x='datetime', y='UNN', customAxis=False, 
            plotTitle='', yTitle='',color='IDcolor'):
    
    fig = px.scatter(df,x=x, y=y, hover_data=['id'], 
                     color= color, size='smThreadPos', 
                     height=400, hover_name='text',
                     opacity=0.3, template='plotly_dark',
                    )
    
    fig.update_layout(showlegend=False, 
                      title=plotTitle,
                     )
    
    fig.update_xaxes(
         rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow')  )
    
    fig.update_yaxes(title_text=yTitle,  fixedrange=False)
    
    if customAxis:
        fig.update_xaxes(title_text = 'Successive Threads over Time')
        fig.update_layout(showlegend=False,
                          xaxis = makeCustomXaxis(df) )
    return fig

def makeFigs(df):
    """return a dictionary of figs
    """

    figs = OrderedDict() 

    figs['peopleFig'] = makeFig(df, x='datetime', y='UNN', color='IDcolor',
                            plotTitle='People over time. Colored by Thread',
                            yTitle = 'People in order of appearance.')

    figs['threadsFig'] = makeFig(df, x='datetime', y='id', color='UNNcolor',
                           plotTitle='Threads over time. Colored by Person',
                           yTitle = 'Posts in order of appearance')

    figs['bothFig'] =  makeFig (df, x='id', y='UNN', customAxis=True, color='UNNcolor',
                            plotTitle='People and Threads over Time. Colored by Person',
                            yTitle = 'People in order of appearance')
    return figs

fullFigs = makeFigs(df) #these will be global and cooked.
fullFigs.keys()
# -



# + [markdown]
# # Dash App! 
#
# in Jupyter, requires the dash jupyter_lab extension (pip installed and enabled in Extension Mgr)
#
# ## Develop and test Components
#

# +
import sys    
inJupyter = sys.argv[-1].endswith('json')
print(f'inJupyter: {inJupyter}')

if inJupyter:
    import jupyterlab_dash #https://github.com/plotly/jupyterlab-dash

# +

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import visdcc #used for javascript.  Not currently used


# #### layout Tester 

# # +
def testLayoutInJupyter(layout=html.H1('hello')):
    if not inJupyter:
        return
        
    global viewer
    
    app=dash.Dash(__name__)
    app.layout = layout
    
    if not 'viewer' in globals(): #create the viewer once
        viewer = jupyterlab_dash.AppViewer() 
        
    viewer.show(app)
    return viewer

viewer = testLayoutInJupyter()

#to destroy:
#viewer.terminate()
#del(viewer)

# + [markdown]
# ### leftPanel

# +
leftPanel = dbc.Col([  html.H2("Selected Thread"),
                           dcc.Markdown('selected thread __goes here__', id='HoverBox')],
                    width=3,
                    style={'overflowY': 'scroll', 'height': 1200}
                )
viewer = testLayoutInJupyter(leftPanel)

# + [markdown]
# #### dropDown

# +
dropDown = dcc.Dropdown(
                        id='dropdown',
                        style={'color':'#000'},
                        options=[
                            {'label': 'All three graphs', 'value': 'allThree'},                            
                            {'label': 'Just People and Threads over time, Color=Thread', 'value': 'justOne'},
                        ],
                        value='allThree'
                    )
viewer = testLayoutInJupyter(dropDown)


# + [markdown]
# ### twinRow 
# (side by side People and Thread figs)

# +
def twinRow(hide_twinRow=False):
    if hide_twinRow:
        return dbc.Row(children = [ dbc.Col(  style={'display': 'none'}, width=6, children = [ dcc.Graph(id='peopleFig', figure=fullFigs['peopleFig']), ]),
                                dbc.Col(   style={'display': 'none'}, width=6, children = [ dcc.Graph(id='threadsFig',   figure=fullFigs['threadsFig']) ])], 
                 id= 'twinRow', style={'background-color':'#111'}, no_gutters= True )

    
    #else
    return dbc.Row(children = [ dbc.Col( width=6, children = [ dcc.Graph(id='peopleFig', figure=fullFigs['peopleFig']), ]),
                                dbc.Col(width=6, children = [ dcc.Graph(id='threadsFig',   figure=fullFigs['threadsFig']) ])], 
                 id= 'twinRow', style={'background-color':'#111'},  no_gutters= True )

viewer = testLayoutInJupyter(twinRow())

# + [markdown]
# ### Searchbox

# +
searchBox = html.Div(
        [html.Span(id='numFound', children=f'{len(df)}'),
         html.Span(' datapoints'),
         html.Br(),
         html.Span('Filter by '),
         dcc.Input(id='Cfilter',
                       placeholder='name or phrase, or query like == threadID>10000',
                       type='text',
                       size = '50',
                       value=''),
          
          html.Button('Redraw!', id='Redraw!'),
          html.P(id='searchBoxMessage')
        ],
                   id='searchBox'
                  )


viewer = testLayoutInJupyter(searchBox)


# + [markdown]
# #### test SearchBox

# +
def queryResponse(queryPhrase='6<id<7'):
    testerdf =   df.head(1)     
    Error=''
    
    try:
        testerdf.query(queryPhrase)
    except  Exception:
        Error = '[Bad Query]'
        return Error, None

    if not Error:
        newdf = df.query(queryPhrase)
        return str(len(newdf)), newdf
    
queryResponse('6<id<8')[0]


# +

# -

# ### right panel

# +
def rightPanel(hide_twinRow=False):
    return dbc.Col(id='rightPanel',
                    style={'background-color':'#111', 'color':'#FFF'},
                    width=9,
                    children = [   
                        html.P(id='msgBox', children=''),
                        html.H3('e-NABLE on G+, Wikifactory, and hub.e-NABLE.org...'),
                        html.Br(),
                        searchBox,
                        dcc.Markdown("""
* **Mouse over** a data point to see author and date.
* **Click** on a data point to view the Thread or **>>>Participate** at hub.e-nable.org
                        """),
                       dropDown,  
                       #html.P(),
                       visdcc.Run_js(id = 'javascript'),
                       twinRow(hide_twinRow), 
                       dcc.Graph(id='bothFig', figure=fullFigs['bothFig'],
                       style={'background-color':'#111'}
                   ) 
                ])

testLayoutInJupyter(rightPanel())

# + [markdown]
# ### both Panels

# + [markdown]
# ## App with Callbacks

# +
app = dash.Dash(__name__)

app = dash.Dash(__name__, external_stylesheets=['assets/bootstrap-grid.min'])  ### now uses css in assets dir?

app.layout = dbc.Container(dbc.Row([
                leftPanel,
                rightPanel(False)]), fluid=True)

from dash.dependencies import Input, Output, State

######################################
#SearchBox Callbacks
####### update Figures with when ........ Redraw!
@app.callback(
    [Output('peopleFig','figure'),
     Output('threadsFig','figure'),
     Output('bothFig','figure')],
    [Input('Redraw!', 'n_clicks'),
     Input('Cfilter','value')]
)
def updateFigures(redraw, searchPhrase):
    source='unknown'
    
    ctx = dash.callback_context
    if ctx.triggered:
        if ctx.triggered[0]['value']:
            source = ctx.triggered[0]['prop_id'].split('.')[0]

    if source =='Redraw!':
        #first get newdf
        if searchPhrase.startswith('=='):
            queryPhrase = searchPhrase[2:]
            newdf = queryResponse(queryPhrase)[1]
        else:
            Cquery = df.body.str.contains(searchPhrase, case=False)         
            Aquery = df.name.str.contains(searchPhrase, case=False)
            newdf=df[Cquery | Aquery]

        #then redraw
        numFound = len(newdf)
        if numFound == 0:
            return list(makeFigs(df).values()) 
        else:
            return list(makeFigs(newdf).values()) 
        
    return [dash.no_update, dash.no_update, dash.no_update] #otherwise, no update

################################
##### UpdateNumFound with query
@app.callback(
    Output('numFound','children'),  #change 
    [Input('Cfilter', 'value')]
)
def updateNumFound(searchPhrase):
    if searchPhrase.startswith('=='):
        queryPhrase = searchPhrase[2:]
        return f'{queryPhrase} =>> {queryResponse(queryPhrase)[0]}'

    Aquery = df.name.str.contains(searchPhrase, case=False)
    Cquery = df.body.str.contains(searchPhrase, case=False)         
    newdf=df[Cquery | Aquery]

    return str(len(newdf))

################################
####### Dropdown Callback
@app.callback(
    Output('twinRow','children'),
    [Input('dropdown', 'value')]
)
def test(dropdown):
    hide_twinRow = dropdown == 'justOne'
    return twinRow(hide_twinRow).children

################################
####### ThreadBox callBack

@app.callback(
    [Output('HoverBox' , 'children'),
     Output('Cfilter',   'value'   )    ],
    
    [Input('threadsFig', 'clickData'),
     Input('peopleFig', 'clickData'),
     Input('bothFig'  , 'clickData')     ]
)
def updateThreadBox(tdata, pdata, bdata):
    ctx = dash.callback_context
    if ctx.triggered:
        if ctx.triggered[0]['value']:
            
            source =       ctx.triggered[0]['prop_id'].split('.')[0]
            customdata =   ctx.triggered[0]['value']['points'][0]['customdata'][0]
            
            threadRet = f""" {source} {customdata} 
                        
            {markdownOfThread(df, float(customdata))}
            """
            
            queryRet = f'==   {round(customdata)} <= id < {round(customdata+1)}'
            return [threadRet, queryRet]
     
    return [dash.no_update, dash.no_update]

if inJupyter:  #this allows running via python 
    if not 'viewer' in globals().keys():   #create the viewer once
        viewer = jupyterlab_dash.AppViewer()
    viewer.show(app)
else:
    if __name__ == "__main__":
        app.run_server(debug=True)

# -

# !python macrosmodule.py  #you can interrupt kernel to stop






