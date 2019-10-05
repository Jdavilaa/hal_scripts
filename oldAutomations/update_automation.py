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
        parser.add_argument("-ou", "--olduser", help = "Example: johndoe1", required = False, default = "")
        parser.add_argument("-on", "--oldname", help = "Example: JohnDoe", required = False, default = "")

        argument = parser.parse_args()zz
        status = False
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

        if argument.olduser:
            self.olduser = "{0}".format(argument.olduser)
            status = True
            self.options.append("ou")

        if argument.oldname:
            self.oldname = "{0}".format(argument.oldname)
            status = True
            self.options.append("on")



        if not status:
            print("Maybe you want to use -M or -u or -ou or -n or -on arguments ?") 


def do_update(app):
        myfile = "/hassio/automations.yaml"
  
        with open(myfile,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if "u" in app.options and "- id: 'saludo_" + old_user in line:
                    f.write("- id: 'saludo_" + app.user + "\n")
                elif "u" in app.options and "    entity_id: device_tracker." + old_user in line:
                    f.write("    entity_id: device_tracker." + app.user + "\n")
                elif "n" in app.options and "  alias: Saludar a " + old_name in line:
                    f.write("  alias: Saludar a " + app.name + "\n")
                elif "n" in app.options and "      text: \"Hola " + old_name in line:
                #elif "n" in app.options and "      text: \".*" + old_name + ".*" in line:
                    f.write("      text: \"Hola " + app.name + "\n")
                else:
                    f.write(line)



if __name__ == '__main__':
    app = CommandLine()
 
    if app.status:
        do_update(app)



