#This is the IBM Safeguard Tape Sample Script, intended to be customized by the end user that will take a list of cartridges from an online logical library to an offline logical library, and can bring them back online.
import os
import csv
import sys
import argparse

#This script assumes the following:
#1: User has installed the TS4500 CLI as a pre-requisite: https://www.ibm.com/docs/it/ts4500-tape-library?topic=commands-installing-cli
#2: User provides a list of cartridges and logical library destinations in a txt file (Sample: filename.txt)
#3: User has both an online and offline logical library created (https://www.ibm.com/docs/en/ts4500-tape-library?topic=libraries-creating-logical)
#4: User provides a target logical library to be moved to (offline or online depending on the scenario)
#5: Where indicated '-ip' address is the IP address of the TS4500
#6: Where indicated '-u' user is a valid login for the TS4500 with Administrator role
#7: Where indicated '-p' user password for user
#8: This script is intended for end user customization, including template fields and is not expected to run as is.
#** Offline logical library defined as a logical library with no (0) drives

#This code enables command line arguments of the source and target destinations to be passed by the end user into the script
parser = argparse.ArgumentParser(description='Logical Library Information')

parser.add_argument('--sourceLogicalLibrary', dest='sourceLogicalLibrary', type=str, help='Name of source logical library')

parser.add_argument('--targetLogicalLibrary', dest='targetLogicalLibrary', type=str, help='Name of target logical library')

args = parser.parse_args()


os.system("java -jar TS4500CLI.jar -ip address -u user -p pwd --viewLogicalLibraries librarylist.csv")
#This will generate a list of existing logical libraries into a CSV file - By default, the file is saved in the directory where the TS4500CLI.jar file is stored.
#To save the file in a different directory, specify the path to that directory.

#First: verify your existing logical libraries - online and offline
sourceLibName = args.sourceLogicalLibrary
targetLibName = args.targetLogicalLibrary

with open("librarylist.csv", 'r') as file:
  csvreader = csv.reader(file)
  librarylist = list(csvreader)
  for i, val in enumerate(librarylist):
  	print(i, ",", val)
  	print(val[0])
  	if sourceLibName in val[0]:
  		print("Source Found!")
  	else:
  		print("Source Not Found")
  	if targetLibName in val[0]:
  		print("Target Found!")
  	else:
  		print("Target Not Found")

#Second: move the cartridges from one logical library to another

os.system("java -jar TS4500CLI.jar -ip address -u user -p pwd --assignDataCartridges filename.txt")

#Third: media verification to determine that the tape cartridges are readable: https://www.ibm.com/docs/en/ts4500-tape-library?topic=cartridges-automatic-media-verification

os.system("java -jar TS4500CLI.jar -ip address -u user -p pwd --setDriveUse -use verification -f# -c# -r#")

#Caution: moving a cartridge to a non-existent or the incorrect logical library name will result in false 'The cartridges were assigned succesfully response.'