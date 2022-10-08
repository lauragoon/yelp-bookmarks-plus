import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time

# import sys
# sys.path.append('../')

# Keep track of global variables used to interact with webpage
def gen_site_globals():

    global COLLECTION_INFO
    COLLECTION_INFO = DRIVER.find_element(By.CLASS_NAME, "collection-left-pane")

    global COLLECTION_TITLE
    COLLECTION_TITLE = COLLECTION_INFO.find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "h1").get_attribute("innerHTML")

    global BOOKMARK_AMT
    BOOKMARK_AMT = int(COLLECTION_INFO.find_element(By.CLASS_NAME, "js-content-list").get_attribute("data-item-count"))


def get_bookmarks():
    temp_bookmarks = COLLECTION_INFO.find_elements(By.CLASS_NAME, "collection-item")
    last_bookmark = None

    while (last_bookmark is None or last_bookmark != temp_bookmarks[-1]):
        last_bookmark = temp_bookmarks[-1]
        DRIVER.execute_script("arguments[0].scrollIntoView();", temp_bookmarks[-1])
        time.sleep(0.9)
        temp_bookmarks = COLLECTION_INFO.find_elements(By.CLASS_NAME, "collection-item")

    global BOOKMARKS
    BOOKMARKS = COLLECTION_INFO.find_elements(By.CLASS_NAME, "collection-item")


def process_bookmarks():
    pass


# Connect with webpage
def connect_site(collections_url):

    # support 2 browsers
    driver = None

    try:
        s = Service(r'geckodriver.exe')
        firefox_opts = Options()
        # firefox_opts.add_argument('--headless')
        driver = webdriver.Firefox(service=s, options=firefox_opts)
    except SessionNotCreatedException:
        try:
            chromedriver_autoinstaller.install()
            chrome_opts = webdriver.ChromeOptions()
            chrome_opts.add_argument('headless')
            chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=chrome_opts)
        except SessionNotCreatedException: 
            raise NotImplementedError("This script currently supports only Firefox and Chrome.")

    driver.get(collections_url)

    global DRIVER
    DRIVER = driver


# Run helper functions in order
def run_script():

    yelp_url = input("URL to Yelp bookmark collection: ")
    connect_site(yelp_url)

    time.sleep(0.5) # delay so don't start typing before site loads

    gen_site_globals()
    get_bookmarks()


run_script()