# Dependencies
from bs4 import BeautifulSoup
import splinter 
from splinter import Browser
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd

# Use ChromeDriver to visit websites instead of get request method
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

def news_titles_description (url_1):
    
    browser.visit(url_1)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find()

    # Collect the latest News Title
    title = results.find('div', class_="content_title")
    news_title = title.a.text.strip()
        
    # Get paragraph texts
    paragraph = results.find('div', class_="rollover_description_inner")
    news_p = paragraph.text.strip()

    print(news_title)
    print("-------------")
    print(news_p)

news_titles_description(url_1)
