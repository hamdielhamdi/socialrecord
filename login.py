from selenium import webdriver
import json

with open('config.json') as file:
    config = json.load(file)

def create_logged_driver():
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
    return driver