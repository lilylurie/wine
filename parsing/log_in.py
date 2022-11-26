import requests

url = 'https://www.wine-searcher.com/sign-in?pro_redirect_url_F=%2F'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
data = {
    '_csrf': 'ggMjHtNI_1EkfhreUVs_LHOPwYeRRYT15YV8bq9_B63DVXInlAe9PVwrQIgOLg4BIPWiytN1vZK8xE0M4U1jmw==',
    'register_gift_yn_F': '',
    'LoginModel[username]': 'st087048@student.spbu.ru',
    'LoginModel[password]': 'Ta2002nya',
    'LoginModel[rememberMe]': '0',
    'LoginModel[rememberMe]': '1',
    'login-button': '',
}
session = requests.Session()
session.headers.update(headers)
response = session.post(url, data=data)
print(response.status_code)