import helper
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

PACHAMAMA_TIMEOUT = 10
def Scroll(distance, occurence):
    for i in range(0,occurence):
        pyautogui.scroll(distance)


def addEvent(eventObj, credentials, signUpGeniusLink):    
    options = webdriver.ChromeOptions();
    options.add_argument("--profile-directory=Default");
    options.add_argument("--whitelisted-ips");
    options.add_argument("--start-maximized");
    options.add_argument("--disable-extensions");
    options.add_argument("--disable-plugins-discovery");

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Default")
    
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get("https://connect.pachamama.org/user/login")
    signInButtonID = "edit-submit"
    if not helper.HasPageLoadedIDCheck(driver, PACHAMAMA_TIMEOUT, signInButtonID):
        print("Page has not loaded in time")
        return
    emailFieldID = "edit-name-or-mail"
    passwordFieldID = "edit-pass"
    driver.find_element_by_id(emailFieldID).send_keys(credentials["username"])
    driver.find_element_by_id(passwordFieldID).send_keys(credentials["password"])
    pyautogui.press(["enter"])
    
    
    helper.PauseForEffect(PACHAMAMA_TIMEOUT)
    
    # Create an Event
    eventsLinkText = "Events"
    # Need to create a new chain every time
    action = ActionChains(driver)    
    attendEventLink = driver.find_element_by_partial_link_text(eventsLinkText)
    action.click(on_element = attendEventLink)
    action.perform()
    
    helper.PauseForEffect(1)
    
    createEventTextLink = "Create Event"
    action = ActionChains(driver)    
    attendEventLink = driver.find_element_by_partial_link_text(createEventTextLink)
    action.click(on_element = attendEventLink)
    action.perform()
    
    helper.PauseForEffect(PACHAMAMA_TIMEOUT)
    
    
    saveButtonID = "edit-submit"
    if not helper.HasPageLoadedIDCheck(driver, PACHAMAMA_TIMEOUT, saveButtonID):
        print("Page has not loaded in time")
        return

    # Event Details
    helper.ClickElementFromTagAndText(driver, "label", eventObj["type"])
    titleID = "edit-title-0-value"
    driver.find_element_by_id(titleID).send_keys(eventObj["title"])
    if  "image" in eventObj:
        pyautogui.press(["tab"])
        pyautogui.press(["enter"])
        helper.PauseForEffect(3)
        pyautogui.write(eventObj["image"], interval = 0.1)
        pyautogui.press(["enter"])
        helper.PauseForEffect(PACHAMAMA_TIMEOUT)
        Scroll(-100, 2)
        helper.ClickElementFromTagAndText(driver, "div","Small")
    
    groupTypeID = "edit-groups"
    select = Select(driver.find_element_by_id(groupTypeID))
    select.select_by_visible_text(eventObj["group"])
    
    helper.PauseForEffect(3)
    # Date and Time
    eventStartDate = "edit-field-event-date-0-value-date"
    eventEndDate = "edit-field-event-date-end-0-value-date"
    eventStartTime = "edit-field-event-date-0-value-time"
    eventEndTime = "edit-field-event-date-end-0-value-time"
    driver.find_element_by_id(eventStartDate).send_keys(eventObj["start_date"])
    element = driver.find_element_by_id(eventStartTime)
    element.clear()
    element.send_keys(eventObj["start_time"])
    
    element = driver.find_element_by_id(eventEndDate)
    element.clear()
    element.send_keys(eventObj["end_date"])     
    element = driver.find_element_by_id(eventEndTime)
    element.clear()
    element.send_keys(eventObj["end_time"])
    
    
    
    # Location
    locationID = "edit-field-event-location-0-value"
    driver.find_element_by_id(locationID).send_keys(eventObj["location"])
    countryID = "edit-field-event-address-0-address-country-code--2"

    groupTypeID = "edit-groups"
    select = Select(driver.find_element_by_id(countryID))
    select.select_by_visible_text(eventObj["country"])
    
    
    helper.PauseForEffect(3)
    
    # Description
    driver.switch_to_frame(1)
    description = eventObj["description"]
    description = description.replace("$LINK$", signUpGeniusLink)
    driver.find_element_by_xpath('html/body').send_keys(description)
    driver.switch_to_default_content()

    helper.PauseForEffect(3)

    
    # Save
    helper.PauseForEffect(PACHAMAMA_TIMEOUT)
    
    driver.find_element_by_id(saveButtonID).send_keys(Keys.ENTER)
    
    helper.PauseForEffect(PACHAMAMA_TIMEOUT)
    driver.close()