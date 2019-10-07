import sys  
import os

def find_between( s, first, last, end ):
    try:
        start = s.index( first, end ) + len( first )
        end = s.index( last, start )
        return s[start:end], end
    except ValueError:
        return "NOTFOUND", 0



def inject_slot(entity, name):
    host = "192.168.0.156"
    injectionsfile = "/homeassistant/slot_injections.json"

    myfile = open(injectionsfile, "w+")
    myfile.write(	'\n{\n    "operations": [\n' +
    '        [\n            "add",\n' +
    '            {\n                "' + entity + '": [\n' +
    '                   "' + name + '"\n' +
    '               ]\n            }\n' +
    '        ]\n    ]\n}\n')   

    myfile.seek(0)

    print("Inyectando slot: " + name)
    os.system("sudo mosquitto_pub" + " -h " + host + " -t hermes/injection/perform -s < " + injectionsfile)

    myfile.close()
    #os.remove(injectionsfile)




def update_all_slots():
    host = "192.168.0.156"
    injectionsfile = "/homeassistant/slot_injections.json"

    #Lectura de usuarios
    users = []
    end = 0
    myfile = open("/homeassistant/known_devices.yaml", "rt") 
    contents = myfile.read()       
    myfile.close()   
    while True:  
        user, end = find_between( contents, ":\n  name: ", "\n" , end)
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

    print("Actualizando slots: " + str(users))
    os.system("sudo mosquitto_pub" + " -h " + host + " -t hermes/injection/perform -s < " + injectionsfile)

    myfile.close()

    #os.remove(injectionsfile)






if __name__ == "__main__":
    if len(sys.argv) == 3:
        entityname = sys.argv[1]
        slotname = sys.argv[2]
        inject_slot(entityname, slotname)
    if len(sys.argv) == 2:
        entityname = sys.argv[1]
        if str(entitiyname) == "username":
            update_all_slots()
    else:
        print ("error en los parámetros")
        sys.exit()

