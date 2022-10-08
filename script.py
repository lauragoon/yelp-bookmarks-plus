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

    global BOOKMARK_CONTAINER
    BOOKMARK_CONTAINER = COLLECTION_INFO.find_element(By.CLASS_NAME, "js-content-list")

    global COLLECTION_AMT
    COLLECTION_AMT = int(BOOKMARK_CONTAINER.get_attribute("data-item-count"))

    print(COLLECTION_AMT)

# Connect with webpage
def connect_site(collections_url):

    # support 3 browsers
    driver = None

    try:
        s = Service(r'geckodriver.exe')
        firefox_opts = Options()
        firefox_opts.add_argument('--headless')
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

    gen_site_globals()

# Run helper functions in order
def run_script():

    yelp_url = input("URL to Yelp bookmark collection: ")
    connect_site(yelp_url)

    time.sleep(0.5) # delay so don't start typing before site loads



run_script()