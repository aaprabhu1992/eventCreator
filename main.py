import sys
import json
import argparse

import helper
import realityHub
import pachamama
import signUpGenius
import eventbrite
import nextdoor

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
parser.add_argument('-nextdoor',
                   type=str,
                   help='NextDoor Credentials')
                   

# Read all arguments
args = parser.parse_args()
fileName = args.fileName
realityHubCredFile = args.realityHub
signUpGeniusCredFile = args.signUpGenius
eventbriteCredFile = args.eventbrite
pachamamaCredFile = args.pachamama
nextdoorCredFile = args.nextdoor



# Read all the Input files
eventObj = helper.ReadJSON(fileName)
realityHubCred = helper.ReadJSON(realityHubCredFile)
signUpGeniusCred = helper.ReadJSON(signUpGeniusCredFile)
eventbriteCred = helper.ReadJSON(eventbriteCredFile)
pachamamaCred = helper.ReadJSON(pachamamaCredFile)
nextdoorCred = helper.ReadJSON(nextdoorCredFile)


signUpGeniusLink = ""
if "signUpGenius" in eventObj:
    signUpGeniusLink = signUpGenius.addEvent(eventObj["signUpGenius"], signUpGeniusCred)
    
eventbriteLink = "https://www.eventbrite.com/e/cook-and-serve-vegan-enchiladas-w-chef-emily-forbes-tickets-154013868627"   
if "eventbrite" in eventObj:
    eventbriteLink = eventbrite.addEvent(eventObj["eventbrite"], eventbriteCred, signUpGeniusLink)



if "realityHub" in eventObj:
    realityHub.addEvent(eventObj["realityHub"], realityHubCred, eventbriteLink)
if "pachamama" in eventObj:
    pachamama.addEvent(eventObj["pachamama"], pachamamaCred, signUpGeniusLink)
if "nextdoor" in eventObj:
    nextdoor.addEvent(eventObj["nextdoor"], nextdoorCred, eventbriteLink)

