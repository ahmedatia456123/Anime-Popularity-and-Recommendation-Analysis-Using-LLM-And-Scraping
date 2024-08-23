from playwright.sync_api import sync_playwright
from seleniumbase import SB
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import re
import csv
import requests

head = 'site:https://anilist.co anime '
df = pd.read_csv('../myanimelist/myanimelist_details_processed.csv')


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

filename = 'anlist_data.csv'
headers = [ 'mal_id','data']
saver = EfficientSaver(filename, headers)

query = '''
query ($kjkl: Int) {
  Media (idMal: $kjkl type:ANIME) {
    id
    idMal 
    title {
      romaji
      english
      userPreferred
    }
    type 
    format 
    description
    status
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    season
    seasonYear
    seasonInt
    episodes
    duration
    countryOfOrigin
    source
    hashtag
    trailer {
      id
      site
      thumbnail
    }
    updatedAt
    coverImage {
      extraLarge
      large
      medium
      color
    }
    bannerImage
    genres
    synonyms
    averageScore
    meanScore
    popularity
    trending
    favourites
    tags {
      id
      name
      description
      category
      rank
      isGeneralSpoiler
      isMediaSpoiler
      isAdult
    }
    relations {
      edges {
        node {
        coverImage{
        extraLarge
        large
        medium
        }
          id
          idMal
          title {
            romaji
            english
            native
            userPreferred
            }
          type
          format
          seasonYear
          
        }
        id
        relationType
      }
    }
    
    
  characters (sort:[ROLE ]) {
      edges {
        node {
          id
          favourites
          name {
            first
            last
            full
            alternative
            alternativeSpoiler
            userPreferred
            
          }
          image {
            large
            medium
          }

        }
        id
        role
        name
        voiceActorRoles (language:JAPANESE) {
          roleNotes
          voiceActor {
            id
            favourites
            name {
              first
              last
              full
              userPreferred
            }
            languageV2
            image {
            large
            medium
          }
          }
          
        }
        favouriteOrder
      }
    }


    staff (sort:[RELEVANCE ROLE]) {
      edges {
        node {
          id
          name {
              first
              last
              full
              userPreferred
            }
            languageV2
            image {
            large
            medium
          }
        }
        id
        role
        favouriteOrder
      }
    }

  studios (sort:FAVOURITES_DESC){
    edges {
      node {
        id
        name
        isAnimationStudio
        favourites
      }
      id
      isMain
      
    }
  }

  recommendations (sort:RATING_DESC) {
    edges {
      node {
        id
        rating
        mediaRecommendation {
          id
          idMal
          title {
            romaji
            english
            userPreferred
          }
          coverImage {
            extraLarge
            large
            medium
            color
          }
          bannerImage
        }

      }
    }
    
  }
    
  }
}
'''
url = 'https://graphql.anilist.co'
check = True
for i,raw in df.iterrows():
    
    my_id = raw['id']

 
    final_data = {
        'mal_id':None,
        'data':None,
    }
    variables = {
        "kjkl": int(my_id)
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    res = json.loads(response.text)
    
    final_data['mal_id'] = my_id = int(raw['id'])
    final_data['data'] = my_id = json.dumps(res)


    time.sleep(1)
    saver.save_item(final_data)
    print(f"{i+1} out of {len(df)} {final_data['mal_id']} {response}")
        
    


saver.close()


