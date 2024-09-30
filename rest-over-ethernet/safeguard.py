#!/usr/local/bin/python3

import requests
import ssl
import warnings
import argparse
import json
import signal
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="IP address or hostname of library")
parser.add_argument("-u", "--user", help="Username for logging into the library")
parser.add_argument("-p", "--password", help="Password for logging into the library")
parser.add_argument("-s", "--source", help="Source logical library")
parser.add_argument("-d", "--destination", help="Destination logical library")
parser.add_argument("-c", "--create", help="Create the destination logical library if it does not already exist", action="store_true")
parser.add_argument("-n", "--noerror", help="Ignore any SSL errors", action="store_true")
parser.add_argument("-q", "--quick", help="Reduce runtime by skipping the completion check at the end", action="store_true")
args = parser.parse_args()

show_http_error = False
quick_run = args.quick
create_LL = args.create

if args.noerror:
    warnings.filterwarnings("ignore")

# get all the necessary user input if it was not specified in the command
if args.ip:
    ip = args.ip
else:
    ip = input("Library IP: ")

if args.user:
    username = args.user
else:
    username = input("Username: ")

if args.password:
    password = args.password
else:
    password = input("Password: ")

if args.source:
    sourceLL = args.source
else:
    sourceLL = input("Source logical library: ")

if args.destination:
    destinationLL = args.destination
else:
    destinationLL = input("Destination logical library: ")
    create_LL = input("Does this logical library already exist? (y/n): ").lower().strip() == 'n'

base_url = "https://" + ip + "/web/api/v1/"
login_endpoint = "login"
logout_endpoint = "logout"
drives_endpoint = "drives"
data_cart_endpoint = "dataCartridges"
logical_libraries_endpoint = "logicalLibraries"
assign_arg = "/assignDataCartridges"
login_json = '{"user":"' + username + '", "password":"' + password + '"}'
ca_file='/etc/pki/tls/certs/ca-bundle.crt'
ca_file=False
source_details = dict()
destination_details = dict()
cart_list = list()
source_found = False
destination_found = False
task_failed = False
all_drives_empty = True
max_carts_per_request = 30

session = requests.Session()
session.headers.update({'Content-Type': 'application/json'})

# login to the library
response = session.post(base_url + login_endpoint, data=login_json, verify=ca_file)

if show_http_error:
    print("Login: " + str(response))
    print()

endpoint = ""

# function used to ensure that this script logs out after completion
def cleanup(*args):
    response = session.post(base_url + logout_endpoint, data=login_json, verify=ca_file)
    if show_http_error:
        print("Logout: " + str(response))

    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

# get the details of the affected logical libraries, if they exist
response = session.get(base_url + logical_libraries_endpoint, verify=ca_file)
try:
    json_output = json.loads(response.text)

    for ll in json_output:
        if ll['name'] == sourceLL:
            source_details = ll
            source_found = True
        elif ll['name'] == destinationLL:
            destination_details = ll
            destination_found = True
except:
    print(response.text)
    print("!!!!!!!!!!!!!!!! Invalid JSON !!!!!!!!!!!!!!!!")

# create the destination logical library if it does not already exist and the parameter was included
if create_LL:
    if destination_found:
        print("Create option was specified, but destination logical library '" + destinationLL + "' already exists, ignoring...")
        print()
    else:
        print("Creating logical library '" + destinationLL + "'")
        print()
        payload = '{"name": "' + destinationLL + '", "mediaType": "' + str(source_details['mediaType']) + '"}'
        response = session.post(base_url + logical_libraries_endpoint, verify=ca_file, json=json.loads(payload))

        if response.status_code == 201:
            response = session.get(base_url + logical_libraries_endpoint + '/' + destinationLL, verify=ca_file)
            try:
                json_output = json.loads(response.text)

                for ll in json_output:
                    if ll['name'] == destinationLL:
                        destination_details = ll
                        destination_found = True
            except:
                print(response.text)
                print("!!!!!!!!!!!!!!!! Invalid JSON !!!!!!!!!!!!!!!!")

