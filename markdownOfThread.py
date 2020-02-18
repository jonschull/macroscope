#derived from markdownize.py
def avatarImg(username=''):
    return f'http://res.cloudinary.com/e-nable-org/image/upload/w_150,r_max/{username}'                         #show it

def getPostsFromThread(df, ID = 11):
    roundvalue = round(ID)
    return [post for post in df.to_dict('records') if roundvalue <= float(post['id']) < roundvalue + 1]





# +
def markdownOfThread(df, ID=11.3):
    from markdownify import markdownify as md
    RET='\n'
    posts = getPostsFromThread(df, ID)
    
    
    
    
    title = f"""**{posts[0]['body'][:80]}...**
    
Category:{posts[0]['topics']}

{str(posts[0]['datetime'])[:-15]} | {str(posts[0]['datetime'])[11:16]}  **[>>>Hub.e-nable.org]({posts[0]['permalink']})**
___
"""
            
    content = [f'\n{title}\n\n']
    for post in posts:
        postBody = md(post['body'])#.replace('<p>',RET).replace('</p>',RET)
        content.append(
f"""
![avatar]({avatarImg(post['name'])})  {post['name']}  

{str(post['datetime'])[:-15]} | {str(post['datetime'])[11:16]}


{postBody}
___
""")

    markdown = '\n'.join(content)
    return markdown

import sys
inJupyter = sys.argv[-1].endswith('json')
print(f'inJupyter: {inJupyter}')
if inJupyter:
    import pandas as pd
    df = pd.read_json('dump.json')
    df['name'] = [user.replace('(Legacy) ', '') for user in df['user']] 


    from IPython.display import Markdown, display
    display(Markdown(markdownOfThread(df, 6)))
# -

if __name__=='__main__':
    import pandas as pd
    df = pd.read_json('dump.json')
    df['name'] = [user.replace('(Legacy) ', '') for user in df['user']] 


    from IPython.display import Markdown, display
    display(Markdown(markdownOfThread(df, 6)))




