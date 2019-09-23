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
    user = find_between( contents, "\n  name: ", "\n" )
    if user == "":
        break
    print (user)

