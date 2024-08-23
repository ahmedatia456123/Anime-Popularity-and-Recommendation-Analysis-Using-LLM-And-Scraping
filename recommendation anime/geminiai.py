"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""
key = "place you key"
import os
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import json
import time
import csv
# Construct the full command string
command = "gcloud auth application-default login --client-id-file=client_secret.json --scopes https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.tuning,https://www.googleapis.com/auth/generative-language.retriever"

# Run the command
creds = os.system(command)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

def load_creds():
    """Converts `client_secret.json` to a credential object.

    This function caches the generated tokens to minimize the use of the
    consent screen.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
    

#creds = load_creds()

genai.configure(credentials=creds)
print('Available base models:', [m.name for m in genai.list_models()])


"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""




# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 20000,

}


model = genai.GenerativeModel(
  model_name="tunedModels/comparing-animes-wal383hukdq2",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

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

filename = 'published.csv'
headers = [ 'rec','mal_id','name','post','postid','ready','mainTag']
saver = EfficientSaver(filename, headers)

df = pd.read_csv('../Anime_data.csv')

check=True
qouta=False

for index,row in df.iterrows():
    
    recs = eval(row.blogger_rec)
    
    if len(recs) < 3:
        continue
    mal_id = row.myanimelist_id
    output=[]

    
    for rec in recs:
        
        if qouta:
            break
        try:
            testing = int(rec['rating'])
        except:
            
            continue
        passit=True
        counter = 0
        while passit and counter<=1:
            try:
                genai_obj = json.dumps({"anime1":row['name_x'],"anime2":rec['title']})
                
                response = model.generate_content([
                  genai_obj
                ],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                }
                )
                output.append({"input":genai_obj,"output":response.text,"poster":rec["poster"],"rating":rec["rating"]})
                
                print(f"{row['name_x']} --  {rec['title']}")
                passit=False
                #time.sleep(4)
            except Exception as e:
                counter = counter +1
                print(e)
                try:
                    if "Resource has been exhausted" in str(e):
                        qouta=True
                        break
                except:
                    pass
                
    if qouta:
        break    
            
    data = {
    "rec":row.blogger_rec,
    "mal_id":row.myanimelist_id,
    "name":row['name_x'],
    "post":output,
    "postid":None,
    "ready":None,
    "mainTag":row.mainTag,
    }
    
    saver.save_item(data)
    print(f"{index} - {len(df)} - {mal_id} - {row['name']}")
    
saver.close()

