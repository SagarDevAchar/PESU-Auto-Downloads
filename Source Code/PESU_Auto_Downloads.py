"""
    Configured for CSE
    Automated Content Download System for www.pesuacademy.com

    Copyright (c) 2020 Sagar Dev Achar
    Under MIT License
    ---------------------------------------------------------
    Completed on:   12 September 2020
                    07:31 PM

    Coded By:   Sagar Dev Achar
    Credits:    Vijay Murugan A S
    ---------------------------------------------------------
    Description:
        Selenium + ChromeDriver based script which simulates
        a user's visit and actions on the PESU Academy
        Student Portal and downloads the Slides and Notes
        for courses CS201 to CS205 to the default Chrome
        download directory
    ---------------------------------------------------------
"""

import time
import sys
import msvcrt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def secure_password_input(prompt=''):
    p_s = ''
    proxy_string = [' '] * 64
    while True:
        sys.stdout.write('\x0D' + prompt + ''.join(proxy_string))
        c = msvcrt.getch()
        if c == b'\r':
            break
        elif c == b'\x08':
            p_s = p_s[:-1]
            proxy_string[len(p_s)] = " "
        else:
            proxy_string[len(p_s)] = "*"
            p_s += c.decode()

    sys.stdout.write('\n')
    return p_s


def download_subject_content(driver, subject_id, content_id):
    id_string = "rowWiseCourseContent_%d" % subject_id
    course = driver.find_element_by_id(id_string)
    course.click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "tab-content")))
    nav_menu = driver.find_element_by_class_name("tab-content").find_element_by_class_name("nav")

    for i in range(1, len(nav_menu.text.split('\n')) + 1):  # Nav Menu Loop (Units)
        tab_content = driver.find_element_by_id("CourseContentId").find_elements_by_class_name("contentlink")
        tab_count = len(tab_content)
        if tab_count > 0:
            tab_content[0].click()

        if i > 1:
            tab_count -= 1

        time.sleep(3)

        for t in range(tab_count):  # Chapters Loop
            print("Unit %d Topic %d downloading..." % (i, t+1), end='')
            tabs = driver.find_element_by_id("courseMaterialContent").find_elements_by_class_name("text-center")
            tabs[content_id].click()

            time.sleep(1)
            PDFs = driver.find_elements_by_class_name("embed-responsive-item")
            for PDF in PDFs:
                try:
                    driver.switch_to.frame(PDF)
                    download_button = driver.find_element_by_id("open-button")
                    download_button.click()
                except Exception as e:
                    pass #print("ERROR : Bullshit Site : " + str(e))

                driver.switch_to.default_content()

            LINKS = driver.find_elements_by_class_name("link-preview")
            for LINK in LINKS:
                try:
                    LINK.click()
                except Exception as e:
                    pass #print("ERROR : Bullshit Site : " + str(e))

            driver.switch_to.default_content()

            time.sleep(1)

            next_content = driver.find_element_by_class_name(
                "coursecontent-navigation-area").find_element_by_class_name("pull-right")
            next_content.click()

            print("\x0DUnit %d Topic %d downloaded!   " % (i, t+1))

            if next_content.text.upper() == "BACK TO UNITS":
                break

            time.sleep(3)

        try:
            time.sleep(3)
            nav_tab = driver.find_element_by_class_name("tab-content").find_element_by_xpath(
                "//*[@id=\"courselistunit\"]/li[%d]/a" % (i + 1))
            nav_tab.click()

            time.sleep(3)
        except Exception:
            break

    time.sleep(3)

    back_link = driver.find_element_by_class_name("back_link")
    back_link.click()

    time.sleep(3)

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('prefs', {"plugins.always_open_pdf_externally": True})
options.add_argument("headless")
chrome = webdriver.Chrome("chromedriver.exe", options=options)
#chrome.minimize_window()
chrome.implicitly_wait(10)

print("\nAutomated Content Download System for www.pesuacademy.com")
print("(C) Sagar Dev Achar")
print("\nDO NOT CLOSE THE AUTOMATED CHROME WINDOW !!!")
print("---------------------------------------------------------")

print("The following credentials will be kept PRIVATE\n")

LS = input("Login via G-Mail [G] or PES Credentials[P] : ").upper()

USERNAME = ""
if LS == "G":
    USERNAME = input("\nG-Mail ID : ")
    PASSWORD = secure_password_input("Password  : ")

    print("\nLogging You In...")

    chrome.get("https://accounts.google.com/o/oauth2/auth/identifier?scope=email&redirect_uri=https%3A%2F%2Fwww.pesuacademy.com%2FAcademy%2FGoogleSignOnAuthorization%2FOAuth2TokenCallback&response_type=code&client_id=1005275274649-dvj7qd0dvgvvv8mloua8p1c2dgkbt1i1.apps.googleusercontent.com&approval_prompt=force&flowName=GeneralOAuthFlow")

    mail_input = chrome.find_element_by_xpath("//input[@type='email']")
    mail_input.send_keys(USERNAME + "\n")
    time.sleep(2)
    # WebDriverWait(chrome, 10).until(expected_conditions.element_to_be_clickable((By.NAME, "password")))

    password_input = chrome.find_element_by_xpath("//input[@type='password']")
    password_input.send_keys(PASSWORD + "\n")
    time.sleep(2)

    del USERNAME, PASSWORD
else:
    USERNAME = input("\nPES ID   : ").upper()
    PASSWORD = secure_password_input("Password : ")

    print("\nLogging You In...")

    chrome.get("https://www.pesuacademy.com/Academy/")
    username_input = chrome.find_element_by_id("j_scriptusername")
    password_input = chrome.find_element_by_name("j_password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD + '\n')

    del USERNAME, PASSWORD

try:
    WebDriverWait(chrome, 20).until(lambda driver: "www.pesuacademy.com/Academy/a/studentProfilePESU" in driver.current_url)
except TimeoutException:
    print("Invalid Login Credentials!")
    chrome.quit()
    print("\n---------------------------------------------------------")
    input("Press ENTER to exit...")
    exit(0)

print("---------------------------------------------------------")

menu = chrome.find_element_by_class_name("menu-left")
courses_link = menu.find_element_by_id("menuTab_653")
time.sleep(5)
courses_link.click()

WebDriverWait(chrome, 10).until(expected_conditions.element_to_be_clickable((By.ID, "rowWiseCourseContent_10213")))

input("\nPress ENTER to Download All Slides from CS201 to CS205...")
print("---------------------------------------------------------")
for c in range(10212, 10217):   # Courses Loop
    print("Downloading Slides from CS%d..." % (201 + c - 10212))
    download_subject_content(chrome, c, 1)
    print("Downloaded Slides from CS%d!\n" % (201 + c - 10212))

input("\nPress ENTER to Download All Notes from CS201 to CS205...")
print("---------------------------------------------------------")
for c in range(10212, 10217):   # Courses Loop
    print("Downloading Notes from CS%d..." % (201 + c - 10212))
    download_subject_content(chrome, c, 2)
    print("Downloaded Notes from CS%d!\n" % (201 + c - 10212))

chrome.quit()

print("\n---------------------------------------------------------")
input("Press ENTER to exit...")

"""
while True:
    try:
        exec(input("Code Line    |>\t"))
    except Exception as e:
        print("ERROR        <|\t" + str(e))
"""