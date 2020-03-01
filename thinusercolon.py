#!/usr/bin/env python3

with open ("/root/oscplab/thinc_users_all.list") as w:
        for line in w:
                username = line.rstrip()
                with open ("/root/oscplab/thinc_plaintext_all.list") as plaintext:
                        for line in plaintext:
                                password = line.rstrip()
                                with write ("/root/oscplab/thinc_usercolonpass.list", 'a') as output:
                                    output.write(username,":",password)