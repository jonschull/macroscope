#derived from postQueries.ipynb
import pandas
from pandas import DataFrame

def sortByID(t):
    return t['ID']

DFnormPosts = pandas.read_json('normPosts.json')  #read
JNnormPosts = DFnormPosts.to_dict('records')      #create Jason
DFnormPosts = DFnormPosts.sort_values('ID')
JNnormPosts.sort(key=sortByID)
len(DFnormPosts), len(JNnormPosts)

postData = DFnormPosts