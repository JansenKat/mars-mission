
import pandas as pd
import requests as r
from bs4 import BeautifulSoup
from selenium import webdriver

#Urls as variables 
#Some are broken into 2 pieces so the base can be used later.
nasa_url = "https://mars.nasa.gov/news/"
jpl_base = "https://www.jpl.nasa.gov"
jpl_search = jpl_base+"/spaceimages/?search=&category=Mars"
twitter_url = "https://twitter.com/marswxreport?lang=en"
facts_url = "http://space-facts.com/mars/"
astro_base = 'https://astrogeology.usgs.gov'
astro_url = astro_base+"/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

#Selenium driver to get soups
driver = webdriver.Firefox()
driver.get(nasa_url)
driver.implicitly_wait(10)
nasa_soup = BeautifulSoup(driver.page_source,"lxml")

driver.get(facts_url)
driver.implicitly_wait(10)
facts_soup = BeautifulSoup(driver.page_source,"lxml")

driver.get(astro_url)
driver.implicitly_wait(10)
astro_soup = BeautifulSoup(driver.page_source,"lxml")

#Requests to get remaining soups
jpl_r = r.get(jpl_search).text
jpl_soup = BeautifulSoup(jpl_r,'lxml')

twitter_r = r.get(twitter_url).text
twitter_soup = BeautifulSoup(twitter_r,'lxml')


##Search through soups to find text

#Nasa Mars Latest Article title and teaser
news_title = nasa_soup.body.find('div',class_='content_title').text
news_p = nasa_soup.body.find('div',class_='article_teaser_body').text

# Featured Image from JPL
featured_image_url = jpl_base+jpl_soup.body.find('article')['style'].split(' ')[1].strip('url').strip(";(')")

#Twitter
mars_weather = twitter_soup.body.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

#Mars Facts Table
facts_df = pd.read_html(str(facts_soup.body.find('table',id='tablepress-p-mars-no-2')))[0]
facts_df.columns = ['description','value']
facts_df = facts_df.set_index('description')


#Astropedia
#Find Title and url to hemisphere pages.
astro_h = astro_soup.find_all('h3')
astro_d = [{'title':h.text,'url':astro_base+h.parent['href']} for h in astro_h]

#Visit each url found above and add the img_url to the appropriate dictionary.
for h in astro_d:
    driver.get(h['url'])
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source,"lxml")
    img = soup.find('a',target='_blank')
    h.update({'img_url':img['href']})

#Close the Selenium Webdriver
driver.close()