# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

#define browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():

    # Call in function browser
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Mars Recent News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_news = soup.find('div', class_='content_title').find('a')
    mars_title = mars_news.text.strip()
    mars_text = soup.find('div', class_='image_and_description_container').text
    print(f'{mars_title}: {mars_text}')

    mars_data["News_title"] = mars_title
    mars_data["News_summary"] = mars_text

    # Mars Twitter Weather
    url = 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    results = soup.find_all('p', class_='TweetTextSize')
    mars_weather = results[0].text

    print("Mars weather: ", mars_weather)

    mars_data["mars_weather"] = mars_weather

    # Mars Table of Facts
    url = 'https://space-facts.com/mars/'

    mars_facts = pd.read_html(url)
    df = mars_facts[0]
    renamed_df = df.rename(columns={0: 'feature', 1: 'data'})
    df = renamed_df.set_index("feature", inplace=False)
    df.to_html('mars_facts.html')

    mars_data["mars_information"] = df

    # Mars Hemisphere Images
    Cerberus = "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"
    Valles = "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"
    Schiaparelli = "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"
    Syrtis = "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": Valles},
        {"title": "Cerberus Hemisphere", "img_url": Cerberus},
        {"title": "Schiaparelli Hemisphere", "img_url": Schiaparelli},
        {"title": "Syrtis Major Hemisphere", "img_url": Syrtis},
    ]

    mars_data["hemisphere images"] = hemisphere_image_urls

    # Return the dictionary
    return mars_data