from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
PROXY = "125.21.3.41:8080" # IP:PORT or HOST:PORT


chromedriver = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('--proxy-server=http://%s' % PROXY)# для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, options=options)
browser.get("http://whatismyipaddress.com")
