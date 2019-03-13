#if you like this give me job offers haha
#I am not taking responsiblity for constantly updating this 
import pymysql
import csv
from selenium import webdriver
import time
from datetime import datetime

#webdriver: selenium webdriver, Did this so it can be reused
    #can create with webdriver.Chrome()
#csv_format: boolean, if true then will output the results into a csv file
    #if csv_format is false then need to pass user and root for database
#username: String, username for database connection, default:"root"
#password: String, password for database connection, default: ""
#database: String, name of the database, default: "text"
def scrape(webdriver, csv_format, username="root", password="", db="text"):
    source = 'CNN'
    url = "http://rss.cnn.com/rss/cnn_latest.rss"
    webdriver.get(url)
    headers = webdriver.find_elements_by_xpath("//ul/li/h4/a")
    dates = webdriver.find_elements_by_xpath("//ul/li/h5")
    blurbs = webdriver.find_elements_by_xpath("//ul/li/div")
    
    stories = []
    for index, header in enumerate(headers):
        print(dates[index].text[7:])
        curr_dict = {}
        curr_dict['title'] = header.text
        curr_dict['url'] = header.get_attribute('href')
        curr_dict['date'] = dates[index].text[7:]
        curr_dict['blurb'] = blurbs[index].text
        stories.append(curr_dict)
    stories

    if csv_format:
            timeStr = time.strftime("%H:%M_%d-%m-%Y")
            fname = "data/" + source + "_" + timeStr + ".csv"

            with open(fname, 'w') as csvfile:
                fieldnames = ['source', 'title', 'blurb', 'date','url']
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writeheader()
                writer.writerows(stories)

    else:
        cnx = pymysql.connect(host='localhost',
                                port=3306,
                                user=username,
                                password=password,
                                db=db)
        cur = cnx.cursor()
        for el in list:
            cur_datetime_object = datetime.strptime(el['date'], '%a, %d %b %Y %H:%M:%S %Z')
            try:
                cur.execute("INSERT INTO Articles (Source, Title, URL, date) VALUES " +
                       "(%s, %s, %s, %s)", (source, el['title'], el['url'], cur_datetime_object))
            except:
                print("already contains article: " + el['title'])

        cnx.commit()
