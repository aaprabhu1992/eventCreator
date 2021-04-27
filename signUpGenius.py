import helper


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

SIGN_UP_GENIUS_TIMEOUT = 10

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
    driver.find_element_by_id(emailFieldID).send_keys(credentials["username"])
    driver.find_element_by_id(passwordFieldID).send_keys(credentials["password"])
    driver.find_element_by_id(loginButtonID).send_keys(Keys.ENTER)
    createSignUpClass = "btn btn-green black-shadow-active"
    helper.PauseForEffect(SIGN_UP_GENIUS_TIMEOUT)
    signUpListItemID = "member-sidebar--menu-signupsid"
    if not helper.HasPageLoadedIDCheck(driver, SIGN_UP_GENIUS_TIMEOUT, signUpListItemID):
        print("Page has not loaded in time")
        return eventURL
    
    # Create a new Item
    allButtons = driver.find_elements_by_tag_name("button")
    for button in allButtons:
        if button.text == "Create a Sign Up":
            button.click()
            break
            
    titleID = "signuptitle"
    selectGroupID = "selectgroup"
    selectTypeID = "selecttype"
    categoriesID = "searchCategories"
    if not helper.HasPageLoadedIDCheck(driver, SIGN_UP_GENIUS_TIMEOUT, titleID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(titleID).send_keys(eventObj["title"])
    select = Select(driver.find_element_by_id(selectGroupID))
    select.select_by_visible_text(eventObj["group"])
    select = Select(driver.find_element_by_id(selectTypeID))
    select.select_by_visible_text(eventObj["type"])
    select = Select(driver.find_element_by_id(categoriesID))
    select.select_by_visible_text(eventObj["categories"])
    saveAndContiueText = "Save and Continue"
    allButtons = driver.find_elements_by_tag_name("span")
    for button in allButtons:
        if button.text == saveAndContiueText:
            button.click()
            break
    

