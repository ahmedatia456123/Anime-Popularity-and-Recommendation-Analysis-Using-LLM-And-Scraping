# Import necessary libraries for web scraping and data handling
from playwright.sync_api import sync_playwright
from seleniumbase import SB
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import re
import csv

# Read the CSV file containing links from MyAnimeList
df = pd.read_csv('myanimelist_link.csv')

class EfficientSaver:
    """
    Class to efficiently save data to a CSV file.
    """

    def __init__(self, filename, headers):
        # Initialize with the filename and headers
        self.filename = filename
        self.headers = headers
        self.open_file()

    def open_file(self):
        """Opens the CSV file in append mode."""
        # Open the CSV file in append mode with UTF-8 encoding
        self.csvfile = open(self.filename, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csvfile)
        # Write the header only if the file is empty
        if self.csvfile.tell() == 0:
            self.writer.writerow(self.headers)

    def save_item(self, item):
        """Saves a single item's data to the CSV."""
        # Save each item as a row in the CSV file
        data_row = [item.get(header) for header in self.headers]
        self.writer.writerow(data_row)

    def close(self):
        """Closes the CSV file."""
        # Close the CSV file
        self.csvfile.close()

# Filename for the output CSV and the headers for the columns
filename = 'myanimelist_data.csv'
headers = ['leftside', 'id', 'name', 'sup_name', 'poster', 'body']
saver = EfficientSaver(filename, headers)

# Start the Playwright context to automate the browser
with sync_playwright() as p:
    # Initialize an empty dictionary to store the final data
    final_data = {
        'leftside': None,
        'id': None,
        'name': None,
        'sup_name': None,
        'poster': None,
        'body': None,
    }

    # Launch the Chromium browser in non-headless mode (visible)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    def open_google():
        """Opens the Google homepage."""
        page.goto('https://www.google.com/', timeout=60000000)

    def get_html(keyword):
        """Fetches the HTML content of a given URL."""
        page.goto(keyword)
        # Wait for a specific element to load before proceeding
        page.wait_for_selector("#horiznav_nav", timeout=60000000)
        return page.content()

    # Open Google homepage before starting the scraping process
    open_google()

    # Iterate through each row in the DataFrame
    for i, raw in df.iterrows():
        my_id = raw['myanimelist_id']
        
        # Skip processing if the ID is in the skipping list
        if my_id in skepping:
            continue
        
        print(" --- ")
        
        # Reset final_data for each new entry
        final_data = {
            'leftside': None,
            'id': None,
            'name': None,
            'sup_name': None,
            'poster': None,
            'body': None,
        }
        
        # Get the link from the DataFrame
        link = raw['myanimelist']
        print(link)
        
        # Fetch the HTML content of the page
        html = get_html(link)
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract various data points using BeautifulSoup
        final_data['leftside'] = soup.find('div', {'class': 'leftside'})
        final_data['id'] = my_id
        
        try:
            final_data['name'] = soup.find('h1', {'class': 'title-name h1_bold_none'}).find('strong').text.strip()
        except:
            pass
        
        try:
            final_data['sup_name'] = soup.find('p', {'class': 'title-english title-inherit'}).text.strip()
        except:
            pass
        
        try:
            final_data['poster'] = soup.find('img', {'class': 'lazyloaded'})['data-src']
        except:
            pass
        
        try:
            final_data['body'] = soup.find('div', {'class': 'rightside js-scrollfix-bottom-rel'}).find('table')
        except:
            pass
        
        # Save the extracted data to the CSV file
        saver.save_item(final_data)
        print(f"{i+1} out of {len(df)} {final_data['name']}")
        
# Close the CSV file after all data has been saved
saver.close()
