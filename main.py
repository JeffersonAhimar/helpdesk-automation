import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from scripts import scriptChangeTicketStatus

load_dotenv('.env')
URL = os.getenv('URL_HELP_DESK')
USERNAME = os.getenv('HD_USERNAME')
PASSWORD = os.getenv('HD_PASSWORD')
print(USERNAME)
print(PASSWORD)


driver = webdriver.Chrome()
driver.get(URL)

driverWait = WebDriverWait(driver, 5)


def login():
    # USERNAME
    username = driverWait.until(EC.presence_of_element_located((By.ID, "username")))
    username.send_keys(USERNAME)
    # PASSWORD
    password = driverWait.until(EC.presence_of_element_located((By.ID, "password")))
    password.send_keys(PASSWORD)
    # SELECT COMPANY
    logOnToElement = driverWait.until(EC.presence_of_element_located((By.NAME, "domain")))
    logOnToSelect = Select(logOnToElement)
    logOnToSelect.select_by_value("8")
    # LOGIN CLICK
    loginBtn = driverWait.until(EC.presence_of_element_located((By.NAME, "loginButton")))
    loginBtn.click()


def openRequest():
    requestsBtn = driverWait.until(EC.presence_of_element_located((By.ID, "Requests")))
    requestsBtn.click()


def openAdvanceSearch():
    advanceSearchBtn = driverWait.until(EC.presence_of_element_located((By.ID, "advsearchlink")))
    advanceSearchBtn.click()


def openSubjectByTicketId(ticketId):
    textHref = f"//a[@href='WorkOrder.do?woMode=viewWO&woID={ticketId}&&fromListView=true&fromAdvSearch=true']"
    try:
        subjectBtn = driverWait.until(EC.presence_of_element_located((By.XPATH, textHref)))
        subjectBtn.click()
    except TimeoutException:
        goToNextPage(25,2)
        try:
            subjectBtn = driverWait.until(EC.presence_of_element_located((By.XPATH, textHref)))
            subjectBtn.click()
        except TimeoutException:
            goToNextPage(50,3)
            try:
                subjectBtn = driverWait.until(EC.presence_of_element_located((By.XPATH, textHref)))
                subjectBtn.click()
            except TimeoutException:
                print("No se encontró en la página 2 ni en la 3")


def goToNextPage(offset,page):
    txt_script = f"""
    showRange('RequestsView', '{offset+1}','{page}')
    """
    driver.execute_script(txt_script)


def openEditForm():
    editBtn = driverWait.until(EC.presence_of_element_located((By.ID, "Req_Det_Edit")))
    editBtn.click()

def run():
    try:
        login()

        ticketsList = [
            112404,112476
        ]

        for ticket in ticketsList:
            print(f"Searching ticket # {ticket}")
            openRequest()
            openAdvanceSearch()
            openSubjectByTicketId(ticket)
            openEditForm()
            print(f"Editing status of ticket # {ticket} \n")
            time.sleep(1) # seconds
            # driver.execute_script(scriptChangeTicketStatus())

    except:
        print("Unknown error")
    finally:
        print(f"Tickets changed: {ticketsList}")
        time.sleep(5) # seconds
        driver.quit()


if __name__ == '__main__':
    run()
