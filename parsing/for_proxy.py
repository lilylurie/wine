import requests_html
from bs4 import BeautifulSoup
import pickle
import requests
# from grab import Grab



def scrap_proxy():
    global px_list
    px_list = set()

    session = requests_html.HTMLSession()
    r = session.get('https://free-proxy-list.net/')
    r.html.render()
    for i in range(1, 21):

        add=r.html.xpath('/html/body/section[1]/div/div[2]/div/table/tbody/tr[{}]/td[1]/text()'.format(i))[0]
        port=r.html.xpath('/html/body/section[1]/div/div[2]/div/table/tbody/tr[{}]/td[2]/text()'.format(i))[0]
        px_list.add(':'.join([add, port]))

    print("---New proxy scraped, left: " + str(len(px_list)))
    with open('proxis.pickle', 'wb') as f:
        pickle.dump(px_list, f)
    print(px_list)
    return px_list
#"https": "https://" + px,
def check_proxy(px):
    try:
        requests.get("https://www.wine-searcher.com/", proxies = {"https": "http://" + px}, timeout = 3)
    except Exception as x:
        print('--'+px + ' is dead: '+ x.__class__.__name__)
        return False
    return True

# def check_my_proxy(px):
#     try:
#         g.setup(proxy=px)
#         g.go('http://avito.ru')
#         # g.go('https://www.wine-searcher.com/')
#     except Exception as x:
#         print('--'+px + ' is dead: '+ x.__class__.__name__)
#         return False
#     return True

def get_proxy(scrap = False):
    global px_list
    if scrap or len(px_list) < 6:
            px_list = scrap_proxy()
    while True:
        if len(px_list) < 6:
            px_list = scrap_proxy()
        px = px_list.pop()
        if check_proxy(px):
            break
    print('-'+px+' is alive. ({} left)'.format(str(len(px_list))))
    with open('proxis.pickle', 'wb') as f:
            pickle.dump(px_list, f)
    return px
px_list = []
# g = Grab()
print(get_proxy())
# g.setup(proxy='66.29.154.103:3128')
# g.go('http://avito.ru')