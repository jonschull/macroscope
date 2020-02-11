#!/usr/bin/env python
# coding: utf-8

# In[101]:



import pandas as pd
bodiesDF = pd.read_json('dataForGraph.json')
bodiesDF.sort_values('isoformat')


def avatarImg(username=''):
    return f'http://res.cloudinary.com/e-nable-org/image/upload/w_150,r_max/{username}'                         #show it

def getPostsFromThread(ID = 11):
    roundvalue = round(ID)
    return [post for post in bodiesDF.to_dict('records') if roundvalue <= float(post['ID']) < roundvalue + 1]

def markdownOfThread(ID=11.3):
    from markdownify import markdownify as md
    RET='\n'
    posts = getPostsFromThread(ID)
    
    title = f"""**{posts[0]['body'][:80]}...**
    
Category:{posts[0]['category']}

{posts[0]['isoformat'][:-15]} | {posts[0]['isoformat'][11:16]}
___
"""
            
    content = [f'\n{title}\n\n']
    for post in posts:
        postBody = md(post['body_html'])#.replace('<p>',RET).replace('</p>',RET)
        content.append(
f"""
![avatar]({avatarImg(post['username'])})  {post['username']}  

{post['isoformat'][:-15]} | {post['isoformat'][11:16]}

{postBody}
___
""")

    markdown = '\n'.join(content)
    return markdown


def markdownOfPost(ID=11.1):
    post = [post for post in bodiesDF.to_dict('records') if post['ID'] == ID]
    if not post:
        return
    else:
        post= post[0]
    title = post['body'][:80]
    content = [f'\n**{title}...**\n\n']
    content.append(
f"""
![avatar]({avatarImg(post['username'])}){post['username']} | {post['isoformat'][:-15]} | {post['isoformat'][11:16]}

{post['body_html']}
___
""")

    markdown = '\n'.join(content)
    return markdown



if __name__=='__main__':
    import pandas as pd
    from IPython.display import HTML, display, Markdown

    bodiesDF = pd.read_json('dataForHoverPanel.json')
    bodiesDF = bodiesDF.sort_values('isoformat')

    #display(Markdown(markdownOfThread(ID=11.2)))
    display(Markdown(markdownOfPost(  ID=0)))


# In[86]:


from IPython.display import HTML, display, Markdown


# In[104]:


Markdown(markdownOfThread(11595))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




