from selenium import webdriver
import bbc_scraper as bbc

driver = webdriver.Chrome()

#By putting true the results will go into a csv files in a dirctory called data
bbc.scrape(driver, True)
driver.quit()
