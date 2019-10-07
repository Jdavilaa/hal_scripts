#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys 
import os
import argparse
from shutil import copyfile
#from pathlib import Path
#import slot_injection

end = 0

def find_between( s, first, last ):
    try:
        global end
        start = s.index( first, end ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class CommandLine:


    def __init__(self):
        parser = argparse.ArgumentParser(description = "Actualizar perfil de hassio")
        parser.add_argument("-M", "--MAC", help = "Example: 64:88:76:87:32", required = True, default = "")
        parser.add_argument("-u", "--user", help = "Example: johndoe", required = False, default = "")
        parser.add_argument("-n", "--name", help = "Example: John Doe", required = False, default = "")
        parser.add_argument("-m", "--message", help = "Example: Buenos días Jonny!", required = False, default = "")
        # parser.add_argument("-t", "--automation_type", help = "Example: JohnDoe", required = False, default = "")

        argument = parser.parse_args()
        status = False
        self.options = []

        self.mac = "{0}".format(argument.MAC)
        if self.mac.startswith('BT_'):
            self.mac = self.mac[3::]

        if argument.user:
            self.user = "{0}".format(argument.user)
            status = True
            self.options.append("u")

        if argument.name:
            self.name = "{0}".format(argument.name)
            status = True
            self.options.append("n")

        if argument.message:
            self.message = "{0}".format(argument.message)
            status = True
            self.options.append("m")

        # if argument.automation_type:
        #     self.automation_type = "{0}".format(argument.automation_type)
        #     status = True
        #     self.options.append("t")

        # if argument.olduser:
        #     self.olduser = "{0}".format(argument.olduser)
        #     status = True
        #     self.options.append("ou")

        # if argument.oldname:
        #     self.oldname = "{0}".format(argument.oldname)
        #     status = True
        #     self.options.append("on")



        if not status:
            print("Maybe you want to use -M or -u or -ou or -n or -on arguments ?") 


def do_update(app):

    myfile = "/homeassistant/automations.yaml"
    startline = -1
    endline = 0

    with open(myfile,"r+") as f:
        new_f = f.readlines()

    for line in new_f:

        if "- id: 'saludo_" + app.mac[::3] + app.mac[1::3] + "'\n" in line:
            startline = endline
        if startline >= 0 and line in ['\n', '\r\n']: 
            break
        endline += 1


    if startline >= 0:

        linenum = 0
        with open(myfile,"r+") as f:

            new_f = f.readlines()
            f.seek(0)

            for line in new_f:
                if linenum not in range(startline, endline):
                    f.write(line)
                # elif "u" in app.options and "- id: 'saludo_" + old_user in line:
                #     f.write("- id: 'saludo_" + app.user + "\n")
                elif "u" in app.options and "entity_id: device_tracker" in line:
                    f.write("    entity_id: device_tracker." + app.user + "\n")
                elif "n" in app.options and "  alias:" in line:
                    f.write("  alias: Saludar a " + app.name + "\n")
                elif "m" in app.options and "text:" in line:
                    f.write("      text: \" " + app.message + "\n")
                else:
                    f.write(line)
                linenum += 1

            f.truncate()



if __name__ == '__main__':
    app = CommandLine()
 
    do_update(app)



