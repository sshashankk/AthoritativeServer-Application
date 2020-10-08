from socket import *
from flask import make_response, jsonify
from flask import Flask
from flask import request
from flask import abort

import requests
import json

app = Flask(__name__)

@app.route('/register' , methods = ['PUT','POST'])

def json_parse():

    req_data = request.get_json(force = True) 
    
    if "hostname" in req_data:
        hostname = req_data['hostname']  
    else:
        print("Hostname is missing. Aborting...")
        abort(400)
    
    if "ip" in req_data:
        ip = req_data['ip'] 
    else:
        print("IP is missing. Aborting...")
        abort(400)
        
    if "as_ip" in req_data:
        as_ip = req_data['as_ip']  
    else:
        print("AS_IP is missing. Aborting...")
        abort(400)
        
    if "as_port" in req_data:
        as_port = req_data['as_port']  
    else:
        print("AS_PORT is missing. Aborting...")
        abort(400)

    server_name = as_ip
    server_port = int(as_port)

    data = {
        "TYPE" : "A",
        "NAME" : hostname,
        "VALUE" : ip,
        "TTL" : "10",
    }
    data_json = json.dumps(data)
    message = data_json.encode("utf-8")
    print("Sending the JSON data: " + message.decode())
    
    # Create socket
    client_socket = socket(AF_INET, SOCK_DGRAM)
    
    # Send to the server
    client_socket.sendto(message, (server_name, server_port))

    print("Waiting for confirmation response from AS server")
    # Receiver response back
    modified_message, server_address = client_socket.recvfrom(2048)
    print("Recieved the confirmation status: " + modified_message.decode())
    # Close the socket
    client_socket.close()
    if modified_message.decode() == "201":
        return 'OK'
    else:
        abort(400)
    

@app.route('/fibonacci' , methods = ['GET','PUT','POST'])
def fibonacci():
    number = request.args.get('number')
    number = int(number)
    answer = str(fibonacci_calc(number))
    print("Calculated fibonacci number at " + number + " position to be " + answer)
    return answer 

def fibonacci_calc(n):
    a = 0
    b = 1
    if n < 0: 
        print("Wrong input")
    elif n == 0: 
        return a 
    elif n == 1: 
        return b 
    else: 
        for i in range(2,n):
            c = a + b 
            a = b 
            b = c 
        return b 

app.run(host='0.0.0.0',
        port=9090,
        debug=True)


