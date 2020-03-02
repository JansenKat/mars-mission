
import pandas as pd
import requests
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

#Scrape provided website with selenium
#Return soup of page.
def s_scrape(url):
    driver = webdriver.Firefox()
    driver.get(nasa_url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    return soup

#Scrape provided website with requests
#Return soup of page.
def r_scrape(url):
    r = requests.get(jpl_search).text
    return BeautifulSoup(r,'lxml')

#Put everything into a single function to return a dictionary of everything.
def scrape():
    data = {}

    #Selenium driver to get soups
    nasa_soup = s_scrape(nasa_url)
    facts_soup = s_scrape(facts_url)
    astro_soup = s_scrape(astro_url)

    #Requests to get remaining soups
    jpl_soup = r_scrape(jpl_search)
    twitter_soup = r_scrape(twitter_url)


    ##Search through soups to find text
    ## add information to data dictionary.

    #Nasa Mars Latest Article title and teaser
    news_title = nasa_soup.body.find('div',class_='content_title').text
    news_p = nasa_soup.body.find('div',class_='article_teaser_body').text
    nasa_latest = {'title':news_title,'teaser':news_p}
    data['nasa']=nasa_latest

    # Featured Image from JPL
    featured_image_url = jpl_base+jpl_soup.body.find('article')['style'].split(' ')[1].strip('url').strip(";(')")
    data['featured_image'] = featured_image_url

    #Twitter
    mars_weather = twitter_soup.body.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    data['mars_weather'] = mars_weather

    #Mars Facts Table
    facts_df = pd.read_html(str(facts_soup.body.find('table',id='tablepress-p-mars-no-2')))[0]
    facts_df.columns = ['description','value']
    facts_df = facts_df.set_index('description').to_html()
    data['facts_table'] = facts_df

    #Astropedia
    #Find Title and url to hemisphere pages.
    astro_h = astro_soup.find_all('h3')
    astro_d = [{'title':h.text,'url':astro_base+h.parent['href']} for h in astro_h]

    #Visit each url found above and add the img_url to the appropriate dictionary.
    for h in astro_d:
        soup = s_scrape(h['url'])
        img = soup.find('a',target='_blank')
        h.update({'img_url':img['href']})
    data['hemispheres'] = astro_d

    return data

if __name__ == "__main__":
    scrape()