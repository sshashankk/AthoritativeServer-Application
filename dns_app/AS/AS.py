from socket import *
from flask import abort
import json

server_port = 53533

# Create a socket (UDP)
server_socket = socket(AF_INET, SOCK_DGRAM)
# Bind to port
server_socket.bind(('', server_port))

print("Socket at Server Side Created")
flag = False

while(True):
    print("Waiting to recieve the request from client")
    message, client_address = server_socket.recvfrom(2048)
    modified_message = message.decode()
    data = json.loads(modified_message)
    print("Recieved message: " + modified_message)
        
    if(len(data) == 4): 
        with open('.//regis_file.txt', 'w', encoding='utf-8') as f:
            if (data['TYPE'] == None or data['NAME'] == None or data['VALUE'] == None or data['TTL'] == None):
                message = "400"
                print("FS and AS yet to be registered or There is an error in the input. Try registering again!")
            else:
                s = json.dumps(data, indent=4, sort_keys=True)
                f.writelines(s)
                message = "201"
                flag = True
                print("Sending back the registeration response to FS server")
                print("Done with Registering")
                
    elif(len(data) == 2):
        if (flag == False):
            print("Try registering FS first")
            message = "400"
            # continue
        else:
            if (("TYPE" not in data) or ("NAME" not in data)):                                         
                print("Error in data or some keys in the data are missing. Aborting.")
                abort(400)
        
            with open('regis_file.txt', 'r') as f:
                file_dict = json.load(f)
                if(file_dict['TYPE'] != None and file_dict['NAME'] != None and file_dict['VALUE'] != None and file_dict['TTL'] != None and data['NAME'] == file_dict['NAME'] and data['TYPE'] == file_dict['TYPE']):
                    response_data = {
                        'TYPE' : file_dict['TYPE'],  
                        'NAME' : file_dict['NAME'],
                        'VALUE' : file_dict['VALUE'],
                        'TTL' : file_dict['TTL']
                    }
                    print("Sending back the response to US server")
                    message = json.dumps(response_data)
                else:
                    print("Sending back the response to US server")
                    print("Data in the Text File Missing")
                    message = "400"
    
    else:
        print("Insufficient data passed")
        message = "400"
        
    server_socket.sendto(message.encode(), client_address)
    print("Sent")


app.run(host='0.0.0.0',
        port=53533,
        debug=True)
 
