import sys  
import os
from hermes_python.hermes import Hermes
from hermes_python.ontology.injection import InjectionRequestMessage, AddInjectionRequest, AddFromVanillaInjectionRequest


def find_between( s, first, last, end ):
    try:
        start = s.index( first, end ) + len( first )
        end = s.index( last, start )
        return s[start:end], end
    except ValueError:
        return "NOTFOUND", 0



def inject_slot(entity, name):
    host = "192.168.0.156:1883"
    injectionsfile = "/hassio/slot_injections.json"

    operations =  [
        AddInjectionRequest({entity : [name] }),
    ]
    request1 = InjectionRequestMessage(operations)

    with Hermes(host) as h:
        print(str(request1))
        #h.request_injection(request1)
"""
    myfile = open(injectionsfile, "w+")
    myfile.write(	'\n{\n    "operations": [\n' +
    '        [\n            "add",\n' +
    '            {\n                "' + entityname + '": [\n' +
    '                   "' + slotname + '"\n' +
    '               ]\n            }\n' +
    '        ]\n    ]\n}\n')   

    myfile.seek(0)

    print("Inyectando slot: " + slotname)
    os.system("sudo mosquitto_pub" + " -h " + host + " -t hermes/injection/perform -s < " + injectionsfile)

    myfile.close()
    #os.remove(injectionsfile)
"""




def update_all_slots():
    host = "192.168.0.156:1883"
    injectionsfile = "/hassio/slot_injections.json"

    #Lectura de usuarios
    users = []
    end = 0
    myfile = open("/hassio/known_devices.yaml", "rt") 
    contents = myfile.read()       
    myfile.close()   
    while True:  
        user, end = find_between( contents, ":\n  name: ", "\n" , end)
        if user == "NOTFOUND":
            break
        users.append(user)

    operations =  [
        AddInjectionRequest({"username" : users }),
    ]

    request2 = InjectionRequestMessage(operations)

    with Hermes(host) as h:
        print(str(request2))
        #h.request_injection(request2)
"""
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
"""






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

