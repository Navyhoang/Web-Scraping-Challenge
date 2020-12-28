# Dependencies for web scraping
from bs4 import BeautifulSoup

# Dependencies to visit web
import requests
import splinter 
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Dependencies to interact with MongoDB database
import pymongo

# Other modules
import json
import re
import pandas as pd
import time

url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url_3 = 'https://space-facts.com/mars/'
url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


def news_titles_description (url_1):
    
    # browser.visit(url_1)
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')

    html = requests.get(url_1)
    soup = BeautifulSoup(html.text, 'html.parser')

    results = soup.find()

    # Collect the latest News Title
    title = results.find('div', class_="content_title")
    news_title = title.a.text.strip()
        
    # Get paragraph texts
    paragraph = results.find('div', class_="rollover_description_inner")
    news_p = paragraph.text.strip()

    return news_title, news_p

def featured_img (url_2):
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser =  Browser('chrome', **executable_path, headless=False) 

    # Navigate with browser.visit
    browser.visit(url_2)

    time.sleep(1)

    #Get html content of the visited page
    html = browser.html

    # Start scraping using BS
    soup = BeautifulSoup(html, 'html.parser')

    # Click on the "Full Image" button
    browser.find_by_id("full_image").click()

    # Click on the "More Info" button
    browser.find_by_text("more info     ").click()

    # Start scraping the full_size image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_img = soup.find("img", class_='main_image')['src']

    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + featured_img

    browser.quit()

    return featured_image_url

def mars_facts (url_3):
    html = requests.get(url_3)
    soup = BeautifulSoup(html.text, 'html.parser')
    results = soup.find()

    # Scrape the table from the website
    table = results.find('table', class_="tablepress tablepress-id-p-mars", id="tablepress-p-mars")
    trs = table.find_all("tr")
    tds_column1 = table.find_all('td', class_='column-1')
    tds_column2 = table.find_all('td', class_='column-2')

    # Get values in column 1
    column1 = []

    for td in tds_column1:
        if (td):
            try:
                column1.append(td.text)
            except:
                pass

    # Get values in column 2
    column2 = []

    for td in tds_column2:
        if (td):
            try:
                column2.append(td.text)
            except:
                pass

    data = list(zip(column1,column2))

    # Import column1 and column2 into Pandas DataFrame
    mars_fact_df = pd.DataFrame(data, columns=['Parameter', 'Value']).set_index('Parameter')

    mars_fact_html = mars_fact_df.to_html(header=True, index=False)

    return mars_fact_html
    
def mars_hemispheres(url_4):
    html = requests.get(url_4)
    soup = BeautifulSoup(html.text, 'html.parser')
    results = soup.find_all('a', class_='itemLink product-item')

    # Extract all 4 links/href from the results
    titles = []
    img_urls = []
    hemisphere_image_urls = []
    merge_dict = {}
    title_dict = {}
    img_url_dict = {}

    for result in results:
        title = result.text
        tail = result.get('href')
        full_url = f'https://astrogeology.usgs.gov{tail}'
        
        # Open each link found using get request
        mar_html = requests.get(full_url)
        mars_soup = BeautifulSoup(mar_html.text, 'html.parser')
        
        # Once each link is opened, searcj for the full resolution image url link
        img_url = mars_soup.find("div", class_="downloads").a.get('href')
        
        titles.append(title)
        img_urls.append(img_url)
        
        keys_1 = ['title', 'title', 'title', 'title']
        keys_2 = ['img_url', 'img_url', 'img_url', 'img_url']
      
        # Create 1st dictionary
        for key in keys_1:
            for value in titles:
                title_dict[key] = value
        
        # Create  2nd dictionary

        for key in keys_2:
            for value in img_urls:
                img_url_dict[key] = value
        
        # Merge 2 dictionaries
        def Merge(img_url_dict,title_dict):
            res = { **img_url_dict, **title_dict}
            return res
        
        merge_dict = Merge(title_dict,img_url_dict)
        
        # Append the merge dictionaries into a list
        hemisphere_image_urls.append(merge_dict)

    return hemisphere_image_urls
        
def scrape():

    # Start running all scraping codes above     
    news_title_, news_p_ = news_titles_description (url_1)
    featured_image_url_ = featured_img (url_2)
    mars_fact_df_ = mars_facts (url_3)
    hemisphere_image_urls_ = mars_hemispheres(url_4)

    # Create a dictionary that contains all scraped information
    results_dict = {
                    "latest_news": news_title_,
                    "latest_news_paragraph": news_p_,
                    "current_featured_image_url": featured_image_url_,
                    "mars_facts": mars_fact_df_,
                    "mars_hemispheres_urls": hemisphere_image_urls_

                    }

    return results_dict

def insert_into_mongo():

    # # insert the results_dict into MongoDB database
    results_dict_ = scrape()

    # Use PyMongo to establish Mongo connection
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    # Create a database and a collection within the database on the local MongoDB
    mydb = client.scrape_mars_db
    mycol = mydb.scrape_mars

    # Insert results_dict to collection mycol
    mycol.insert_one(results_dict_)


insert_into_mongo()

