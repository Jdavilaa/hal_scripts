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

    def parse_bool(self, sval):
        if sval == "True" or sval == "true" or sval == "yes":
            return "true"
        elif sval == "False" or sval == "false" or sval == "no":
            return "false"
        else:
            self.status = False
            return ""


    def __init__(self):
        parser = argparse.ArgumentParser(description = "Actualizar perfil de hassio")
        parser.add_argument("-M", "--MAC", help = "Example: 64:88:76:87:32", required = True, default = "")
        parser.add_argument("-u", "--user", help = "Example: johndoe", required = False, default = "")
        parser.add_argument("-n", "--name", help = "Example: John Doe", required = False, default = "")
        parser.add_argument("-pp", "--picturepath", help = "/home/usuario/img/image.jpg", required = False, default = "")
        parser.add_argument("-pu", "--pictureurl", help = "https://icons.org/images/image.jpg", required = False, default = "")
        parser.add_argument("-t", "--track", help = "Example: True", required = False, default = "")
        parser.add_argument("-o", "--hide", help = "Example: False", required = False, default = "")

        argument = parser.parse_args()
        status = False
        self.status = True
        self.options = []

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


def do_update(app):
    myfile = "/homeassistant/known_devices.yaml"
    startline = -1
    endline = 0
    with open(myfile,"r+") as f:
        new_f = f.readlines()

    for line in new_f:

        if "  mac: " + app.mac + "\n" in line:
            startline = endline - 3
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
                elif linenum == startline and "u" in app.options:
                    f.write(app.user.lower() + ":" + "\n")
                elif "o" in app.options and "hide_if_away:" in line:
                    f.write("  hide_if_away: " + app.hide + "\n")
                elif "n" in app.options and "name:" in line:
                    f.write("  name: " + app.name + "\n")
                elif "p" in app.options and "picture:" in line:
                    f.write("  picture: " + app.picture + "\n")
                elif "t" in app.options and "track:" in line:
                    f.write("  track: " + app.track + "\n")
                else:
                    f.write(line)
                linenum += 1
            f.truncate()

  #      if "n" in app.options:
  #          slot_injection.update_all_slots()



if __name__ == '__main__':
    app = CommandLine()
 
    if app.status:
        do_update(app)



