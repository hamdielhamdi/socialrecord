# coding: utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import json
import string


""" will be structured in utils.py file """
def RepresentsIntL(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def RepresentIntC(s):
    try :
        int(s.split(' ')[0])
        return True
    except:
        return False

selfProfile = "https://mbasic.facebook.com/profile.php?fref=pb"


def mfacebookToBasic(url):
    """Reformat a url to load mbasic facebook instead of regular facebook, return the same string if
    the url don't contains facebook"""

    if "m.facebook.com" in url:
        return url.replace("m.facebook.com", "mbasic.facebook.com")
    elif "www.facebook.com" in url:
        return url.replace("www.facebook.com", "mbasic.facebook.com")
    else:
        return url



dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)


class FacebookBot(webdriver.PhantomJS):
    """Main class for browsing facebook"""

    def __init__(self):

        webdriver.PhantomJS.__init__(self, desired_capabilities=dcap)

    def get(self, url):
        """The make the driver go to the url but reformat the url if is for facebook page"""
        super().get(mfacebookToBasic(url))
        self.save_screenshot("Debug.png")

    def login(self, email, password):
        """Log to facebook using email (str) and password (str)"""

        url = "https://mbasic.facebook.com"
        self.get(url)
        email_element = self.find_element_by_name("email")
        email_element.send_keys(email)
        pass_element = self.find_element_by_name("pass")
        pass_element.send_keys(password)
        pass_element.send_keys(Keys.ENTER)

        try :
                self.find_element_by_class_name("bp").click()
                self.get(url)
        except:
            pass

        print("Logged in")
        return True

    def getPostInProfile(self,profileURL):

        self.get(profileURL)
        for level in [0, 1,2]:
            for i in list(string.ascii_lowercase):
                try:
                    p = self.find_element_by_id("u_0_" + str(i))
                    post = (p.find_elements_by_tag_name("span"))

                    post_content = post[1].text

                    if post_content == "·":
                        image = True
                    else:
                        image = False
                    date = p.find_element_by_tag_name("abbr").text

                    reaction_content = p.find_elements_by_tag_name("a")
                    nbr_like = 0
                    for item in reaction_content:
                        if RepresentsIntL(item.text):
                            nbr_like = int(item.text)
                    nbr_comment = 0
                    link_to_comment_content = 0
                    for item in reaction_content:
                        if RepresentIntC(item.text):
                            nbr_comment = int((item.text).split(' ')[0])
                            # TODO : get comment content from this link
                            link_to_comment_content = item.get_attribute('href')

                    #  TODO : scroll down
                    a = self.find_elements_by_tag_name("a")
                    for link in a:
                        if link.text == "Afficher plus d’actualités":
                            link_to_the_next_page = link.get_attribute("href")
                    print(post_content, image, date, nbr_like, nbr_comment)
                except:
                    pass
            print(link_to_the_next_page)

            self.get(link_to_the_next_page)




