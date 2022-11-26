from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
PROXY = "8.219.97.248:80" # IP:PORT or HOST:PORT

chromedriver = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('--proxy-server=http://%s' % PROXY)# для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, options=options)
# gives an implicit wait for 20 seconds
browser.get('https://www.wine-searcher.com/sign-in?pro_redirect_url_F=%2F')
time.sleep(2)
email = browser.find_element("id", 'loginmodel-username')
password = browser.find_element("id", 'loginmodel-password')
login = browser.find_element("id", "pv_submit_F")

email.send_keys('st087048@student.spbu.ru')
password.send_keys('Ta2002nya')
login.click()
browser.get('https://www.wine-searcher.com/find/monte+vertine+le+pergole+torte+tuscany+igp+italy/1/italy')
requiredHtml = browser.page_source
print(requiredHtml)