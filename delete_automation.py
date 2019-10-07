#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys 
import os
# import inspect
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
        parser.add_argument("-M", "--MAC", help = "Example: 64:88:76:87:32", required = True, default = "")
       
        argument = parser.parse_args()
        status = False

        self.mac = "{0}".format(argument.MAC)
        if self.mac.startswith('BT_'):
            self.mac = self.mac[3::]
       


if __name__ == '__main__':
    app = CommandLine()

    myfile = "/homeassistant/automations.yaml" 

    
    ignorar_linea = False
    linenum = 0

    with open(myfile,"r+") as f:
        new_f = f.readlines()
        f.seek(0)

        for line in new_f:

            if "- id: 'saludo_" + app.mac[::3] + app.mac[1::3] + "'\n" in line:
                ignorar_linea = True
            elif not ignorar_linea:
                f.write(line)
            elif ignorar_linea and line in ['\n', '\r\n']: 
                ignorar_linea = False
        f.truncate()

