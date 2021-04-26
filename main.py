import sys
import json
import argparse

import helper
import realityHub
import pachamama

parser = argparse.ArgumentParser()
parser.add_argument('-fileName',
                    type=str,
                    help='Event JSON')
parser.add_argument('-realityHub',
                    type=str,
                    help='Reality Hub Credential')
parser.add_argument('-pachamamaHub',
                    type=str,
                    help='Pachamama Hub Credential')
##parser.add_argument('-eventbrite',
##                    type=str,
##                    help='Eventbrite Credentials')
args = parser.parse_args()
fileName = args.fileName
realityHubCredFile = args.realityHub
##eventbriteCred = args.eventbrite
pachmamaCredFile = args.pachamamaHub

eventObj = {}
try:
    with open(fileName, "r") as f:
        eventObj = json.load(f)
except OSError:
    print("File Read Error")
helper.PrettyPrintJSON(eventObj)


realityHubCred = {}
try:
    with open(realityHubCredFile, "r") as f:
        realityHubCred = json.load(f)
except OSError:
    print("Reality Hub Credentials File Read Error")
helper.PrettyPrintJSON(realityHubCred)

pachmamaCred = {}
try:
    with open(pachmamaCredFile, "r") as f:
        pachmamaCred = json.load(f)
except OSError:
    print("Pachamama Credentials File Read Error")
helper.PrettyPrintJSON(pachmamaCred)

# realityHub.addEvent(eventObj, realityHubCred)
pachamama.addEvent(eventObj, pachmamaCred)

