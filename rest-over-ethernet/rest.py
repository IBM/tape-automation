#!/usr/local/bin/python3
#
# Copyright 2023 IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#

import requests
import ssl
import warnings
import argparse
import json
import signal
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="IP address or hostname of library")
parser.add_argument("-u", "--user", help="Username for logging into the library")
parser.add_argument("-p", "--password", help="Password for logging into the library")
parser.add_argument("-e", "--endpoint", help="Specify a single endpoint to run against")
parser.add_argument("-j", "--json", help="Performs basic JSON validation on the response", action="store_true")
parser.add_argument("-s", "--showhttperror", help="Shows the HTTP error code with the data", action="store_true")
parser.add_argument("-n", "--noerror", help="Ignore any SSL errors", action="store_true")
parser.add_argument("-r", "--nourl", help="Do not display the URL that is being queried", action="store_true")
parser.add_argument("-m", "--method", help="Default HTTP method for this request. POST, PUT, GET accepted.")
parser.add_argument("-jp", "--payload", help="JSON payload for requests.")
args = parser.parse_args()

if args.noerror:
    warnings.filterwarnings("ignore")

if args.ip:
    ip = args.ip
else:
    print("Library IP: ")
    ip = input()

if args.user:
    username = args.user
else:
    print("Username: ")
    username = input()

if args.password:
    password = args.password
else:
    print("Password: ")
    password = input()

if args.method:
    defaultMethod = args.method.upper()
else:
    print("Default method: ")
    defaultMethod = input().upper()


show_http_error = args.showhttperror

base_url = "https://" + ip + "/web/api/v1/"
login_endpoint = "login"
logout_endpoint = "logout"
login_json = '{"user":"' + username + '", "password":"' + password + '"}'
ca_file='/etc/pki/tls/certs/ca-bundle.crt'
ca_file=False

session = requests.Session()
session.headers.update({'Content-Type': 'application/json'})
response = session.post(base_url + login_endpoint, data=login_json, verify=ca_file)

if args.showhttperror:
    print("Login: " + str(response))
    print()

endpoint = ""

def cleanup(*args):
    response = session.post(base_url + logout_endpoint, data=login_json, verify=ca_file)
    if show_http_error:
        print("Logout: " + str(response))

    sys.exit(0)

if defaultMethod == "POST":
    defaultHttpFunction = session.post
elif defaultMethod == "PUT": 
    defaultHttpFunction = session.put
else :
    defaultHttpFunction = session.get

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

while (endpoint != "exit" and endpoint != "quit" and endpoint != "logout"):
    httpFunction = defaultHttpFunction
    isAltFunction = False
    if args.endpoint:
        endpoint = args.endpoint
        if args.payload:
            json_input = json.loads(args.payload)
            input_array = [endpoint, args.payload]

        else :
            input_array = [endpoint]

    else:
        print("Next request:")
        raw_input = input()
        input_array = raw_input.split(" ", 1)
        endpoint = input_array[0] 

    if endpoint != "exit" and endpoint != "quit" and endpoint != "logout":
        
        # added support for post, put, patch 
        endpoint_as_upper = endpoint.upper()
        if endpoint_as_upper == "POST":
            httpFunction = session.post
            isAltFunction = True

        elif endpoint_as_upper == "PUT": 
            httpFunction = session.put
            isAltFunction = True

        elif endpoint_as_upper == "GET":
            httpFunction = session.get
            isAltFunction = True
        
        num_args = len(input_array)
        if isAltFunction: #changes params based on new format if new method is selected

            input_array = raw_input.split(" ", 2) # limit keeps json input together
            num_args = len(input_array)
            endpoint = input_array[1]
            num_args= num_args -1 # number of args not including the method

            if num_args > 1:
                json_input = json.loads(input_array[2])

            else :
                json_input = ""
        elif not (args.endpoint):
            if num_args > 1 :
                json_input = json.loads(input_array[1])

            else:
                json_input = ""

        url = base_url + endpoint
        if not args.nourl:
            print("URL = '" + url + "'")

        # added support for post, put
        response = httpFunction(url, verify=ca_file) if (num_args == 1) else httpFunction(url, verify=ca_file, json=json_input)
    
        if args.showhttperror:
            print(response)
    
        if args.json:
            try:
                json_output = json.loads(response.text)
                # response.json()
                print(json.dumps(json_output, indent=4))
            except:
                print(response.text)
                print("!!!!!!!!!!!!!!!! Invalid JSON !!!!!!!!!!!!!!!!")
        else:
            print(response.text)

    print()
    
    if args.endpoint:
        endpoint = "exit"

cleanup()
