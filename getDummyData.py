import pandas as pd

#### MAKE RANDOM DATA

#printable ASCC is 32 to 126
from numpy.random import randint as NPrandint
def randString(len=100):
    return ''.join([chr(i) for i in NPrandint(32,126,len) ])

xs=[]
ys=[]
texts=[]
customs=[]
from random import randint
howMany = 15000
for i in range(howMany):
    xs.append( randint(0,1000) )
    ys.append( randint(0,1000) )
    texts.append(randString())
    customs.append('http://lab.e-nable.org?' + str(randint(0,3)))
colors = ys
######


postData = pd.DataFrame({
    'xs':xs,
    'ys':ys,
    'texts':texts,
    'customs': customs,
    'colors':colors
})

