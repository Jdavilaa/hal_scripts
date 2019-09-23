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
            if not os.path.exists("/hassio/www/"):
                os.makedirs("/hassio/www/")
	    #copyfile(src, "/home/pi/homeassistant/www/" + filename)
            copyfile(src, "/hassio/www/" + filename)
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
    myfile = "/hassio/known_devices.yaml"
    linenum = 0
    with open(myfile,"r+") as f:
        new_f = f.readlines()
        f.seek(0)
        encontrado = False
        for line in new_f:
            if "  mac: " + "BT_" + app.mac + "\n" in line:
                encontrado = True
                break
            linenum += 1


    if encontrado:
        old_name = "nnnnnnnn"
        old_user = "uuuuuuuu"

        startline = linenum - 3    
        with open(myfile,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            linenum = 0
            for line in new_f:
                if linenum not in range(startline, startline+7):
                    f.write(line)
                elif linenum == startline and "u" in app.options:
                    old_user = find_between( line, "", ":\n" )
                    f.write(app.user.lower() + ":" + "\n")
                elif linenum == startline + 1 and "o" in app.options:
                    f.write("  hide_if_away: " + app.hide + "\n")
                elif linenum == startline + 4 and "n" in app.options:
                    name_old = find_between( line, "", ":\n" )
                    f.write("  name: " + app.name + "\n")
                elif linenum == startline + 5 and "p" in app.options:
                    f.write("  picture: " + app.picture + "\n")
                elif linenum == startline + 6 and "t" in app.options:
                    f.write("  track: " + app.track + "\n")
                else:
                    f.write(line)
                linenum += 1
            f.truncate()

  #      if "n" in app.options:
  #          slot_injection.update_all_slots()

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



