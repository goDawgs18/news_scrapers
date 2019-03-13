#if you like this give me job offers haha
#I am not taking responsiblity for constantly updating this 
from selenium import webdriver
import csv
import time

#for connection to mysql db
import pymysql

#webdriver: selenium webdriver, Did this so it can be reused
    #can create with webdriver.Chrome()
#csv_format: boolean, if true then will output the results into a csv file
    #if csv_format is false then need to pass user and root for database
#username: String, username for database connection, default:"root"
#password: String, password for database connection, default: ""
#database: String, name of the database, default: "text"

def scrape(webdriver, csv_format, username="root", password="", db="text"):
    url = "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"
    source = 'BBC'
    webdriver.get(url)
    headers = webdriver.find_elements_by_xpath("//ul/li/a")
    blurbs = webdriver.find_elements_by_xpath("//ul/li/div")
    
    all_stories = []
    for index, header in enumerate(headers):
        print(header.text)
        curr_dict = {}
        curr_dict['title'] = header.text
        curr_dict['url'] = header.get_attribute('href')
        curr_dict['source'] = source
        curr_dict['blurb'] = blurbs[index].text
        all_stories.append(curr_dict)
    all_stories
    
    if csv_format:
        timeStr = time.strftime("%H:%M_%d-%m-%Y")
        fname = "data/" + source + "_" + timeStr + ".csv"
        
        with open(fname, 'w') as csvfile:
            fieldnames = ['source', 'title', 'blurb', 'url']
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            writer.writerows(all_stories)
            
    else:
        cnx = pymysql.connect(host='localhost',
                                port=3306,
                                user=username,
                                password=password,
                                db=db)
        cur = cnx.cursor()
        try:
            cur.execute("INSERT INTO Articles (source, title, url) VALUES " +
                   "(%s, %s, %s)", (source, el['title'], el['url']))
        except:
            print("already contains article: " + el['title'])
        
        cnx.commit()

# In[5]:


#now time to put list into the database 

# for el in list:
    




# # In[7]:


# #lets read it!
# with cnx.cursor() as cursor:
#     cursor.execute("SELECT * from Articles")
#     print(cursor.fetchall())


# In[ ]:




