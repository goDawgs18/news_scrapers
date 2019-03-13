#!/usr/bin/env python
# coding: utf-8

# In[1]:


#set up connection to database
import pymysql

cnx = pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='',
                                db='text')
cur = cnx.cursor()


# In[2]:


#need webdriver to open the news sites
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# In[3]:


#this is the rss feed for bbc news and gets all the latest articles
url = "https://www.npr.org/sections/news/"
browser = webdriver.Chrome()
browser.get(url)
time.sleep(1)


# In[4]:


#This is now npr specific but fills a list with content
headers = browser.find_elements_by_xpath("//div[@class='item-info']/h2/a")
section = browser.find_elements_by_xpath("//div[@class='item-info']/div/h3/a")
dates = browser.find_elements_by_xpath("//div[@class='item-info']/p/a/time")

list = []
for index, header in enumerate(headers):
    curr_dict = {}
    curr_dict['title'] = header.text
    curr_dict['url'] = header.get_attribute('href')
    curr_dict['date'] = dates[index].get_attribute('datetime')
    curr_dict['section'] = section[index].text
    list.append(curr_dict)
browser.quit()
list


# In[5]:


#now time to put list into the database 

#Also need this to convert the date strings
from datetime import datetime
source = 'NPR'
for el in list:
    #datetime="2019-02-08"
    cur_datetime_object = datetime.strptime(el['date'], '%Y-%m-%d')
    try:
        cur.execute("INSERT INTO Articles (source, title, category, url, date) VALUES " +
               "(%s, %s, %s, %s, %s)", (source, el['title'], el['section'], el['url'], cur_datetime_object))
    except:
        print("already contains article: " + el['title'])

cnx.commit()


# In[6]:


#lets read it!
with cnx.cursor() as cursor:
    cursor.execute("SELECT * from Articles")
    print(cursor.fetchall())


# In[ ]:




