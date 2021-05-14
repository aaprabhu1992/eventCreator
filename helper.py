import json
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


    
def ClearAndAddElement(driver, elementID, textValue):
    elementObj = driver.find_element_by_id(elementID)
    elementObj.clear()
    elementObj.send_keys(textValue)

def ClearAndAddElement_Input(driver, elementID, textValue):
    elementObj = driver.find_element_by_id(elementID)
    elementObj.send_keys(Keys.CONTROL + "a")
    elementObj.send_keys(Keys.DELETE)
    elementObj.send_keys(textValue)
def PrettyPrintJSON(jsonObj, jsonIndent = 3):
    print(json.dumps(jsonObj, indent = jsonIndent))


def PauseForEffect(inputTime):
    time.sleep(inputTime)


def HasPageLoadedIDCheck(driver, timeout, elementID):
    try:
        element_present = EC.presence_of_element_located((By.ID, elementID))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        return False

def HasPageLoadedLinkCheck(driver, timeout, linkText):
    try:
        element_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, linkText))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        return False


def HasPageLoadedClassCheck(driver, timeout, className):
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, className))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        return False


def ClickElementFromTagAndText(driver, tagName, displayText, printText = False):
    allItems = driver.find_elements_by_tag_name(tagName)
    for item in allItems:
        if item.text == displayText:
            item.click()
            print("Element found, Tag: {}, Name: {}".format(tagName, displayText))
            return
        else:
            if printText:
                print(item.text)
    print("No Element found, Tag: {}, Name: {}".format(tagName, displayText))


def MoveToElement(driver, tagName, displayText):
    allItems = driver.find_elements_by_tag_name(tagName)
    for item in allItems:
        if item.text == displayText:
            actions = ActionChains(driver)
            actions.move_to_element(item).perform()
            break

def GetElementFromTagAndText(driver, tagName, displayText):
    allItems = driver.find_elements_by_tag_name(tagName)
    for item in allItems:
        if item.text == displayText:
            print("Element found, Tag: {}, Name: {}".format(tagName, displayText))
            return item
    print("No Element found, Tag: {}, Name: {}".format(tagName, displayText))

def ReadJSON(jsonFile):
    outputJSON = {}
    try:
        with open(jsonFile, "r") as f:
            outputJSON = json.load(f)
    except OSError:
        print("File Read Error")
    PrettyPrintJSON(outputJSON)
    return outputJSON
