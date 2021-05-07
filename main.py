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
parser.add_argument('-eventbrite',
                   type=str,
                   help='Eventbrite Credentials')
parser.add_argument('-pachamama',
                   type=str,
                   help='Pachamama Credentials')
args = parser.parse_args()
fileName = args.fileName
realityHubCredFile = args.realityHub
signUpGeniusCredFile = args.signUpGenius
eventbriteCredFile = args.eventbrite
pachamamaCredFile = args.pachamama

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

pachamamaCred = {}
try:
    with open(pachamamaCredFile, "r") as f:
        pachamamaCred = json.load(f)
except OSError:
    print("Pachamama Credentials File Read Error")
helper.PrettyPrintJSON(pachamamaCred)


signUpGeniusLink = "https://www.signupgenius.com/go/4090e45adaa2cabfb6-climate4"
# if "signUpGenius" in eventObj:
    # signUpGeniusLink = signUpGenius.addEvent(eventObj["signUpGenius"], signUpGeniusCred)
    
# eventbriteLink = ""   
# if "eventbrite" in eventObj:
    # eventbriteLink = eventbrite.addEvent(eventObj["eventbrite"], eventbriteCred, signUpGeniusLink)


# realityHub.addEvent(eventObj, realityHubCred, eventbriteLink)
pachamama.addEvent(eventObj["pachamama"], pachamamaCred, signUpGeniusLink)

