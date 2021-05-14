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


def addEvent(eventObj, credentials, eventBriteLink):    
    options = webdriver.ChromeOptions();
    options.add_argument("--profile-directory=Default");
    options.add_argument("--whitelisted-ips");
    options.add_argument("--start-maximized");
    options.add_argument("--disable-extensions");
    options.add_argument("--disable-plugins-discovery");
    
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get("https://nextdoor.com/login/")
    signInButtonID = "signin_button"
    if not helper.HasPageLoadedIDCheck(driver, NEXTDOOR_TIMEOUT, signInButtonID):
        print("Page has not loaded in time")
        return
    emailFieldID = "id_email"
    passwordFieldID = "id_password"addEvent
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
    
    neighborText = "Choose neighbors"
    helper.ClickElementFromTagAndText(driver, "span", neighborText)
    helper.PauseForEffect(1)
    #Summer Lake + Nearby
    helper.ClickElementFromTagAndText(driver, "span", eventObj["neighborType"])
    
    neighborText = "Choose category"
    helper.ClickElementFromTagAndText(driver, "span", neighborText)
    helper.PauseForEffect(1)
    #Classes
    helper.ClickElementFromTagAndText(driver, "span", eventObj["categoryType"])


    driver.find_element_by_xpath('//input[@data-testid="event-form-subject"]').send_keys(eventObj["title"])
    driver.find_element_by_xpath('//textarea[@data-testid="event-form-body"]').send_keys(eventObj["description"])
    driver.find_element_by_xpath('//button[@data-testid="event-form-next-button"]').click()
    
    helper.PauseForEffect(NEXTDOOR_TIMEOUT)
    driver.close()