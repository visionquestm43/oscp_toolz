#!/usr/bin/env python3

import requests
from requests.exceptions import Timeout

proxies = {
    "http": "http://10.11.0.60:8080"
}

RHOSTS = '10.11.1.221'
startPort = 1131
endPort = 6000
badPorts = {3389, 5357, 5722, 9389}
portRange = range(startPort, endPort)
outputFile = '/root/oscplab/labtargets/dot221/dot221winrmreq.txt'
raw_data = 'hEkuywjd'

with open(outputFile, 'w') as output:
    output.write("Testing ip %s " % RHOSTS + "ports {} to {}:\n".format(startPort, endPort) + "********\n")

for port in portRange:
    if port not in badPorts:
        try:
            url = 'http://%s' % RHOSTS + ':{}'.format(port) + '/wsman'
            req = requests.post(url, data=raw_data, proxies=proxies, timeout=(1, 2))

            responseHeaders = req.headers

            if 'WWW-Authenticate' in responseHeaders:
                print(url, '\n{}: '.format(port), responseHeaders['WWW-Authenticate'])
                with open(outputFile, 'a') as output:
                    output.write("\n!!!!!!!!!!\n\n")
                    output.write(url + '\n{}: '.format(port) + responseHeaders['WWW-Authenticate'] + "\n\n!!!!!!!!!!\n\n")

        except Timeout:
            print("Request to TCP port {}".format(port) + " timed out.")

        if port % 100 == 0:
            print("\n---> Through TCP Port {}".format(port) + "\n")
            with open(outputFile, 'a') as output:
                output.write("\n---> Through TCP Port {}".format(port) + "\n")


