# -------------------------------------------
# web-scraping-challenge
#     by Diane Scherpereel      November 2019
# -------------------------------------------

# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import requests
from splinter import Browser

def scrape():   #using the commands below to scrape 5 different websites
    mars_dictionary = {}   # make a dictionary to store everything

    # --------------
    # Nasa Mars News
    # --------------

    # URL of Mars News page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Set up a chrome browser and visit the page
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(mars_news_url)

    # Retrieve page with the requests module
    nasa_response = requests.get(mars_news_url)
    # Create BeautifulSoup object and parse
    nasa_soup = BeautifulSoup(nasa_response.text, 'html.parser')


    # Find the title and save it to the variable "nasa_news_title"
    nasa_news_title_raw = nasa_soup.find(class_='content_title')
    nasa_news_title = nasa_news_title_raw.text.strip()

    # Find and save the paragraph to the variable "nasa_paragraph"
    nasa_paragraph_raw = nasa_soup.find(class_='rollover_description_inner')
    nasa_paragraph = nasa_paragraph_raw.text.strip()

    # Add both the title and the paragraph to the dictionary
    mars_dictionary['nasa_news_title'] = nasa_news_title
    mars_dictionary['nasa_paragraph'] = nasa_paragraph

    # ---------------------
    # JPL Mars Space Images
    # ---------------------

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Create BeautifulSoup object and parse
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'lxml')

    # Select the part that contains the image urls
    featured_image = jpl_soup.select('li.slide a.fancybox')

    # Make a list of just the data-fancybox-hrefs
    img_list = [i.get('data-fancybox-href') for i in featured_image]

    # Put just the base part of the webpage into a variable
    img_base_url = 'https://www.jpl.nasa.gov'

    # Combine the base url with the first img url from img_list
    featured_image_url = img_base_url + img_list[0] 

    # Add to the dictionary
    mars_dictionary['featured_image_url'] = featured_image_url

    # -------------
    # Mars Weather
    # -------------

    # URL of page to be scraped
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    mars_weather_response = requests.get(mars_weather_url)

    # Create BeautifulSoup object and parse, change mars_weather_response to text
    mars_weather_soup = BeautifulSoup(mars_weather_response.text, 'html.parser')

    # Find and save the latest tweet for Mars weather
    mars_weather_raw = mars_weather_soup.find(class_='TweetTextSize')
    mars_weather = mars_weather_raw.text.strip()

    # Add to the dictionary
    mars_dictionary['mars_weather'] = mars_weather

    # -------------
    # Mars Facts
    # -------------

    # Label the mars facts url
    mars_facts_url = 'https://space-facts.com/mars/'

    # Use pandas to read the mars facts table
    mars_facts_table = pd.read_html(mars_facts_url)

    # Put the table into a pandas dataframe
    mars_facts_db1 = mars_facts_table[0]

    # Set index to the 0 column
    mars_facts_db1.set_index(0, inplace=True)

    # Delete the index name ('0')
    mars_facts_db1.index.names = [None]

    # Delete the column name ('1')
    mars_facts_db1.columns = ['']

    # Convert the pandas dataframe to HTML table string
    mars_facts_html_table = mars_facts_db1.to_html()

    # Clean up the table by getting rid of these \n
    mars_facts_html_table = mars_facts_html_table.replace('\n', '')

    # Add to the dictionary
    mars_dictionary['mars_facts'] = mars_facts_html_table

    # ----------------
    # Mars Hemispheres
    # ----------------

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mars hemispheres
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    # Create BeautifulSoup object and parse
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Get the 4 hemispheres from div.item
    hemispheres = soup.select('div.item')

    # Loop through each hemisphere

    hemisphere_image_urls = []

    for h in hemispheres:
        title = (h.find('h3').text).replace(' Enhanced', '')
        
        # click the hemisphere
        browser.click_link_by_partial_text(title)
    
        # make new soup of that page
        soup = BeautifulSoup(browser.html, 'html.parser')
    
        # find the full image
        full = soup.find('a', text='Sample')
    
        # get the img url
        img_url = full['href']
    
        # make a dictionary and append to the list
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    
        # go back 
        browser.back()

    # close the browser
    browser.quit()    

    # Add to the dictionary
    mars_dictionary['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dictionary