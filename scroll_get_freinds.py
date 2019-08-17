'''
Created on  15/08/2018

@author: hamdi elhamdi
'''

import json
import pandas as pd
from time import gmtime, strftime
from selenium import webdriver


with open('config.json') as file:
    config = json.load(file)


def standalone_friends_getter():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    # to open chrome webbrowser and maximize the window
    driver = webdriver.Chrome(executable_path="chromedriver.exe",
                              chrome_options=options)
    # connect to the specific ip address
    driver.get("https://www.facebook.com")

    # Login to Facebook
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys(config['email'])
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys(config['password'])
    driver.find_element_by_id("loginbutton").click()

    # Click on Profile Name
    driver.find_element_by_xpath("//a[@title='Profil']").click()

    # Click on 'Friends' option
    import time
    time.sleep(5)
    driver.find_element_by_xpath("//a[@data-tab-key='friends']").click()

    listProfileName = []

    # Flag to check the visibility of 'Films' Section (this section's placing is just after the friend list)
    movieSection = False

    # Loop to check the 'Films' Section  in each iteration
    while movieSection == False:
        try:
            # Taking the element of 'Films' Section
            movieElem = driver.find_element_by_xpath("//a[text()='Films']")
            print(movieElem.text)

            # Check the element of 'Films' Section
            if movieElem.text == "Films":
                movieSection = True
                break
        except Exception:
            # Get the list of all friends
            profilePicList = driver.find_elements_by_xpath("//div[@data-testid='friend_list_item']/a")
            for profilePic in profilePicList:
                # Get the profile URL of friend in each iteration of the loop by using 'href' attribute
                profileURL = profilePic.get_attribute("href")

                if profileURL.find('profile.php?id=') == -1:
                    finalProfileName = profileURL[profileURL.index('.com/') + len('.com/'):profileURL.index('?')]
                else:
                    finalProfileName = profileURL[
                                       profileURL.index('profile.php?id=') + len('profile.php?id='):profileURL.index(
                                           '&')]

                # Append the list by the profile name
                listProfileName.append({'profile_name': finalProfileName, 'url_profile': profileURL})
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    filteredFriendSet = listProfileName

    df = pd.DataFrame(filteredFriendSet)
    df = df.drop_duplicates(subset='profile_name', keep='first')
    save2csv(df)
    # To close the browser
    driver.quit()
    return 'ok'

def save2csv(df: pd.DataFrame):
    path = 'users_id_url_profile_db'
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for i in ['-', ' ', ':']:
        timenow = timenow.replace(i, '_')

    file_name = "{0}/{1}.csv".format(path, timenow)
    df.to_csv(file_name)


