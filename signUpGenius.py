import helper
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

SIGN_UP_GENIUS_TIMEOUT = 10
SMALL_PAUSE = 3
MEDIUM_PAUSE = 5
TAB_COUNT_PUBLISH = 18

def Scroll(distance, occurence):
    for i in range(0,occurence):
        pyautogui.scroll(distance)

def AddBasicInformation(driver, eventObj):
    # Add Basic Information
    helper.ClickElementFromTagAndText(driver, "button", "Create a Sign Up")
    helper.PauseForEffect(SIGN_UP_GENIUS_TIMEOUT)
    titleID = "signuptitle"
    selectGroupID = "selectgroup"
    selectTypeID = "selecttype"
    categoriesID = "searchCategories"
    if not helper.HasPageLoadedIDCheck(driver, SIGN_UP_GENIUS_TIMEOUT, titleID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(titleID).click()
    pyautogui.write(eventObj["title"])
    select = Select(driver.find_element_by_id(selectGroupID))
    select.select_by_visible_text(eventObj["group"])
    select = Select(driver.find_element_by_id(selectTypeID))
    select.select_by_visible_text(eventObj["type"])
    select = Select(driver.find_element_by_id(categoriesID))
    select.select_by_visible_text(eventObj["categories"])
    Scroll(100, 5)
    saveAndContiueText = "Save and Continue"
    helper.ClickElementFromTagAndText(driver, "span", saveAndContiueText)
    helper.PauseForEffect(SIGN_UP_GENIUS_TIMEOUT)
    return driver.current_url
    
def GetEventID(currentURL):
    #https://www.eventbrite.com/manage/events/152465467317/details
    elements = currentURL.split("/")
    return elements[-3]
    
def AddSlots(driver, eventObj):
    helper.PauseForEffect(MEDIUM_PAUSE)
    helper.ClickElementFromTagAndText(driver, "strong", eventObj["type_schedule"])
    tabQuantity = 0
    if eventObj["type_schedule"] == "Slots Only":
        tabQuantity = 3
        
    for i in range(0, tabQuantity):
        pyautogui.press(["tab"])
    helper.PauseForEffect(SMALL_PAUSE)
    pyautogui.write(eventObj["date"], interval = 0.1)
    print(eventObj["date"])
    helper.PauseForEffect(SMALL_PAUSE)
    pyautogui.press(["enter"])
    helper.PauseForEffect(SMALL_PAUSE)
    all_slots = eventObj["all_slots"]
    lenSlots = len(all_slots)
    pyautogui.press(["tab"])
    pyautogui.press(["space"])
    for i in range(0, lenSlots):
        slot = all_slots[i]
        helper.PauseForEffect(SMALL_PAUSE)
        driver.find_element_by_name("slotname").click()
        pyautogui.write(slot["title"], interval = 0.1)
        pyautogui.press(["tab"])
        pyautogui.write(slot["comment"], interval = 0.1)
        pyautogui.press(["tab"])
        pyautogui.write(slot["quantity"], interval = 0.1)
        pyautogui.press(["tab"])
        helper.PauseForEffect(SMALL_PAUSE)
        if i < (lenSlots - 1):
            pyautogui.press(["tab"])
        pyautogui.press(["tab"])
        pyautogui.press(["enter"])
        helper.PauseForEffect(SMALL_PAUSE)
    
    helper.PauseForEffect(MEDIUM_PAUSE)
    saveAndContiueText = "Save and Continue"
    helper.ClickElementFromTagAndText(driver, "span", saveAndContiueText)
    helper.PauseForEffect(SIGN_UP_GENIUS_TIMEOUT)


def AddSettings(driver, eventObj):
    # No Changes in this region hence small pause sufficient
    helper.PauseForEffect(SMALL_PAUSE)
    saveAndContiueText = "Save and Continue"
    helper.ClickElementFromTagAndText(driver, "span", saveAndContiueText)
    helper.PauseForEffect(SMALL_PAUSE)


def AddPublish(driver, eventObj):
    helper.PauseForEffect(MEDIUM_PAUSE)
    for i in range(0, TAB_COUNT_PUBLISH):
        pyautogui.press(["tab"])
    helper.PauseForEffect(SMALL_PAUSE)    
    pyautogui.press(["space"])
    helper.PauseForEffect(SIGN_UP_GENIUS_TIMEOUT)
    element = driver.find_element_by_partial_link_text("https://www.signupgenius")
    return element.text

    
def addEvent(eventObj, credentials):    
    eventURL = None
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.signupgenius.com/register")
    # Login
    emailFieldID = "email"
    passwordFieldID = "pword"
    loginButtonID = "loginBtnId"
    if not helper.HasPageLoadedIDCheck(driver, SIGN_UP_GENIUS_TIMEOUT, loginButtonID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_partial_link_text("Got it!").click()
    driver.find_element_by_id(emailFieldID).send_keys(credentials["username"])
    driver.find_element_by_id(passwordFieldID).send_keys(credentials["password"])
    driver.find_element_by_id(loginButtonID).send_keys(Keys.ENTER)
    createSignUpClass = "btn btn-green black-shadow-active"
    helper.PauseForEffect(SIGN_UP_GENIUS_TIMEOUT)
    signUpListItemID = "member-sidebar--menu-signupsid"
    if not helper.HasPageLoadedIDCheck(driver, SIGN_UP_GENIUS_TIMEOUT, signUpListItemID):
        print("Page has not loaded in time")
        return eventURL
    # Start with Base
    url = AddBasicInformation(driver, eventObj)
    eventID = GetEventID(url)
    # driver.get("https://www.signupgenius.com/index.cfm?go=w.manageSignUp#/{}/slots/".format(eventID))

    # Other Details
    AddSlots(driver, eventObj)
    AddSettings(driver, eventObj)

    # Publish
    driver.get("https://www.signupgenius.com/index.cfm?go=w.manageSignUp#/{}/publish/".format(eventID))    
    signUpLink = AddPublish(driver, eventObj)
    driver.close()
    print(signUpLink)
    return signUpLink
