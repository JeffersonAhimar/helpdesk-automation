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

driver = webdriver.Chrome()
driver.get(URL)

driverWait = WebDriverWait(driver, 2)


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
        print("✔️ Ticket found!")
        subjectBtn.click()
    except TimeoutException:
        goToNextPage(25,2)
        try:
            subjectBtn = driverWait.until(EC.presence_of_element_located((By.XPATH, textHref)))
            print("✔️ Ticket found!")
            subjectBtn.click()
        except TimeoutException:
            goToNextPage(50,3)
            try:
                subjectBtn = driverWait.until(EC.presence_of_element_located((By.XPATH, textHref)))
                print("✔️ Ticket found!")
                subjectBtn.click()
            except TimeoutException:
                print("❌ Ticket wasn't found!")


def goToNextPage(offset,page):
    txt_script = f"""
    showRange('RequestsView', '{offset+1}','{page}')
    """
    driver.execute_script(txt_script)
    print(f"...Searching on next page -> {page}")


def openEditForm():
    editBtn = driverWait.until(EC.presence_of_element_located((By.ID, "Req_Det_Edit")))
    print(f"Opening form to edit status")
    editBtn.click()

def run():

    changedTickets=[]
    unchangedTickets=[]
    ticketsList = [
        111812,112624
    ]

    try:
        login()

        print("*************************************")
        print(f"Requested Tickets: {ticketsList}")
        print(f"# of requested Tickets: {len(ticketsList)}")
        print("*************************************")

        for ticket in ticketsList:
            print("-------------------------------------")
            print(f"Searching ticket # {ticket}")
            openRequest()
            openAdvanceSearch()
            try:
                openSubjectByTicketId(ticket)
                openEditForm()
                print(f"Executing script")
                # driver.execute_script(scriptChangeTicketStatus())
                changedTickets.append(ticket)
            except:
                print("Ticket status wasn't changed")
                unchangedTickets.append(ticket)
            print("------------------------------------- \n")
            time.sleep(1) # seconds

    except:
        print("Unknown error")
    finally:
        print("*************************************")
        print(f"Changed Tickets: {changedTickets}")
        print(f"# of changed Tickets: {len(changedTickets)}")
        print("*************************************")
        print("*************************************")
        print(f"Unchanged tickets: {unchangedTickets}")
        print(f"# of unchanged Tickets: {len(unchangedTickets)}")
        print("*************************************")
        time.sleep(5) # seconds
        driver.quit()


if __name__ == '__main__':
    run()
