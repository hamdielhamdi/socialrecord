'''
Created on  17/08/2018

@author: hamdi elhamdi
'''

import json
import time
from time import gmtime, strftime
import pandas as pd


from bs4 import BeautifulSoup as bs
from login import create_logged_driver
with open('config.json') as file:
    config = json.load(file)

def getuserinfo(user_id,profile_url):
    #  id  : intro_container_id
    driver = create_logged_driver()
    driver.get(profile_url)
    driver.find_element_by_xpath("//a[@title='about']").click()
    driver.find_element_by_xpath("//a[@data-testid='nav_edu_work']").click()
    data = driver.page_source
    soup = bs(data, 'lxml')
    info = soup.find_all('div', {'id': 'pagelet_eduwork'})
    for i in info:
        print(i.text)



getuserinfo('smax90','https://www.facebook.com/smax90')