#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys 
import os
import argparse
#from pathlib import Path
from shutil import copyfile
#import slot_injection

from pwd import getpwnam
from grp import getgrnam


class CommandLine:

    def parse_bool(self, sval):
        if sval == "True" or sval == "true" or sval == "yes":
            return "true"
        elif sval == "False" or sval == "false" or sval == "no":
            return "false"
        else:
            self.status = False
            return ""


    def __init__(self):
        parser = argparse.ArgumentParser(description = "Crear perfil de hassio")
        parser.add_argument("-M", "--MAC", help = "Example: 64:88:76:87:32", required = True, default = "")
        parser.add_argument("-u", "--user", help = "Example: johndoe", required = False, default = "")
        parser.add_argument("-n", "--name", help = "Example: John Doe", required = True, default = "")
        parser.add_argument("-m", "--message", help = "Example: Buenos dias Mariano", required = False, default = "")

        argument = parser.parse_args()
        status = False
        self.status = True
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

        if not self.status:
            print("Maybe you want to use True, true, False or false to boolean arguments") 

        if not status:
            print("Maybe you want to use -M or -u or -pp or -pu or -t or -o as arguments ?") 
            self.status = False


def do_add(app): 

    usuario = os.environ.get('USER')
    uid = getpwnam(usuario)[2]
    gid = getgrnam(usuario)[2]

    if "u" not in app.options:
        app.user = app.name.lower()
        app.user = app.user.replace(" ","_")

    if "m" not in app.options:
        app.message = "Saludos "+ app.name

    myfile = "/homeassistant/automations.yaml"
    if os.path.exists(myfile):
        os.chown(myfile, uid, gid)

    with open(myfile,"r+") as f:
        first_line = f.readline()
        if "[]" in first_line:
            f.truncate()

    with open(myfile,"a") as f:
        f.write("- id: 'saludo_" + app.mac[::3] + app.mac[1::3] + "'" +
		"\n  alias: Saludar a " + app.name +
		"\n  trigger:" +
		"\n  - platform: state" +
		"\n    entity_id: device_tracker." + app.user +
		"\n    from: not_home" +
		"\n    to: home" +
		"\n  condition:" +
		"\n    condition: time" +
		"\n    after: '12:00:00'" +
		"\n    before: '00:00:00'" +
		"\n  action:" +
		"\n  - service: snips.say" +
		"\n    data:" +
		"\n      text: \""+ app.message +"\"\n\n") 



if __name__ == '__main__':
    app = CommandLine()
 
    if app.status:
        do_add(app)

