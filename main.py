"""
File where definition of main class is hidden
"""
import requests
import time
import random

from userinfo import UserInfo


class ShrewdBot:
    user_login = "test_login"
    user_password = "test_password"
    user_id = 0

    url = 'https://www.instagram.com/'
    url_login = "https://www.instagram.com/accounts/login/ajax/"

    session = requests.Session()

    # TBD: user_agent should be changed

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")

    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    def __init__(self, login, password):
        self.user_login = login
        self.user_password = password

        self.user_login = input("Enter your username: ")
        self.user_password = input("Enter your password: ")

        self.login()

    def login(self):
        print("Trying to login as", self.user_login)
        self.session.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                                     'ig_vw': '1920', 'csrftoken': '',
                                     's_network': '', 'ds_user_id': ''})
        self.login_post = {'username': self.user_login,
                           'password': self.user_password}
        self.session.headers.update({'Accept-Encoding': 'gzip, deflate',
                                     'Accept-Language': self.accept_language,
                                     'Connection': 'keep-alive',
                                     'Content-Length': '0',
                                     'Host': 'www.instagram.com',
                                     'Origin': 'https://www.instagram.com',
                                     'Referer': 'https://www.instagram.com/',
                                     'User-Agent': self.user_agent,
                                     'X-Instagram-AJAX': '1',
                                     'X-Requested-With': 'XMLHttpRequest'})
        r = self.session.get(self.url)
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.session.post(self.url_login, data=self.login_post,
                                  allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.session.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                ui = UserInfo()
                self.user_id = ui.get_user_id_by_login(self.user_login)
                self.login_status = True
                print("Login successful")
            else:
                self.login_status = False
                print("Login failed")
        else:
            print("Connection problems")

ShrewdBot(123, 123)