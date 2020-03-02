#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests as r
from bs4 import BeautifulSoup
from selenium import webdriver


# In[2]:


nasa_url = "https://mars.nasa.gov/news/"

jpl_base = "https://www.jpl.nasa.gov"
jpl_search = jpl_base+"/spaceimages/?search=&category=Mars"

twitter_url = "https://twitter.com/marswxreport?lang=en"

facts_url = "http://space-facts.com/mars/"

astro_base = 'https://astrogeology.usgs.gov'
astro_url = astro_base+"/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


# ## Here's the latest Mars Nasa News article

# In[3]:


driver = webdriver.Firefox()
driver.get(nasa_url)
driver.implicitly_wait(10)
nasa_soup = BeautifulSoup(driver.page_source,"lxml")
driver.close()


# In[4]:


news_title = nasa_soup.body.find('div',class_='content_title').text
news_p = nasa_soup.body.find('div',class_='article_teaser_body').text


# ## What about the Featured Image?

# In[5]:


jpl_r = r.get(jpl_search).text
jpl_soup = BeautifulSoup(jpl_r,'lxml')


# In[6]:


featured_image_url = jpl_base+jpl_soup.body.find('article')['style'].split(' ')[1].strip('url').strip(";(')")
featured_image_url


# ## Let's check twitter for the latest tweet from Mars Weather

# In[7]:


twitter_r = r.get(twitter_url).text
twitter_soup = BeautifulSoup(twitter_r,'lxml')
mars_weather = twitter_soup.body.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


# ## Now for some Mars Facts

# In[8]:


driver = webdriver.Firefox()
driver.get(facts_url)
driver.implicitly_wait(10)
facts_soup = BeautifulSoup(driver.page_source,"lxml")
driver.close()


# In[9]:


facts_df = pd.read_html(str(facts_soup.body.find('table',id='tablepress-p-mars-no-2')))[0]
facts_df.columns = ['description','value']
facts_df = facts_df.set_index('description')
(facts_df)


# ## Last, but not least, Astrogeology has some cool images we want to save.

# In[10]:


driver = webdriver.Firefox()
driver.get(astro_url)
driver.implicitly_wait(10)
astro_soup = BeautifulSoup(driver.page_source,"lxml")
driver.close()


# In[12]:


astro_h = astro_soup.find_all('h3')


# We don't have the links to each of the images, so let's go get them as well as their Titles.

# In[13]:


astro_d = [{'title':h.text,'url':astro_base+h.parent['href']} for h in astro_h]
astro_d


# Now we need to visit those links to find the image url.
# Since I've already got the urls to each of those pages, let's visit each and get what we need.

# In[14]:


driver = webdriver.Firefox()
for h in astro_d:
    driver.get(h['url'])
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source,"lxml")
    img = soup.find('a',target='_blank')
    h.update({'img_url':img['href']})
driver.close()
astro_d


# In[ ]:



