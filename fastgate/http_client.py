import time

import requests

from fastgate.utils import random_string


class FastGateHTTPClient(object):
    def __init__(self, host="192.168.1.254", port=80):
        self.host = host
        self.port = port
        self.seed = "{}pytester{}".format(int(time.time()), random_string(12))
        self.session_key = "NULL"
        self.base_url = "/status.cgi"
        self.base_params = lambda: {
            "_": self.seed,
            "sessionKey": self.session_key
        }
        self.headers = {"X-XSRF-TOKEN": "ciao", "DNT": "1"}
        self.cookies = {"XSRF-TOKEN": "ciao"}

    def request(self, method, params={}, cookies={}, headers={}, **kwargs):
        _params = self.base_params()
        _params.update(params)
        _cookies = self.cookies.copy()
        _cookies.update(cookies)
        _headers = self.headers.copy()
        _headers.update(headers)

        url = "http://{host}:{port}{path}".format(host=self.host, port=self.port, path=self.base_url)

        return requests.request(method, url, params=_params, headers=_headers, cookies=_cookies, **kwargs)

    def get(self, *a, **kw):
        return self.request("GET", *a, **kw)

    def post(self, *a, **kw):
        return self.request("POST", *a, **kw)

    def login(self, user, passwd):
        params = {
            "cmd": "3",
            "nvget": "login_confirm",
            "username": user,
            "password": passwd
        }

        return self.get(params=params)

    def check_login(self, user, passwd):
        r = self.login(user, passwd)
        self.session_key = r.json()["login_confirm"]["check_session"]

        r = self.get(params={
            "cmd": "4",
            "nvget": "login_confirm"
        })

        return str(r.json()["login_confirm"]["login_status"]) == "1"
