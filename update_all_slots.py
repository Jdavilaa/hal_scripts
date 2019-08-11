import sys  
import os


def find_between( s, first, last ):
    try:
        global end
        start = s.index( first, end ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return "NOTFOUND"


host = "192.168.0.156"
injectionsfile = "/hassio/slot_injections.json"

#Lectura de usuarios
users = []
end = 0
myfile = open("/hassio/known_devices.yaml", "rt") 
contents = myfile.read()       
myfile.close()   
while True:  
    user = find_between( contents, ":\n  name: ", "\n" )
    if user == "NOTFOUND":
        break
    users.append(user)


myfile = open(injectionsfile, "w+")
myfile.write(	'\n{\n    "operations": [\n' +
'        [\n            "addFromVanilla",\n' +
#'            {\n                "' + entityname + '": [\n')
'            {\n                "username": [\n')
count = len(users)
for name in users:
    myfile.write('                   "' + name)
    count -= 1
    if count != 0:
        myfile.write('",\n')
    else:
        myfile.write('"\n')
myfile.write(
'               ]\n            }\n' +
'        ]\n    ]\n}\n')   

myfile.seek(0)

#-------------------------------------------------------
#contents = myfile.read()
#print(contents)
os.system("sudo mosquitto_pub" + " -h " + host + " -t hermes/injection/perform -s < " + injectionsfile)
#---------------------------------------------------------

myfile.close()

#os.remove(injectionsfile)
