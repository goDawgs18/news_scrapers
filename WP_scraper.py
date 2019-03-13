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


#this is the rss feed for washington post news and gets all the latest articles
url = "http://feeds.washingtonpost.com/rss/national"
browser = webdriver.Chrome()
browser.get(url)
time.sleep(1)


# In[4]:


#This is now washington post specific but fills a list with content
headers = browser.find_elements_by_xpath("//div[@id='items']/div/h3/a")
dates = browser.find_elements_by_xpath("//div[@id='items']/div/div[@class='pubdate']")

list = []
for index, header in enumerate(headers):
    curr_dict = {}
    curr_dict['title'] = header.text
    curr_dict['url'] = header.get_attribute('href')
    curr_dict['date'] = dates[index].text[:-4]
    list.append(curr_dict)
browser.quit()
list


# In[5]:


#now time to put list into the database 

#Also need this to convert the date strings
from datetime import datetime
source = 'WashingtonPost'
for el in list:
    cur_datetime_object = datetime.strptime(el['date'], '%a, %d %b %Y %H:%M:%S')
    try:
        cur.execute("INSERT INTO Articles (Source, Title, URL, date) VALUES " +
               "(%s, %s, %s, %s)", (source, el['title'], el['url'], cur_datetime_object))
    except:
        print("already contains article: " + el['title'])

cnx.commit()


# In[6]:


# lets read it!
with cnx.cursor() as cursor:
    cursor.execute("SELECT * from Articles")
    print(cursor.fetchall())

