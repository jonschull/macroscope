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
fig = px.scatter(df, x='datetime', y='id', color='IDcolor', size='threadPos', height=800, hover_name='name', opacity=0.4, template='plotly_dark')
fig.update_layout(showlegend=False, 
                  title_text='Threads: Posts over Time, Colored by Thread, Sized by Position in Thread')
fig.update_yaxes(title_text='Successive Threads')
fig.update_xaxes(
     rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow')  
)

threadsFig = fig
# -

fig

# # PeopleFig




# +
fig = px.scatter(df,x='datetime', y='UNN', color='IDcolor',size='smThreadPos', height=800, hover_name='text', opacity=0.3, template='plotly_dark')
fig.update_layout(showlegend=False, 
                  title_text='People: Posts over Time, Colored by Thread')
fig.update_yaxes(title_text='People ordered by first post')
fig.update_xaxes(
     rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow')  
)

peopleFig = fig
peopleFig
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

            
fig = px.scatter(df, y='UNN', x='id',color='IDcolor', height=800, size='smThreadPos', hover_name='text', opacity=0.3, template='plotly_dark')
fig.update_layout(showlegend=False, 
                  title_text="""Horizontal bands are People. Vertical columns of the same color are threads involving multiple people.""",
                  xaxis = customXaxis
                 )
fig.update_yaxes(title_text='People ordered by first post')
fig.update_xaxes(title_text='Successive Threads over time.', 
                 rangeslider=dict(visible=True, thickness=0.02, bgcolor='yellow'),
                )

bothFig = fig

bothFig
# -




