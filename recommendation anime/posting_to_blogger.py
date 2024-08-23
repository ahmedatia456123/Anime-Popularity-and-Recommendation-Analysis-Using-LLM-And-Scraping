import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import pandas as pd
import json
import time
import csv
from urllib.parse import urlparse
from googletrans import Translator
translator = Translator()

blogger_id = 'add you blog id'
# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'place credentials.json file'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

# print(credentials)
def getBloggerService():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def postToBlogger(payload):
    service = getBloggerService()
    post=service.posts()
    insert=post.insert(blogId=blogger_id,body=payload).execute()
    print("Done post!")
    return insert

def buildHtml():
    html = '<h1>Hello world</h1>'
    return html

title = "Testing post 2" 
def update_post(post_id, new_title, new_content, new_labels=None, new_custom_metadata=None,excerpt=None):
  service = getBloggerService()
  post = service.posts()

  # Prepare the update payload
  payload = {
      "id": post_id,  # Specify the post ID to update
  }

  # Include updated fields if provided
  if new_title:
    payload["title"] = new_title
  if new_content:
    payload["content"] = new_content
  if new_labels:
    payload["labels"] = new_labels
  if new_custom_metadata:
    payload["customMetaData"] = new_custom_metadata
  if excerpt:
    payload["excerpt"] = excerpt

  # Update the post
  try:
    post.update(blogId=credentials, postId=post_id, body=payload).execute()
    print(f"Post with ID {post_id} successfully updated!")
  except Exception as e:
    print(f"Error updating post: {e}")
    
    
# preparing post
animeblog = pd.read_csv('published.csv')



nan = None

def build_list(row):
   
    recs=eval(row.rec)
    ready=eval(row.ready)
    output_html = ''
    breaking= '<span><!--more--></span>'
    for anime in ready:
        anime_name = anime['input']['anime2']
        poster=None
        for rec in recs:
            if anime_name.strip() == rec['title'].strip():
                
                poster = f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/{rec['poster']}"
        try:
            output_html = output_html + f'''
                <li class="maininfo">
               <div class="top_side">
                  <h3 class="main_name">{anime_name}</h3>
               </div>
               <div class="bottom_side">
                  <div class="right_data">
                     <div class="poster"> <img alt="أنمي {anime_name}" loading="lazy" src="{poster}"></div>
                  </div>
                  {breaking}
                  <div class="comparition">
                  <div id="main_point"><b>أوجه التشابه</b></div>
                  <div class="similarities">{''.join([f'<div id="point"><b>{simi["point"]}</b><span id="point_details">{simi["details"]}</span> </div>' for simi in anime['output']['similarties']])}</div>
                  <div id="main_point"><b>أوجه الأختلاف</b></div>
                  <div class="diffrancies">{''.join([f'<div id="point"><b>{simi["point"]}</b><span id="point_details">{simi["details"]}</span> </div>' for simi in anime['output']['diffrancies']])}</div>
                  
                  
                  </div>
                            
               </div>
            </li>
                ''' 
            breaking = ''
        except:
            continue
        
    return output_html

def buildPost(row):
    
    poster = eval(row.blogger_script)['poster']
    
    html = f'''
    <img alt="أنمي {row['name']}" id='main_anime' loading="lazy" src="{poster}">
    <div id="recommendation" class="listContainer">
    <ul>
    {build_list(row)}
    </ul>
    </div>

    '''
    return {'html':html.strip(),'title':f"أفضل انميات مثل {eval(row.ready)[0]['input']['anime1']}",'label':'انميات مقترحة'}
    
    

#savering
class EfficientSaver:
  """
  Class to efficiently save data to CSV file.
  """

  def __init__(self, filename, headers):
    self.filename = filename
    self.headers = headers
    self.open_file()

  def open_file(self):
    """Opens the CSV file in append mode."""
    self.csvfile = open(self.filename, 'a', newline='',encoding='utf-8')
    self.writer = csv.writer(self.csvfile)
    # Write header only if file is empty
    if self.csvfile.tell() == 0:
      self.writer.writerow(self.headers)

  def save_item(self, item):
    """Saves a single item's data to the CSV."""
    data_row = [item.get(header) for header in self.headers]
    self.writer.writerow(data_row)

  def close(self):
    """Closes the CSV file."""
    self.csvfile.close()

filename = 'publishedd.csv'
headers = [ 'postid','mal_id']
saver = EfficientSaver(filename, headers)


postlist = []
checking = True

counter = 0


for i,raw in animeblog[animeblog.postid.isna()].iterrows():
    if i <=1349:
        continue
    try:
        counter = counter+1
        if counter == 100:
            break
        mdl_id = raw.mal_id

        #post_id = raw.postid.replace('-','')
        data = buildPost(raw)
        
        
        
        payload={
            
            "content": data['html'],
            "title": data['title'],
            'labels': data['label'],
        }
        bpost_id = postToBlogger(payload)['id']
        #update_post(post_id, data['title'], data['post_body'], new_labels=data['labels'], new_custom_metadata=None,excerpt=None)
        finaldata = {
        'postid':f'-{bpost_id}',
        'mal_id':mdl_id,
        }
        animeblog.at[i,'postid'] = f'{bpost_id}-'
        saver.save_item(finaldata)
        print(f"{i} - {len(animeblog)} - {mdl_id} - {counter}")
        print(data['title'])
        
        time.sleep(11)
    except Exception as e:
        print(e)
        break
        
    

animeblog.to_csv('published.csv',index=False)
saver.close()

# cd desktop/recommendation anime 

# python posting_to_blogger.py  
