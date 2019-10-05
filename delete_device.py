#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys 
import os
# import inspect

import argparse

class CommandLine:

    option = 0

    def __init__(self):
        parser = argparse.ArgumentParser(description = "Eliminar perfil de hassio")
        parser.add_argument("-M", "--MAC", help = "Example: 64:88:76:87:32", required = True, default = "")

        argument = parser.parse_args()

        self.mac = "{0}".format(argument.MAC)
        if not self.mac.startswith('BT_'):
            self.mac = "BT_" + self.mac


if __name__ == '__main__':
    app = CommandLine()

    myfile = "/hassio/known_devices.yaml" 
  
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
                    if linenum not in range(startline, endline+1):
                        f.write(line)
                    linenum += 1
                f.truncate()


