import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import Select
import pytz

def opening(driver):
    driver.get("https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=isla&realmId=190&categoryId=3238")

def click_continue_button(driver):
    # Wait until the 'Continue' button is clickable
    try:
        continue_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "appointment_captcha_month_appointment_showMonth"))
        )
        continue_button.click()
        print("Continue button clicked at:", datetime.now().time())
    except Exception as e:
        print("Error clicking the Continue button:", e)

def appointments_are_available(driver):
    try:
        available_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "arrow"))
        )
        available_button.click()
        print("Appointments button clicked at:", datetime.now().time())
    except Exception as e:
        print("Error clicking the Appointments button:", e)

def click_book_appointment_button(driver):
    # Wait until "Book this appointment" button is available
    try:
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "arrow"))
        )
        for button in buttons:
            if button.text == "Book this appointment":
                button.click()
                print("Book this appointment button clicked at:", datetime.now().time())
                return
    except Exception as e:
        print("Error clicking Book this appointment button:", e)

def input_text(driver):
    try:
        fields = {
            "appointment_newAppointmentForm_lastname": "Bhatti",
            "appointment_newAppointmentForm_firstname": "Abdul Wasay",
            "appointment_newAppointmentForm_email": "abdulwasay12@gmail.com",
            "appointment_newAppointmentForm_emailrepeat": "abdulwasay12@gmail.com",
            "appointment_newAppointmentForm_fields_0__content": "BL7123",
        }

        for field_id, text in fields.items():
            input_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            input_field.clear()
            input_field.send_keys(text)
        dropdown = Select(driver.find_element(By.ID, "appointment_newAppointmentForm_fields_1__content"))
 
        dropdown.select_by_index(1)
        dropdown = Select(driver.find_element(By.ID, "appointment_newAppointmentForm_fields_2__content"))
 
        dropdown.select_by_index(2) 
        dropdown = Select(driver.find_element(By.ID, "appointment_newAppointmentForm_fields_3__content"))
 
        dropdown.select_by_index(1)  

        date_field = driver.find_element(By.ID, "fields4content")
    
    # Remove the 'readonly' attribute
        driver.execute_script("arguments[0].removeAttribute('readonly')", date_field)
        date_text="10.10.2024"
    
    # Enter the desired date
        date_field.send_keys(date_text)
        print("Date entered successfully.")

        print("Text input completed at:", datetime.now().time())
        time.sleep(120)
    except Exception as e:
        print("Error inputting text:", e)

def main():
    pk_timezone = pytz.timezone("Europe/Berlin")

    while True:
        now = datetime.now(pk_timezone)
        if now.hour == 16 and now.minute == 22 and now.second==35 :
            break
        time.sleep(1)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Open the login page
    opening(driver)

    # Wait until the target time to proceed
    while True:
        now = datetime.now(pk_timezone)
        if now.hour == 16 and now.minute == 23 and now.second==0:
            click_continue_button(driver)
            appointments_are_available(driver)
            click_book_appointment_button(driver)
            input_text(driver)
            break
        time.sleep(0.1)

if __name__ == "__main__":
    main()
