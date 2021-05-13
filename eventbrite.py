import helper
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

EVENTBRITE_TIMEOUT = 10
SMALL_PAUSE = 2
MAX_TAGS = 10
def Scroll(distance, occurence):
    for i in range(0,occurence):
        pyautogui.scroll(distance)

def CreateBasicInfo(driver, eventObj):
    titleID = "event-basicInfo-title"
    if not helper.HasPageLoadedIDCheck(driver, EVENTBRITE_TIMEOUT, titleID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(titleID).send_keys(eventObj["title"])
    selectID = "event-basicinfo-organizer-profile"
    eventTypeName = "eventType"
    eventTopicName = "eventTopic"
    eventSubTopicName =  "eventSubTopic"
    tagFieldName  = "tagInputField"
    select = Select(driver.find_element_by_id(selectID))
    select.select_by_visible_text(eventObj["organizer"])
    select = Select(driver.find_element_by_name(eventTypeName))
    select.select_by_visible_text(eventObj["type"])
    select = Select(driver.find_element_by_name(eventTopicName))
    select.select_by_visible_text(eventObj["topic"])
    helper.PauseForEffect(SMALL_PAUSE)
    select = Select(driver.find_element_by_name(eventSubTopicName))
    select.select_by_visible_text(eventObj["subTopic"])
    fieldValue = driver.find_element_by_name(tagFieldName)
    allTags = eventObj["tags"]
    allTags = (allTags, allTags[0:MAX_TAGS])[len(allTags) > MAX_TAGS]

    for tag in allTags:
        fieldValue.send_keys(tag)
        pyautogui.press("enter")
    helper.PauseForEffect(SMALL_PAUSE)

    Scroll(-100, 5)
    print("Scroll Completed")
    locationDetails = eventObj["location"]
    helper.ClickElementFromTagAndText(driver, "div", "Online event")
    print("Completd DIV try")
    # if locationDetails["type"] == "Venue":
        # driver.find_element_by_id("segmented-venueType-0").click()
    # if locationDetails["type"] == "Online event":
        # driver.find_element_by_id("segmented-venueType-1").click()
    # if locationDetails["type"] == "To be announced":
        # driver.find_element_by_id("segmented-venueType-2").click()
    # print("Completd Radio Try")
    
    Scroll(-100, 5)

    dateAndTime = eventObj["dateAndTime"]
    helper.MoveToElement(driver, "div", "Single Event")
    helper.ClickElementFromTagAndText(driver, "div", "Single Event")
    if dateAndTime["type"] == "Single Event":
        startDateID = "event-startDate"
        startTimeID = "event-startTime"
        endDateID = "event-endDate"
        endTimeID = "event-endTime"
        helper.ClearAndAddElement_Input(driver, startDateID, dateAndTime["start_date"])
        helper.ClearAndAddElement_Input(driver, startTimeID, dateAndTime["start_time"])
        helper.ClearAndAddElement_Input(driver, endDateID, dateAndTime["end_date"])
        helper.ClearAndAddElement_Input(driver, endTimeID, dateAndTime["end_time"])

    selectZoneName = "venueTimeZone"
    select = Select(driver.find_element_by_name(selectZoneName))
    select.select_by_visible_text(dateAndTime["zone"])
    
    helper.ClickElementFromTagAndText(driver, "button", "Save & Continue")
    # 
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    return driver.current_url
    
def CreateDetails(driver, eventObj, signUpGeniusLink):
    eventURL = None
    summaryID = "event-design-summary"
    if not helper.HasPageLoadedIDCheck(driver, EVENTBRITE_TIMEOUT, summaryID):
        print("Page has not loaded in time")
        return eventURL
    # Upload Banner
    uploadImageClass = "eds-uploader-dropzone__cover"
    allImages = driver.find_elements_by_class_name(uploadImageClass)
    allImages[0].click()
    helper.PauseForEffect(SMALL_PAUSE)
    pyautogui.write(eventObj["banner"], interval = 0.1)
    pyautogui.press(["enter"])
    helper.PauseForEffect(SMALL_PAUSE)    
    # Will Always ask for CROP, User has to ensure it is up to size
    pyautogui.press(["tab"])
    pyautogui.press(["enter"])

    # Add text
    richTextBoxClass = "eds-richtexteditor__input"
    driver.find_element_by_id(summaryID).send_keys(eventObj["summary"])
    description = eventObj["description"]
    description = description.replace("$LINK$", signUpGeniusLink)
    driver.find_element_by_class_name(richTextBoxClass).send_keys(description)
    
    
    # Add Chef Image
    if "add" in eventObj:
        allAdds = eventObj["add"]
        for add in allAdds:
            assert "type" in add
            Scroll(-100, 5)
            if add["type"] == "image":
                helper.ClickElementFromTagAndText(driver, "button", "Add Image")
                helper.PauseForEffect(SMALL_PAUSE)
                Scroll(-100, 5)
                allImages = driver.find_elements_by_class_name(uploadImageClass)
                print(len(allImages))
                allImages[0].click()
                helper.PauseForEffect(SMALL_PAUSE)
                pyautogui.write(add["content"], interval = 0.1)
                pyautogui.press(["enter"])
                helper.PauseForEffect(SMALL_PAUSE)
            else:
                print("Other types not yet supported")
    helper.PauseForEffect(SMALL_PAUSE)
    helper.ClickElementFromTagAndText(driver, "button", "Save")
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)

