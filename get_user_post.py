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


def get_posts_per_user_name(user_id: str, url: str):
    # TODO: add date selection

    driver = create_logged_driver()

    driver.get(url)
    # Flag to check the visibility of 'Films' Section (this section's placing is just after the friend list)
    index = 0
    while index < 200:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        index += 1
    data = driver.page_source

    soup = bs(data, 'lxml')
    a = soup.find_all('div', {'class': '_5pcr userContentWrapper'})
    user_post = list()
    for i in a:
        try:
            post_content = i.find('div', {'data-testid': 'post_message'}).text
        except Exception as e:
            post_content = None
        try:
            post_creation_date = i.find('div', {'data-testid': 'story-subtitle'}).find('abbr', {'class': '_5ptz'})[
                'title']
        except Exception as e:
            post_creation_date = None
        # TODO : fetch all comment in post if exist
        try:
            post_comments = i.find('div', {'data-testid': 'fbFeedStoryUFI/feedbackSummary'}).text
        except Exception as e:
            post_comments = 0

        """all possible likes type"""
        try:
            post_likes_wow = i.find('span', {'data-testid': 'UFI2TopReactions/tooltip_WOW'}).find('a')['aria-label']
        except Exception as e:
            post_likes_wow = 0
        try:
            post_likes_love = i.find('span', {'data-testid': 'UFI2TopReactions/tooltip_LOVE'}).find('a')['aria-label']
        except Exception as e:
            post_likes_love = 0
        try:
            post_likes_like = i.find('span', {'data-testid': 'UFI2TopReactions/tooltip_LIKE'}).find('a')['aria-label']
        except Exception as e:
            post_likes_like = 0
        try:
            post_likes_triste = i.find('span', {'data-testid': 'UFI2TopReactions/tooltip_SORRY'}).find('a')[
                'aria-label']
        except Exception as e:
            post_likes_triste = 0

        try:
            post_likes_anger = i.find('span', {'data-testid': 'UFI2TopReactions/tooltip_ANGER'}).find('a')['aria-label']
        except Exception as e:
            post_likes_anger = 0
        try:
            post_likes_haha = i.find('span', {'data-testid': 'UFI2TopReactions/tooltip_HAHA'}).find('a')['aria-label']
        except Exception as e:
            post_likes_haha = 0
        if post_content is not None:
            user_post.append({'post': post_content,
                              'date': post_creation_date,
                              'post_comment': post_comments,
                              'nrb_rct_like': post_likes_like,
                              'post_happy': post_likes_haha,
                              'post_anger': post_likes_anger,
                              'post_triste': post_likes_triste,
                              'post_love': post_likes_love,
                              'post_wow':post_likes_wow})
    print(user_id)

    df = pd.DataFrame(user_post)
    save2csv(df, user_id)
    driver.quit()


def save2csv(df: pd.DataFrame, user_id: str):
    path = 'users_posts_db'
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for i in ['-', ' ', ':']:
        timenow = timenow.replace(i, '_')

    file_name = "{0}/{1}_{2}.csv".format(path, timenow, user_id)
    df.to_csv(file_name)

