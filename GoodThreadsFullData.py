#!/usr/bin/env python
# coding: utf-8

# In[10]:


#one big df 
import pandas as pd


def addRows(newdf):
    maxID = max(newdf['ID'])

    recs=[]
    lastID = -1
    for rec in newdf.to_dict('records'):
        if round(rec['ID']) > round(lastID):
            lastID+=1
            #rec = dict(ID=None, x=None, y=None, color=None) #insert blank rows so each thread stops at last item
            rec['x'] = None
            rec['y'] = None
            rec['ts'] = None
            rec['body'] = ''
            rec['body_html'] = None
            rec['username'] = None
            rec['isoformat'] = None
            rec['title'] = None
            recs.append(rec)
            lastID = rec['ID']
        #rec = dict(ID=rec['ID'], x=rec['ts'], y=rec['ID'] + 200000*(rec['ID'] - round(rec['ID'])), color=rec['colors'], IDcolor=int(rec['ID']%10))
                                                   #put comments higher
        rec['x'] = rec['ts']
        rec['y'] = rec['ID'] + 200000*(rec['ID'] - round(rec['ID']))
        rec['IDcolor'] = int(rec['ID']%10)
        recs.append(rec)

    recdf = pd.DataFrame(recs)
    return recdf


# In[11]:


import plotly.graph_objects as go

def threadGraph(recdf):
    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x = recdf.x,
            y = recdf.y,
            mode = 'markers+lines',
            line = dict(color='black',
                        width=0.5,
                       ),
            marker = dict(
                color = recdf.colors,
                colorscale='Jet',
                line={'color':recdf.IDcolor,
                     'width':1.1,
                     'colorscale':'jet'},
                size=7,
            )
        )
    )


    return fig


# In[13]:


if __name__ == '__main__':
    pd.set_option('display.max_rows', 20)
    from IPython.display import display
    df=pd.read_json('dataForGraph.json') 
    df = df.sort_values('ID')
    print(df.columns)
    
    recdf = addRows(df)
    
    display(threadGraph(recdf))


# In[ ]:





# In[ ]:




