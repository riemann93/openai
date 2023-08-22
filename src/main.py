from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
EMAIL = config['LOGIN']['email']
PASSWORD = config['LOGIN']['password']

selectors = configparser.ConfigParser()
selectors.read('selectors.ini')


def click_element(browser, css_selector, delay=2):
    browser.find_element(By.CSS_SELECTOR, css_selector).click()
    time.sleep(delay)


def input_text(browser, css_selector, text, delay=2):
    browser.find_element(By.CSS_SELECTOR, css_selector).send_keys(text)
    time.sleep(delay)


def automate_openai_login():
    browser = webdriver.Chrome()
    browser.get('https://chat.openai.com')
    time.sleep(3)

    click_element(browser, selectors['LOGIN']['button'])
    input_text(browser, selectors['EMAIL']['input'], EMAIL)
    click_element(browser, selectors['EMAIL']['continue_button'])

    input_text(browser, selectors['PASSWORD']['input'], PASSWORD)
    click_element(browser, selectors['PASSWORD']['continue_button'])
    click_element(browser, selectors['POPUP']['dismiss'])

    input_text(browser, selectors['CHAT']['input'], "What cultural meaning does the number 42 have?")
    browser.find_element(By.CSS_SELECTOR, selectors['CHAT']['input']).send_keys(Keys.RETURN)
    time.sleep(5)

    try:
        response_element = browser.find_element(By.CSS_SELECTOR, selectors['CHAT']['response'])
        response_text = response_element.text
        print(f"OpenAI's Response: {response_text}")
    except Exception as e:
        print(f"Error while fetching response: {e}")

    input_text(browser, selectors['CHAT']['input'], "What cultural meaning does the number 41 have?")
    browser.find_element(By.CSS_SELECTOR, selectors['CHAT']['input']).send_keys(Keys.RETURN)
    time.sleep(5)

    try:
        response_element = browser.find_element(By.CSS_SELECTOR, selectors['CHAT']['response'])
        response_text = response_element.text
        print(f"OpenAI's Response: {response_text}")
    except Exception as e:
        print(f"Error while fetching response: {e}")

if __name__ == "__main__":
    automate_openai_login()