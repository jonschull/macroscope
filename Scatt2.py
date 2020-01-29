#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


#https://community.plot.ly/t/hyperlink-to-markers-on-map/17858
from plotly.offline import plot
import pandas as pd
import plotly.graph_objs as go
import re
#printable ASCC is 32 to 126
from numpy.random import randint as NPrandint
def randString(len=100):
    return ''.join([chr(i) for i in NPrandint(32,126,len) ])

#randString()


# In[24]:


from getRealData import postData
df = postData


# In[29]:


df.columns


# In[89]:


titles = [s[:80] for s in df['body']]
usernames = [a['username'] for a in df['author']]

for i, username in enumerate(usernames):
    texts.append(f'{username}: {titles[i]}')
    
customs= ['https://lab.e-nable.org?urlgoeshere' for row in df ]
ys = [round(ID) for ID in df['ID']]


# In[90]:


uniqueUserNames = list(set(usernames))
userNameColors = dict()
for i, uUN in enumerate(uniqueUserNames):
    userNameColors[uUN] = i
#userNameColors


# In[78]:


#COLOR BY THREAD
#colors = [round(id%12) for id in df['ID']]
#dcolors


# In[ ]:





# https://plot.ly/python/v3/line-and-scatter/
# 
# Build scattermapbox trace and store URL's in the customdata
# property. The values of this list will be easy to get to in the
# JavaScript callback below
# Scattergl apparently faster https://plot.ly/python/v3/line-and-scatter/

# In[93]:


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

# Build layout
layout = go.Layout(
    hovermode='closest'
)
        

# Build Figure
fig = go.Figure(
    data=data,
    layout=layout)

# Get HTML representation of plotly.js and this figure
plot_div = plot(fig, output_type='div', include_plotlyjs=True)

# Get id of html div element that looks like
# <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
res = re.search('<div id="([^"]*)"', plot_div)
div_id = res.groups()[0]

# Build JavaScript callback for handling clicks
# and opening the URL in the trace's customdata 
js_callback = """
<script>
var plot_element = document.getElementById("{div_id}");
plot_element.on('plotly_click', function(data){{
    console.log(data);
    var point = data.points[0];
    if (point) {{
        console.log(point.customdata);
        window.open(point.customdata);
    }}
}})
</script>
""".format(div_id=div_id)

# Build HTML string
html_str = """
<html>
<body>
{plot_div}
{js_callback}
</body>
</html>
""".format(plot_div=plot_div, js_callback=js_callback)

# Write out HTML file
with open('Scatt2.html', 'w') as f:
    f.write(html_str)
    
#!open Scatt2.html
print('Thread over time.  Colored by user')
fig


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




