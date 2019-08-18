# IMPORTS
from time import strftime, gmtime

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

from login import create_logged_driver

requests.packages.urllib3.disable_warnings()
with open('config.json') as f:
    config = json.load(f)

# CONSTRAINTS
EMAIL = config['email']
PASSW = config['password']
LOGIN_URL = "https://www.facebook.com/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2F&amp;refid=8"
FACEBOOK_URL = "http://www.facebook.com"

# VARS
s = None


# MAIN CLASS
def getuserintro(url, user_id):
    dict_info = dict()
    driver = create_logged_driver()

    driver.get(url)

    """subscriber"""
    driver.get(url)
    sub = driver.page_source
    code_sub = BeautifulSoup(sub, 'lxml').find('div',{'id':'intro_container_id'})
    try :
        subscriber = code_sub.find_all('a')
        for i in subscriber:
            if ' personnes' in i.text:
                suivipar = i.text
                dict_info.update({'suivipar': suivipar})
    except:print('no subscribers found !!')
    """overview"""
    driver.get('%s/about?section=overview' % url)
    overview = driver.page_source
    soup = BeautifulSoup(overview, 'lxml')

    for i in soup.find_all('li'):
        try:
            place_etude = i.find('div', {'data-overviewsection': 'education'}).find('a', {'class': 'profileLink'}).text
            dict_info.update({'place_etude': place_etude})
        except:
            place_etude = None

        try:
            habite_a = i.find('div', {'data-overviewsection': 'places'}).find('a',
                                                                              {'class': 'profileLink'}).text
            dict_info.update({'habite_a': habite_a})
        except:
            habite_a = None

    """contact - info"""
    driver.get('%s/about?section=contact-info' % url)
    contact = driver.page_source
    soup = BeautifulSoup(contact, 'lxml')

    for i in soup.find_all('li'):
        try:
            tel = i.find('span', {'dir': 'ltr'}).text
            dict_info.update({'tel': tel})
        except:
            tel = None
    try:
        sexe = soup.find('li', {'class': '_3pw9 _2pi4 _2ge8 _3ms8'}).find('span', {'class': '_2iem'}).text

        dict_info.update({'sexe': sexe})
    except:
        sexe = None
    try:
        birth_day = soup.find('li', {'class': '_3pw9 _2pi4 _2ge8 _4vs2'}).find('span', {'class': '_2iem'}).text

        dict_info.update({'birth_day': birth_day})
    except:
        birth_day = None
    dict_info.update({'user_id': user_id})

    dict_info = check_dict(dict_info)
    print(dict_info)
    return dict_info

def check_dict(dict_):
    for k in ['birth_day','sexe','tel','habite_a','place_etude','suivipar']:
        if k not in dict_:
            dict_[k]='undefined'
    return dict_

def save2csv(df: pd.DataFrame, user_id: str):
    path = 'users_posts_db'
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for i in ['-', ' ', ':']:
        timenow = timenow.replace(i, '_')

    file_name = "{0}/{1}_{2}.csv".format(path, timenow, user_id)
    df.to_csv(file_name)

def create_userinfodb():
    data = pd.read_csv('users_id_url_profile_db/2019_08_18_22_29_25.csv')
    lister= list()
    for i in list(range(data.shape[0])):
        url = 'https://www.facebook.com/'+data.at[i,'profile_name']
        user_info = getuserintro(url, data.at[i,'profile_name'])
        lister.append(user_info)
    df = pd.DataFrame(lister)
    df.to_csv('user_intro.csv')


create_userinfodb()
