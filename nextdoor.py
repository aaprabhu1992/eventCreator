import helper
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

NEXTDOOR_TIMEOUT = 10
def Scroll(distance, occurence):
    for i in range(0,occurence):
        pyautogui.scroll(distance)

def basicPage(driver, eventObj):
    neighborText = "Choose neighbors"
    helper.ClickElementFromTagAndText(driver, "span", neighborText)
    helper.PauseForEffect(1)
    #Summer Lake + Nearby
    if eventObj["neighborType"] == "Summer Lake":
        helper.ClickElementFromTagAndText(driver, "label", eventObj["neighborType"], True)
    else:
        helper.ClickElementFromTagAndText(driver, "label", eventObj["neighborType"], True)
        helper.ClickElementFromTagAndText(driver, "button", "Next")
        
    neighborText = "Choose category"
    helper.ClickElementFromTagAndText(driver, "span", neighborText)
    helper.PauseForEffect(1)
    #Classes
    helper.ClickElementFromTagAndText(driver, "label", eventObj["categoryType"])

    driver.find_element_by_xpath('//input[@data-testid="event-form-subject"]').send_keys(eventObj["title"])
    driver.find_element_by_xpath('//textarea[@data-testid="event-form-body"]').send_keys(eventObj["description"])
    driver.find_element_by_xpath('//button[@data-testid="event-form-next-button"]').click()

def detailsPage(driver, eventObj, eventBriteLink):
    # Event Details
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    
    helper.PauseForEffect(1)
    pyautogui.write(eventObj["start_date"])
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    helper.PauseForEffect(2)
    pyautogui.write(eventObj["start_time"], interval = 0.1)
    print(eventObj["start_time"])
    helper.PauseForEffect(2)
    pyautogui.press(["tab"])
    helper.PauseForEffect(1)
    pyautogui.press(["enter"])
    
    helper.PauseForEffect(1)

    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])

    
    helper.PauseForEffect(1)
    pyautogui.write(eventObj["end_date"])
    pyautogui.press(["tab"])
    helper.PauseForEffect(2)
    pyautogui.write(eventObj["end_time"], interval = 0.1)
    print(eventObj["end_time"])
    helper.PauseForEffect(2)
        
    # Event Location
    eventLocation = eventObj["website"]
    if eventBriteLink:
        eventLocation = eventBriteLink
    driver.find_element_by_xpath('//input[@class="postbox-field-text-input pac-target-input"]').send_keys(eventLocation)

    driver.find_element_by_xpath('//input[@class="postbox-event-checkbox"]').click()
    
    driver.find_element_by_xpath('//button[@data-testid="button-detail"]').click()

def addEvent(eventObj, credentials, eventBriteLink):    
    options = webdriver.ChromeOptions();
    options.add_argument("--profile-directory=Default");
    options.add_argument("--whitelisted-ips");
    options.add_argument("--start-maximized");
    options.add_argument("--disable-extensions");
    options.add_argument("--disable-plugins-discovery");
    
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get("https://nextdoor.com/")
    
    helper.PauseForEffect(NEXTDOOR_TIMEOUT)
    # Create an Event
    loginText = "Log in"
    helper.ClickElementFromTagAndText(driver, "button", loginText)

    
    
    signInButtonID = "signin_button"
    if not helper.HasPageLoadedIDCheck(driver, NEXTDOOR_TIMEOUT, signInButtonID):
        print("Page has not loaded in time")
        return
    emailFieldID = "id_email"
    passwordFieldID = "id_password"
    driver.find_element_by_id(emailFieldID).send_keys(credentials["username"])
    driver.find_element_by_id(passwordFieldID).send_keys(credentials["password"])
    pyautogui.press(["enter"])
    
    
    helper.PauseForEffect(NEXTDOOR_TIMEOUT)
    
    # Create an Event
    eventsLinkText = "Events"
    helper.ClickElementFromTagAndText(driver, "span", eventsLinkText)
        
    helper.PauseForEffect(1)
    
    
    addEventID = "main_content"
    if not helper.HasPageLoadedIDCheck(driver, NEXTDOOR_TIMEOUT, addEventID):
        print("Page has not loaded in time")
        return
    driver.find_element_by_id(addEventID).click()
        
    helper.PauseForEffect(NEXTDOOR_TIMEOUT)
    
    basicPage(driver, eventObj)
    helper.PauseForEffect(NEXTDOOR_TIMEOUT)
    
    
    
    detailsPage(driver, eventObj, eventBriteLink)
    helper.PauseForEffect(NEXTDOOR_TIMEOUT)

    
    # add Image
    if "image" in eventObj:
        print(eventObj["image"])
        action = ActionChains(driver)
        imageButton = driver.find_element_by_xpath('//input[@class="uploader-fileinput"]')
        action.click(on_element = imageButton)
        action.perform()
        helper.PauseForEffect(1)
        pyautogui.write(eventObj["image"], interval = 0.1)
        pyautogui.press(["enter"])

    helper.PauseForEffect(NEXTDOOR_TIMEOUT)
    # # Post the Image
    # driver.find_element_by_xpath('//button[@data-testid="button-photo"]').click()
    
    
    driver.close()