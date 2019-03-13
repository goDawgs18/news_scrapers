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


# In[ ]:


#need webdriver to open the news sites
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# In[ ]:


#this is the rss feed for bbc news and gets all the latest articles
url = "https://www.foxnews.com/about/rss/"
browser = webdriver.Chrome()
browser.get(url)
time.sleep(1)


# In[ ]:


#This is now fox specific but fills a list with content
headers = browser.find_elements_by_xpath("//ul/li/h2/a")
dates = browser.find_elements_by_xpath("//ul[@id='feed-content']/li/p[@class='date']")

list = []
for index, header in enumerate(headers):
    print(header.text)
    curr_dict = {}
    curr_dict['Title'] = header.text
    curr_dict['URL'] = header.get_attribute('href')
    curr_dict['Date'] = dates[index].text
    list.append(curr_dict)
browser.quit()
list


# In[ ]:


#now time to put list into the database 

#Also need this to convert the date strings
from datetime import datetime
source = 'Fox'
for el in list:
    date = el['Date'].split(" ")
    date_final = date[0] + ' ' + date[1] + ' ' + date[2]
    cur_datetime_object = datetime.strptime(date_final, '%B %d, %Y')
    try:
        cur.execute("INSERT INTO Articles (Source, Title, URL, date) VALUES " +
               "(%s, %s, %s, %s)", (source, el['Title'], el['URL'], cur_datetime_object))
    except:
        print("already contains article: " + el['Title'])

cnx.commit()


# In[ ]:


#lets read it!
with cnx.cursor() as cursor:
    cursor.execute("SELECT * from Articles")
    print(cursor.fetchall())


# In[ ]:




