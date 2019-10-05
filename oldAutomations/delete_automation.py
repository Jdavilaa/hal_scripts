import sys 
import os
import inspect
"""
from pwd import getpwnam
from grp import getgrnam

uid = getpwnam("usuario")[2]
gid = getgrnam("usuario")[2]
"""
import argparse

class CommandLine:

    option = 0

    def __init__(self):
        parser = argparse.ArgumentParser(description = "Eliminar perfil de hassio")
        parser.add_argument("-M", "--MAC", help = "Example: 64:88:76:87:32", required = False, default = "")
        parser.add_argument("-u", "--user", help = "Example: johndoe", required = False, default = "")

        argument = parser.parse_args()
        status = False

        if argument.MAC:
            self.mac = "{0}".format(argument.MAC)
            if not self.mac.startswith('BT_'):
                self.mac = "BT_" + self.mac
            status = True
            self.option = 1

        if argument.user:
            self.user = "{0}".format(argument.user)
            status = True
            self.option = 2


        if not status:
            print("Maybe you want to use -M or -u as arguments ?") 


if __name__ == '__main__':
    app = CommandLine()

    myfile = "/hassio/known_devices.yaml" 

    if app.option == 1:         
        busqueda = "  mac: " + app.mac + "\n"
        row = 3
    elif app.option == 2:         
        busqueda = app.user + ":\n"
        row = 4

    linenum = 0
    with open(myfile,"r+") as f:
        new_f = f.readlines()
        f.seek(0)
        encontrado = False
        for line in new_f:
            if busqueda in line:
                encontrado = True
                break
            linenum += 1

    if encontrado:
        startblock = linenum - row
        deleteblock = range(startblock, startblock + 8)

        with open(myfile,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            linenum = 0
            for line in new_f:
                if linenum not in deleteblock:
                    f.write(line)
                linenum += 1
            f.truncate()

