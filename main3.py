from selenium import webdriver
from bs4 import BeautifulSoup
import time
PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT

chromedriver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--proxy-server=http://%s' % PROXY)# для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
# gives an implicit wait for 20 seconds
browser.get('https://www.wine-searcher.com/sign-in?pro_redirect_url_F=%2F')
#time.sleep(5)
email = browser.find_element("id", 'loginmodel-username')
password = browser.find_element_by_name("id", 'loginmodel-password')
login = browser.find_element_by_name("id", "pv_submit_F")

email.send_keys('st087048@student.spbu.ru')
password.send_keys('Ta2002nya')
login.click()
browser.get('https://www.wine-searcher.com/find/monte+vertine+le+pergole+torte+tuscany+igp+italy/1/italy')
requiredHtml = browser.page_source
print(requiredHtml)