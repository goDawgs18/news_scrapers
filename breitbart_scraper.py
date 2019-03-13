#if you like this give me job offers haha
#I am not taking responsiblity for constantly updating this 
from selenium import webdriver
import csv
import time
import pymysql

#webdriver: selenium webdriver, Did this so it can be reused
    #can create with webdriver.Chrome()
#csv_format: boolean, if true then will output the results into a csv file
    #if csv_format is false then need to pass user and root for database
#username: String, username for database connection, default:"root"
#password: String, password for database connection, default: ""
#database: String, name of the database, default: "text"

def scrape(webdriver, csv_format, username="root", password="", db="text"):
    #this is the rss feed for cnn news and gets all the latest articles
    source = 'Breitbart'
    url = "https://www.breitbart.com/news/source/breitbart-news/"
    webdriver.get(url)
    
    headers = webdriver.find_elements_by_xpath("//div[@class='articles-list']/article/div/h2/a")
    dates = webdriver.find_elements_by_xpath("//div[@class='articles-list']/article/div/footer[2]")

    stories = []
    for index, header in enumerate(headers):
        curr_dict = {}
        curr_dict['source'] = source
        curr_dict['title'] = header.text
        curr_dict['url'] = header.get_attribute('href')
        curr_dict['date'] = dates[index].text
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
                                        #10 Feb 2019, 7:22 PM PST
            cur_datetime_object = datetime.strptime(el['date'], '%d %b %Y, %I:%M %p %Z')
            try:
                cur.execute("INSERT INTO Articles (source, title, url, date) VALUES " +
                       "(%s, %s, %s, %s)", (source, el['title'], el['url'], cur_datetime_object))
            except:
                print("already contains article: " + el['title'])

        cnx.commit()
