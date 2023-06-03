import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from user import User
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("-headless")

base_url = 'https://slippi.gg/user/'

def get_user_from_tag(tag):
    user = User(tag)

    driver = webdriver.Firefox(options=options)
    driver.get(base_url + user.uri_name)
    # print('Loading user ' + tag)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jss7"))
        )
    except:
        print('Wait Timed out')
    # finally:
        # print('User ' + tag + 'loaded')

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    player_summary = soup.find('div', class_='jss7')

    p_tags = player_summary.findChildren()

    user.name = p_tags[0].get_text()
    user.rank = p_tags[5].get_text()
    user.elo = p_tags[6].get_text().split()[0]


    return user