import json
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def ClearAndAddElement(driver, elementID, textValue):
    elementObj = driver.find_element_by_id(elementID)
    elementObj.clear()
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
