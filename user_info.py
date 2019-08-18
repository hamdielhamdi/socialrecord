# IMPORTS
import requests
import time
from bs4 import BeautifulSoup, Comment
import json
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
class facebook():
    def __init__(self,user_id):
        self.s = requests.session()
        self.login(user_id)

    def login(self,user_id):
        dict_info = dict()
        # GET DEFAULT VALUES FROM PAGE
        global habite_a, place_etude
        r = self.s.get(FACEBOOK_URL, verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        # GET DEFAULT VALUES
        tmp = soup.find(attrs={"name": "lsd"})
        lsd = tmp["value"]
        data = {'lsd': lsd}
        data['email'] = EMAIL
        data['pass'] = PASSW
        data['login'] = 'Log In'

        r = self.s.post(LOGIN_URL, data=data, verify=False)
        print(r.status_code)

        """subscriber"""
        sub = self.s.get('https://www.facebook.com/%s' % user_id, cookies=r.cookies,
                              verify=False)
        soup = BeautifulSoup(sub.text, 'lxml')
        print(soup)
        # """overview"""
        # overview = self.s.get('https://www.facebook.com/%s/about?section=overview'%user_id, cookies=r.cookies,
        #                   verify=False)
        # soup = BeautifulSoup(overview.text, 'lxml')
        # # print(soup)
        #
        # comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        #
        # for c in comments:
        #         for i in BeautifulSoup(c, 'lxml').find_all('li'):
        #             try :
        #                 place_etude = i.find('div',{'data-overviewsection':'education'}).find('a',{'class':'profileLink'}).text
        #                 dict_info.update({'place_etude':place_etude})
        #             except:
        #                   place_etude = None
        #
        #             try :
        #                 habite_a = i.find('div', {'data-overviewsection': 'places'}).find('a',
        #                                                                                  {'class': 'profileLink'}).text
        #                 dict_info.update({'habite_a': habite_a})
        #             except:habite_a = None
        #
        #
        # """contact - info"""
        # overview = self.s.get('https://www.facebook.com/%s/about?section=contact-info'%user_id, cookies=r.cookies,
        #                       verify=False)
        # soup = BeautifulSoup(overview.text, 'lxml')
        # # print(soup)
        #
        # comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        #
        # for c in comments:
        #     for i in BeautifulSoup(c, 'lxml').find_all('li'):
        #         try:
        #             tel = i.find('span', {'dir': 'ltr'}).text
        #             dict_info.update({'tel': tel})
        #         except:
        #             tel = None
        #     try :
        #         sexe = BeautifulSoup(c, 'lxml').find('li',{'class':'_3pw9 _2pi4 _2ge8 _3ms8'}).find('span',{'class':'_2iem'}).text
        #
        #         dict_info.update({'sexe': sexe})
        #     except:
        #         sexe = None
        #     try :
        #         birth_day = BeautifulSoup(c, 'lxml').find('li',{'class':'_3pw9 _2pi4 _2ge8 _4vs2'}).find('span',{'class':'_2iem'}).text
        #
        #         dict_info.update({'birth_day': birth_day})
        #     except:
        #         birth_day = None
        # dict_info.update({'user_id':user_id})
        # return dict_info
        #


import pandas as pd
df = pd.read_csv('users_id_url_profile_db/2019_08_17_14_20_30.csv')
for i in list(range(df.shape[0])):
    data = facebook(df.at[i,'profile_name'])