print("Source logical library details:")
print(json.dumps(source_details, indent=4))
print()
print("Destination logical library details:")
print(json.dumps(destination_details, indent=4))
print()

# search for any drives in the logical libraries that currently have a cartridge inserted
response = session.get(base_url + drives_endpoint, verify=ca_file)
try:
    json_output = json.loads(response.text)

    for drive in json_output:
        if drive['logicalLibrary'] == sourceLL or drive['logicalLibrary'] == destinationLL:
           if drive['volser'] != None:
                all_drives_empty = False
except:
    print(response.text)
    print("!!!!!!!!!!!!!!!! Invalid JSON !!!!!!!!!!!!!!!!")

if all_drives_empty:
    # only proceed if both logical libraries exist
    # and they are the same media type
    # and the source logical library contains cartridges
    # and the destination logical library is empty
    # and at least one of the logical libraries contains no drives
    # all of these checks are necessary for this to be a valid safeguarded tape use
    if source_found and destination_found and source_details['mediaType'] == destination_details['mediaType'] and source_details['cartridges'] > 0 and destination_details['cartridges'] == 0 and (source_details['drives'] == 0 or destination_details['drives'] == 0):
        # get all of the data cartridges in the library, and add any that are in the source logical library to a list
        response = session.get(base_url + data_cart_endpoint, verify=ca_file)
        try:
            json_output = json.loads(response.text)
            
            for cartridge in json_output:
                if cartridge['logicalLibrary'] == sourceLL:
                    # this is done with the internalAddress attribute to ensure duplicate VOLSERs are handled appropriately
                    cart_list.append(str(cartridge['internalAddress']))
        except:
            print(response.text)
            print("!!!!!!!!!!!!!!!! Invalid JSON !!!!!!!!!!!!!!!!")

        total_carts = len(cart_list)
        print("Reassigning " + str(total_carts) + " cartridges from '" + sourceLL + "' to '" + destinationLL + "'")
        print()

        # generate the individual requests by creating sublists of cartridges containing up to <max_carts_per_request> cartridges
        for i in range(0, len(cart_list), max_carts_per_request):
            assign_list = cart_list[i:i + max_carts_per_request]
            payload = '{"cartridges": ['
            while len(assign_list) > 1:
                payload = payload + '"' + assign_list.pop() + '",'

            payload = payload + '"' + assign_list.pop() + '"]}'

            #print("Sending assign request with JSON: " + payload)

            response = session.post(base_url + logical_libraries_endpoint + '/' + destinationLL + assign_arg, verify=ca_file, json=json.loads(payload))
            if response.status_code != 201:
                task_failed = True
                print("A cartridge assignment request failed!")
                print("JSON from failed request: " + payload)
                print(response)
                print()
                
            #print(response)
            #print()

        if not quick_run and not task_failed:
            print("Polling for completion")
            try:
                num_carts = 1
                poll_count = 120

                while num_carts > 0 and poll_count > 0:
                    time.sleep(5)
                    # check how many cartridges are still assigned to the source logical library
                    response = session.get(base_url + logical_libraries_endpoint + '/' + sourceLL)
                    json_output = json.loads(response.text)
                    num_carts = int(json_output[0]['cartridges'])
                    percent_complete = (100*(total_carts - num_carts))/total_carts
                    #print("Cartridges remaining in logical library: " + str(num_carts))
                    print(str(int(percent_complete)) + '% complete')
                    poll_count = poll_count - 1

                print()
                if num_carts > 0:
                    print("Check logical library contents later for completion status")
                else:
                    print("Operation complete")
            except:
                print("!!!!!!!!!!!!!!!! Invalid JSON !!!!!!!!!!!!!!!!")
                print(response.text)
    else:
        print("Invalid logical library selection")
else:
    print("All drives in the logical library MUST be empty. No cartridges have been reassigned")

if task_failed:
    print("At least one assignment operation failed, see previous messages.")

cleanup()
