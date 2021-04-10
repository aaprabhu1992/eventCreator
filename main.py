import sys
import json
import argparse

import helper
import realityHub
parser = argparse.ArgumentParser()
parser.add_argument('-fileName',
                    type=str,
                    help='Event JSON')
parser.add_argument('-realityHub',
                    type=str,
                    help='Reality Hub Credential')
##parser.add_argument('-eventbrite',
##                    type=str,
##                    help='Eventbrite Credentials')
##parser.add_argument('-pachamama',
##                    type=str,
##                    help='Pachamama Credentials')
args = parser.parse_args()
fileName = args.fileName
realityHubCredFile = args.realityHub
##eventbriteCred = args.eventbrite
##pachmamaCred = args.pachamama

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
realityHub.addEvent(eventObj, realityHubCred)

