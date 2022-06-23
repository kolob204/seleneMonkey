import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()


def add_browser_option(option):
    chrome_options.add_argument(option)


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)


def open_url(url):
    driver.get(url)


def get_driver():
    return driver;


def close_driver():
    driver.quit()
    os.system("taskkill /im chromedriver.exe")