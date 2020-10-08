#Import all dependencies
from socket import *
from flask import Flask
from flask import request
from flask import abort
import requests
import json

app = Flask(__name__)

#Define the route
@app.route('/fibonacci', methods = ['GET'])

#Fibonacci
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    if(hostname == None or fs_port == None or number == None or as_ip == None or as_port == None):
        print("Error in the URL entered or there is some data missing. Aborting...")
        abort(400)
    
    print("URL Validated")
    
    data = {
        "TYPE" : "A",
        "NAME" : hostname,
    }
    
    data_json = json.dumps(data)
    message = data_json.encode("utf-8")
    print("Sending the JSON data: " + message.decode())

#Create socket
    server_name = as_ip
    server_port = int(as_port)
    client_socket = socket(AF_INET, SOCK_DGRAM)

#Send to the server
    client_socket.sendto(message, (server_name, server_port))
    
    print("Sent")
    print("Waiting for response from AS server")

#Receiver response back
    modified_message, server_address = client_socket.recvfrom(2048)
    print("Got the status back from AS Server: " + modified_message.decode())

#Close the socket
    client_socket.close()
    
    if(modified_message.decode() == "400"):
        print("FS and AS not registered yet or Error in the input. Aborting...")
        abort(400)
    elif(modified_message.decode() == "201"):
        print("Successfully received the server name and server port")

    all_data = modified_message.decode()
    alldata = json.loads(all_data) 

    d_ip = alldata['VALUE']
    fib = alldata['NAME']
    
    if(d_ip == None or fib == None or fib != "fibonacci.com"):
        print("Error in the data received from AS Server. Aborting.")
        abort(400)

    fib_list = fib.split('.')
    if(fib_list[0] != None):
        fib = fib_list[0]

    urlfib = "http://"+ d_ip + ":" + fs_port + "/" + fib + "?" + "number=" + number
    
    print("Trying to connect with FS Server on URL: " + urlfib)
    answer = requests.post(urlfib)
    result = str(answer.text)
    print("Received the fibonacci output: " + result)
    return result
    

app.run(host='0.0.0.0',
        port=8181,
        debug=True)