def CreateOnlinePage(driver, eventObj):
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    if "video" in eventObj:
        Scroll(-100, 5)
        helper.ClickElementFromTagAndText(driver, "span", "Add video")
        Scroll(100, 5)
        videoLinkID = "video-url-0"
        driver.find_element_by_id(videoLinkID).send_keys(eventObj["video"])
    if "link" in eventObj:
        Scroll(-100, 5)
        helper.ClickElementFromTagAndText(driver, "span", "Add link")
        Scroll(100, 5)
        linkTitleID = "file-name-0"
        linkLinkID = "file-url-0"
        driver.find_element_by_id(linkTitleID).send_keys(eventObj["link"]["title"])
        driver.find_element_by_id(linkLinkID).send_keys(eventObj["link"]["link"])
    helper.ClickElementFromTagAndText(driver, "button", "Save")
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    

def CreateTickets(driver, eventObj):
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    if eventObj["type"] == "Free":
        helper.ClickElementFromTagAndText(driver, "div", "Free")
        quantityID = "ticket-quantity"
        driver.find_element_by_id(quantityID).send_keys(eventObj["amount"])
    else:
        print("Other Types not supported")
    helper.ClickElementFromTagAndText(driver, "button", "Save")
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
 

def CreateOrderConfirmation(driver, eventObj, signUpGeniusLink):
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    textBoxName = "group-order_confirmation-confirmation_page_message"
    confirm = eventObj["confirm"]
    confirm = confirm.replace("$LINK$", signUpGeniusLink)
    driver.find_element_by_name(textBoxName).send_keys(confirm)
    Scroll(-100, 10)
    emailBoxID = "tinymce"
    driver.switch_to_frame(0)
    email = eventObj["email"]
    email = confirm.replace("$LINK$", signUpGeniusLink)
    driver.find_element_by_xpath('html/body').send_keys(email)
    driver.switch_to_default_content()
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    pyautogui.press(["tab"])
    pyautogui.press(["enter"])
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
 
def CheckIfURLCreated(url):
    if currentURL != "":
        print("Basic Info page not created,Exiting")
        exit(1)
def CreatePublish(driver, eventObj):
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    helper.ClickElementFromTagAndText(driver, "button", "Publish")

    helper.PauseForEffect(EVENTBRITE_TIMEOUT)


