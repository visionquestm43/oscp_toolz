#!/usr/bin/env python3

import msfrpc
import time



outputFile = '/root/oscplab/labtargets/dot221/dot221_winrm.txt'
domain = 'THINC'
RHOSTS = '10.11.1.221'

startPort = 5000  #Last scan completed  Mar 10 thru TCP port
endPort = 5500
portRange = range(startPort, endPort)

'''
Open client connection to msf via msfrpc/msgrpc
Start postgressql.service, start msfconsole,  load msgrpc User='msf' Pass='abc123'
'''

#Create a new instance of the Msfrpc client with the default options
client = msfrpc.Msfrpc({})

# Login to the msfmsg server using the username and password used to load msgrpc
client.login('msf', 'abc123')
sess = client.call('console.create')
console_id = sess[b'id']  # Added 'b'
# print(sess.keys()) Used for troubleshooting and confirmed the presence of the 'b'

deleteMsfWorkspace = "workspace -d mac10\n"
createMsfWorkspace = "workspace -a mac10\n"
client.call('console.write', [console_id, createMsfWorkspace])

use_winrm = 'use auxiliary/scanner/winrm/winrm_auth_methods\n'
set_rhosts = ('set RHOSTS %s \n' % RHOSTS)
set_domain = ('set DOMIAN %s \n' % domain)

setup_client = [use_winrm, set_rhosts, set_domain]

for cmd in setup_client:
    print(cmd)
    client.call('console.write', [console_id, cmd])
    setup_output = client.call('console.read', [console_id])

print("********")
print("Testing ip %s" % RHOSTS, "ports {} to {}".format(startPort, endPort))
print("********")

with open(outputFile, 'w') as output:
    output.write("Testing ip %s " % RHOSTS + "ports {} to {}:\n".format(startPort, endPort))
    #output.write("ports {} to {}:\n".format(startPort, endPort))

with open(outputFile, 'a') as output:
    output.write("********\n\n")

for port in portRange:
    '''
    if port % 100 == 0:
    print("Pausing for 10 sec...")
    time.sleep(10)
    '''
    client.call('console.write', [console_id, 'set RPORT %s \n' % port])
    rportoutput = client.call('console.read', [console_id])
    #print(rportoutput[b'data'].decode("utf-8"))

    run_with_rport = client.call('console.write', [console_id, 'run\n'])

    time.sleep(1)
    runoutput = client.call('console.read', [console_id])
    runoutput_data = runoutput[b'data'].decode("utf-8")
    print(runoutput_data)

    if port % 1 == 50:
        with open(outputFile, 'a') as output:
            output.write(runoutput_data + "\n")

        print("Pausing for 5 sec...")
        time.sleep(5)

    string2find = 'protocol'
    protocol_present = runoutput_data.find(string2find)

    if protocol_present != -1:
        print("\n!!!!!!!!!!\n\n" + runoutput_data + "\n!!!!!!!!!!\n\n")
        with open(outputFile, 'a') as output:
            output.write("\n!!!!!!!!!!\n\n" + runoutput_data + "\n!!!!!!!!!!\n\n")




