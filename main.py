import sys
import json
import argparse

import helper
import realityHub
import pachamama
import signUpGenius
import eventbrite

parser = argparse.ArgumentParser()
parser.add_argument('-fileName',
                    type=str,
                    help='Event JSON')
parser.add_argument('-realityHub',
                    type=str,
                    help='Reality Hub Credential')
parser.add_argument('-signUpGenius',
                    type=str,
                    help='SignUp Genius Hub Credential')
# parser.add_argument('-pachamamaHub',
                    # type=str,
                    # help='Pachamama Hub Credential')
parser.add_argument('-eventbrite',
                   type=str,
                   help='Eventbrite Credentials')
args = parser.parse_args()
fileName = args.fileName
realityHubCredFile = args.realityHub
signUpGeniusCredFile = args.signUpGenius
eventbriteCredFile = args.eventbrite
# pachmamaCredFile = args.pachamamaHub

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

signUpGeniusCred = {}
try:
    with open(signUpGeniusCredFile, "r") as f:
        signUpGeniusCred = json.load(f)
except OSError:
    print("Sign Up Genius File Read Error")
helper.PrettyPrintJSON(signUpGeniusCred)

eventbriteCred = {}
try:
    with open(eventbriteCredFile, "r") as f:
        eventbriteCred = json.load(f)
except OSError:
    print("Eventbrite File Read Error")
helper.PrettyPrintJSON(eventbriteCred)



# if "signUpGenius" in eventObj:
    # signUpGenius.addEvent(eventObj["signUpGenius"], signUpGeniusCred)
if "eventbrite" in eventObj:
    eventbrite.addEvent(eventObj["eventbrite"], eventbriteCred)
# realityHub.addEvent(eventObj, realityHubCred)
# pachamama.addEvent(eventObj, pachmamaCred)

