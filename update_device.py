import sys 
import os
import argparse
from shutil import copyfile
from pathlib import Path
import slot_injection

class CommandLine:

    def parse_bool(self, sval):
        if sval == "True" or sval == "true":
            return "yes"
        elif sval == "False" or sval == "false":
            return "no"
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
            filename = Path(src).name
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
            if "  mac: " + app.mac + "\n" in line:
                encontrado = True
                break
            linenum += 1

    if encontrado:
        startline = linenum - 2
        with open(myfile,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            linenum = 0
            for line in new_f:
                if linenum not in range(startline, startline+6):
                    f.write(line)
                elif linenum == startline and "u" in app.options:
                    f.write(app.user.lower() + ":" + "\n")
                elif linenum == startline + 1 and "n" in app.options:
                    f.write("  name: " + app.name + "\n")
                elif linenum == startline + 3 and "p" in app.options:
                    f.write("  picture: " + app.picture + "\n")
                elif linenum == startline + 4 and "t" in app.options:
                    f.write("  track: " + app.track + "\n")
                elif linenum == startline + 5 and "o" in app.options:
                    f.write("  hide_if_away: " + app.hide + "\n")
                else:
                    f.write(line)
                linenum += 1
            f.truncate()

        if "u" in app.options:
            slot_injection.update_all_slots()


if __name__ == '__main__':
    app = CommandLine()
 
    if app.status:
        do_update(app)



"""
def switch_line(startline, linenum, line):
    return {
        startline: f.write(app.user.lower() + ":" + "\n"),
        startline+1: f.write("  name: " + app.name + "\n"),
        startline+3: f.write("  picture: " + app.picture + "\n"),
        startline+4: f.write("  track: " + app.track + "\n"),
        startline+5: f.write("  hide_if_away: " + app.hide + "\n")
    }.get(linenum, f.write(line)) 
"""



"""
if len(sys.argv) >= 3:
    mac = sys.argv[1]
    name = sys.argv[2]
    if len(sys.argv) > 3:
        picture = sys.argv[3]
    else:
        picture = ""
else:
    mac = input("MAC:")
    name = input("Nombre:")
    picture = input("Imagen:")

end = 0

def find_between( s, first, last ):
    try:
	global end
        start = s.index( first, end ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
	return ""

myfile = open("/hassio/known_devices.yaml", "rt") 
contents = myfile.read()       
myfile.close()   
while True:  
    user = find_between( contents, ":\n  name: ", "\n" )
    if user == "":
	break
    print user





known_devices = "/hassio/known_devices.yaml"
os.chown(known_devices, uid, gid)
with open(known_devices, "a") as myfile:
    myfile.write(	"\n" + str(name).lower() + ":" + 
			"\n  name: " + str(name) +
			"\n  mac: " + str(mac) +
			"\n  picture: " + str(picture) +
			"\n  track: yes" +
			"\n  hide_if_away: no\n")     
"""

