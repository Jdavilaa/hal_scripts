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
        parser.add_argument("-pp", "--picturepath", help = "/home/usuario/img/image.jpg", required = False, default = "")
        parser.add_argument("-pu", "--pictureurl", help = "https://icons.org/images/image.jpg", required = False, default = "")
        parser.add_argument("-t", "--track", help = "Example: true", required = False, default = "true")
        parser.add_argument("-o", "--hide", help = "Example: false", required = False, default = "false")

        argument = parser.parse_args()
        status = False
        self.status = True
        self.options = []
        self.picture = ""

        self.mac = "{0}".format(argument.MAC)
        if not self.mac.startswith('BT_'):
            self.mac = "BT_" + self.mac

        if argument.user:
            self.user = "{0}".format(argument.user)
            status = True
            self.options.append("u")

        if argument.name:
            self.name = "{0}".format(argument.name)
            status = True
            self.options.append("n")

        if argument.picturepath:
            src = argument.picturepath
            filename = os.path.basename(src)
            #filename = Path(src).name
            if not os.path.exists("/homeassistant/www/"):
                os.makedirs("/homeassistant/www/")
            #copyfile(src, "/home/pi/homeassistant/www/" + filename)
            copyfile(src, "/homeassistant/www/" + filename)
            self.picture = "{0}".format("/local/" + filename)
            status = True
            self.options.append("p")

        if argument.pictureurl:
            self.picture = "{0}".format(argument.pictureurl)
            status = True
            self.options.append("p")

        if argument.track:
            self.track = self.parse_bool("{0}".format(argument.track))
            status = True
            self.options.append("t")

        if argument.hide:
            self.hide = self.parse_bool("{0}".format(argument.hide))
            status = True
            self.options.append("o")

        if not self.status:
            print("Maybe you want to use True, true, False or false to boolean arguments") 

        if not status:
            print("Maybe you want to use -M or -u or -pp or -pu or -t or -o as arguments ?") 
            self.status = False


def do_add(app): 
    myfile = "/homeassistant/known_devices.yaml"

    usuario = os.environ.get('USER')
    uid = getpwnam(usuario)[2]
    gid = getgrnam(usuario)[2]
    if os.path.exists(myfile):
        os.chown(myfile, uid, gid)

    if "u" not in app.options:
        app.user = app.name.lower()
        app.user = app.user.replace(" ","_")


    with open(myfile,"a+") as f:
        f.write("" + app.user + ":" + 
		"\n  hide_if_away: " + app.hide +
		"\n  icon: " +
		"\n  mac: " + app.mac +
		"\n  name: " + app.name +
		"\n  picture: " + app.picture +
		"\n  track: " + app.track + "\n\n") 
  
    #inject_slot("username", app.name)   


if __name__ == '__main__':
    app = CommandLine()
 
    if app.status:
        do_add(app)

