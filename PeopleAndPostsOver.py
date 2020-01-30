#!/usr/bin/env python
# coding: utf-8

# In[1]:


from imports import *

#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')


# In[2]:


from getRealData import postData
df = postData


# In[9]:


df.columns


# In[10]:


df = df.sort_values('timeInt')


# In[35]:


titles = [s[:80] for s in df['body']]
usernames = [a['username'] for a in df['author']]

texts = []
for i, username in enumerate(usernames):
    texts.append(f'{username}: {titles[i]}')
    
customs= [f'https://lab.e-nable.org?{ID}' for ID in df['ID'] ]
#ys = [round(ID) for ID in df['ID']]


# In[38]:


uniqueUserNames = [] #these should preserver order in which usernames appear on the scene
for username in usernames:
    if username not in uniqueUserNames:
        uniqueUserNames.append(username)

userNameNumbers = dict()
for i, uUN in enumerate(uniqueUserNames):
    userNameNumbers[uUN] = i

ys = [userNameNumbers[username] for username in usernames]

colors = [ y % 12 for y in ys]
    
df['ys'] = ys
df['texts'] = texts
df['customs'] = customs
df['colors']  = colors

# In[22]:


#userNameNumbers


# In[ ]:


#COLOR BY THREAD
#colors = [round(id%12) for id in df['ID']]
#dcolors


# In[37]:


import plotly.graph_objs as go
data = [
    go.Scattergl(
        x=df['timeInt'],
        y=ys,
        mode='markers',
        marker=dict(
            size=4,
            symbol='square',
            color= colors,
            colorscale='Jet'
        ),
        name='JonTest',
        hovertext =  texts,
        hoverinfo = 'text', #could be changed for Date and Name
        customdata= customs
    )
]

layout = go.Layout(
    hovermode='closest',
    title="People and Posts over time",
    xaxis_title="Time",
    yaxis_title="People",
    height=1000,
    width=1500
)
 


from makeFig import  makeFig

fig = makeFig(data, layout, 'PeopleOverTime.html')
    
print('People and posts over time.  Colored by user')
fig


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




