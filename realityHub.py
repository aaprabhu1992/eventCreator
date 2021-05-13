import helper


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

REALITY_HUB_TIMEOUT = 10

def addEvent(eventObj, credentials, eventBriteLink):    
    eventURL = None
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://realityhub.climaterealityproject.org/home")
    # Page Load
    loginButtonID = "headerLogLink"
    if not helper.HasPageLoadedIDCheck(driver, REALITY_HUB_TIMEOUT, loginButtonID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(loginButtonID).send_keys(Keys.ENTER)
    # Login
    emailFieldID = "email"
    passwordFieldID = "password"
    loginButtonID = "main_login_button"
    if not helper.HasPageLoadedIDCheck(driver, REALITY_HUB_TIMEOUT, emailFieldID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(emailFieldID).send_keys(credentials["username"])
    driver.find_element_by_id(passwordFieldID).send_keys(credentials["password"])
    driver.find_element_by_id(loginButtonID).send_keys(Keys.ENTER)
    # Go to Events
    actBarID = "navbarDropdown_1"
    attendEventText = "Attend an Event"
    if not helper.HasPageLoadedIDCheck(driver, REALITY_HUB_TIMEOUT, actBarID):
        print("Page has not loaded in time")
        return eventURL
    action = ActionChains(driver)
    actBar = driver.find_element_by_id(actBarID)
    action.click(on_element = actBar)
    action.perform()
    # Need to see it on the screen before you click
    helper.PauseForEffect(1)
    
    # Need to create a new chain every time
    action = ActionChains(driver)    
    attendEventLink = driver.find_element_by_partial_link_text(attendEventText)
    action.click(on_element = attendEventLink)
    action.perform()

    postAnEventID = "html_custom_block_0_0_button"
    if not helper.HasPageLoadedIDCheck(driver, REALITY_HUB_TIMEOUT, postAnEventID):
        print("Page has not loaded in time")
        return eventURL
    driver.find_element_by_id(postAnEventID).send_keys(Keys.ENTER)
    # Fill Event details
    eventNameID = "textField_event_name"
    startDateID = "dateTime_event_start"
    startTimeID = "dateTime_event_start_time"
    endDateID = "dateTime_event_end"
    endTimeID = "dateTime_event_end_time"
    timeZoneClass = "time-zone-link btn btn-primary"
    timeZoneCountryID = "time_zone_country_select"
    timeZoneCityID = "time_zone_city_select"
    eventVenueID = "textField_event_venue"
    addrLine1ID = "Address_event_address_address_1_input"
    addrLine2ID = "Address_event_address_address_2_input"
    cityID = "Address_event_address_address_city_input"
    stateID = "Address_event_address_state_text"
    postCodeID = "Address_event_address_address_postal_code_input"
    countryID = "Address_event_address_country_select"
    eventTypeID = "dropDown_3031"
    hostNameID = "textField_2818"
    hostEmailID = "textField_2820"
    hostGroupID = "textField_3335"
    eventWebsiteID = "link_3336"
    submitEventID = "events_item_form_button"
    if not helper.HasPageLoadedIDCheck(driver, REALITY_HUB_TIMEOUT, eventNameID):
        print("Page has not loaded in time")
        return eventURL
    
    # Basic 
    driver.find_element_by_id(eventNameID).send_keys(eventObj["name"])
    helper.PauseForEffect(REALITY_HUB_TIMEOUT)
    driver.switch_to_frame(0)
    driver.find_element_by_xpath('html/body').send_keys(eventObj["description"])
    driver.switch_to_default_content()
    print("Basic Data Added")

    # Time
    helper.ClearAndAddElement(driver, startDateID, eventObj["start_date"])
    helper.ClearAndAddElement(driver, startTimeID, eventObj["start_time"])
    helper.ClearAndAddElement(driver, endDateID, eventObj["end_date"])
    helper.ClearAndAddElement(driver, endTimeID, eventObj["end_time"])
    
    attendEventLink = driver.find_element_by_partial_link_text("NEW YORK").click()
    helper.PauseForEffect(REALITY_HUB_TIMEOUT)
    select = Select(driver.find_element_by_id(timeZoneCountryID))
    select.select_by_visible_text(eventObj["timeZone_Country"])
    select = Select(driver.find_element_by_id(timeZoneCityID))
    select.select_by_visible_text(eventObj["timeZone_Time"])
    
    print("Time Data Added")
    
    
    # Address 
    driver.find_element_by_id(eventVenueID).send_keys(eventObj["venue"])
    driver.find_element_by_id(addrLine1ID).send_keys(eventObj["addr_line_1"])
    driver.find_element_by_id(addrLine2ID).send_keys(eventObj["addr_line_2"])
    driver.find_element_by_id(cityID).send_keys(eventObj["addr_city"])
    driver.find_element_by_id(stateID).send_keys(eventObj["addr_state"])
    driver.find_element_by_id(postCodeID).send_keys(eventObj["addr_pincode"])
    select = Select(driver.find_element_by_id(countryID))
    select.select_by_visible_text(eventObj["addr_country"])
    print("Address Data Added")

    # Event Type
    select = Select(driver.find_element_by_id(eventTypeID))
    select.select_by_visible_text(eventObj["type"])
    driver.find_element_by_id(hostNameID).send_keys(eventObj["hostName"])
    driver.find_element_by_id(hostEmailID).send_keys(eventObj["hostEmail"])
    driver.find_element_by_id(hostGroupID).send_keys(eventObj["hostOrg"])
    if eventBriteLink:
        eventObj["website"] = eventBriteLink
    element = driver.find_element_by_id(eventWebsiteID)
    element.clear()
    element.send_keys(eventObj["website"])
    

    # Submit
    helper.PauseForEffect(REALITY_HUB_TIMEOUT)
    driver.find_element_by_id(submitEventID).click()
    
    #Ensure event has been completed
    completeButtonID = "send_event_message_button_events_event_message_0_9"
    if not helper.HasPageLoadedIDCheck(driver, REALITY_HUB_TIMEOUT + 30, completeButtonID):
        print("Page has not loaded in time")
        eventURL = "Event not Created"
    else:
        eventURL = driver.current_url
    driver.close()
    return eventURL
