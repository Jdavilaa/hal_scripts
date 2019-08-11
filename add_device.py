import sys 
import os
import slot_injection

from pwd import getpwnam
from grp import getgrnam

uid = getpwnam("usuario")[2]
gid = getgrnam("usuario")[2]

if len(sys.argv) >= 3:
    name = sys.argv[1]
    mac = sys.argv[2]
    if len(sys.argv) > 3:
        picture = sys.argv[3]
    else:
        picture = ""
else:
    name = input("Nombre:")
    mac = input("MAC:")
    picture = input("Imagen:")

known_devices = "/hassio/known_devices.yaml"
os.chown(known_devices, uid, gid)
with open(known_devices, "a") as myfile:
    myfile.write(	"\n" + str(name).lower() + ":" + 
			"\n  name: " + str(name) +
			"\n  mac: " + str(mac) +
			"\n  picture: " + str(picture) +
			"\n  track: yes" +
			"\n  hide_if_away: no\n")   
inject_slot("username", str(name))  