def CreateEmailInvitations(driver, eventObj):
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    helper.ClickElementFromTagAndText(driver, "button", "Create Classic Invite")
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    # Add Guests
    driver.find_element_by_partial_link_text("+ Add Guests").click()
    guestsType = eventObj["add_guests"]
    helper.PauseForEffect(SMALL_PAUSE)
    if guestsType["type"] == "previous":
        driver.find_element_by_id("c").click()
        helper.PauseForEffect(SMALL_PAUSE)
        driver.set_window_size(1000, 1000)
        driver.maximize_window()
        element = driver.find_element_by_id(guestsType["eventID"])
        driver.execute_script('return arguments[0].scrollIntoView();', element)
        element.click()
    else:
        print("Other Guetst Add type not supported")
    helper.PauseForEffect(SMALL_PAUSE)
    addID = "lightbox_a_save_button"
    driver.find_element_by_id(addID).click() 
    # Add Schedule
    email_time = eventObj["email_time"]
    if email_time["type"] == "schedule":        
        whenName = "schedule_mode_x"
        driver.find_element_by_name(whenName).click()
        dateID = "schedule_date"
        helper.ClearAndAddElement_Input(driver, dateID, email_time["date"])
        hourID = "endhr"
        minutesID = "endmin"
        ampmID = "endampm"
        select = Select(driver.find_element_by_id(hourID))
        select.select_by_visible_text(email_time["hour"])
        select = Select(driver.find_element_by_id(minutesID))
        select.select_by_visible_text(email_time["min"])
        select = Select(driver.find_element_by_id(ampmID))
        select.select_by_visible_text(email_time["ampm"])
    else:
        print("Other Schedule types not supported")
    helper.PauseForEffect(SMALL_PAUSE)
    driver.find_element_by_partial_link_text("Save & Schedule").click()            
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
def GetEventURL(driver):
    eventURLID = "event_url"
    element = driver.find_element_by_id(eventURLID)
    print(element)
    linkURL = element.text
    return linkURL[:linkURL.find("?")]
def GetEventID(currentURL):
    #https://www.eventbrite.com/manage/events/152465467317/details
    elements = currentURL.split("/")
    return elements[-2]
def addEvent(eventObj, credentials, signUpGeniusLink):    
    eventURL = None
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.eventbrite.com/signin/")
    # Username
    emailFieldID = "email"
    if not helper.HasPageLoadedIDCheck(driver, EVENTBRITE_TIMEOUT, emailFieldID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(emailFieldID).send_keys(credentials["username"])
    pyautogui.press(["enter"])
    # Password
    passwordFieldID = "password"
    if not helper.HasPageLoadedIDCheck(driver, EVENTBRITE_TIMEOUT, passwordFieldID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(passwordFieldID).send_keys(credentials["password"])
    pyautogui.press(["enter"])
    
    helper.PauseForEffect(EVENTBRITE_TIMEOUT)
    # Create a new Event
    helper.ClickElementFromTagAndText(driver, "a", "Create Event")
    currentURL = CreateBasicInfo(driver, eventObj["basic_info"])
    eventID = GetEventID(currentURL)
    print("Event ID is {}".format(eventID))

    driver.get(currentURL)
    CreateDetails(driver, eventObj["details"], signUpGeniusLink)

    driver.get("https://www.eventbrite.com/manage/events/{}/online-event".format(eventID))
    CreateOnlinePage(driver, eventObj["online_page"])

    driver.get("https://www.eventbrite.com/manage/events/{}/tickets/create".format(eventID))
    CreateTickets(driver, eventObj["tickets"])
    
    driver.get("https://www.eventbrite.com/myevent/{}/order-confirmation/".format(eventID))
    CreateOrderConfirmation(driver, eventObj["order_confirmation"], signUpGeniusLink)

    driver.get("https://www.eventbrite.com/manage/events/{}/preview_publish".format(eventID))
    CreatePublish(driver, eventObj["publish"])
    
    driver.get("https://www.eventbrite.com/invites?eid={}".format(eventID))
    CreateEmailInvitations(driver, eventObj["invitations"])
    
    driver.get("https://www.eventbrite.com/myevent?eid={}".format(eventID))
    url =  GetEventURL(driver)
    print(url)
    driver.close()
    return url
