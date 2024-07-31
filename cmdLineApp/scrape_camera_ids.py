import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import csv
"""

"""
# Initialize the WebDriver 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
page_num = 1
stop_address = ''
missing_addresses = []

# Open the website
driver.get('https://webcams.nyctmc.org/cameras-list')

address_api_dict = {}
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def send_failure_email(subject, body, to_email):
    from_email = EMAIL
    from_password = PASSWORD
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def click_element_with_retry(element, retries=3):
    for _ in range(retries):
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"Retry clicking element due to: {e}")
            time.sleep(1)
    return False

def get_attribute_with_retry(element, attribute, retries=3):
    for _ in range(retries):
        try:
            return element.get_attribute(attribute)
        except StaleElementReferenceException as e:
            print(f"Retry getting attribute due to: {e}")
            time.sleep(1)
    return None

def scrape_page():
    # Wait for the table to load and find all rows
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tbody[@role='rowgroup']//tr"))
    )
    
    for row in rows:
        # Get the address
        address = row.find_element(By.XPATH, ".//td[contains(@class, 'cdk-column-name')]").text.strip()
        
        
        # Scroll the row into view
        driver.execute_script("arguments[0].scrollIntoView(true);", row)
        
        # Click on the row using JavaScript
        if not click_element_with_retry(row):
            print(f"Failed to click row for address: {address}")
            missing_addresses.append(address)
            continue
        
        # Click the "View Selected" button
        try:
            view_selected_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'View Selected')]"))
            )
            view_selected_button.click()
        except ElementClickInterceptedException:
            overlay = driver.find_element(By.CLASS_NAME, "cdk-overlay-backdrop")
            driver.execute_script("arguments[0].click();", overlay)
            view_selected_button.click()

        # Wait for the popup to appear and get the src attribute
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'image')]"))
        )
        api_url = get_attribute_with_retry(img_element, 'src')

        if api_url is None:
            print(f"Failed to get API URL for address: {address}")
            missing_addresses.append(address)
            continue

        #print("\n")
        #print('*' * 60)
        print(f'{address} : {api_url}')
        #print('*' * 60)
        #print("\n")
        
        # Store the address and API URL in the dictionary
        address_api_dict[address] = api_url.split('/')[-2]
        
        # Close the popup
        close_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[mattooltip="Close dialog"]'))
        )
        #close_popup = driver.find_element(By.CSS_SELECTOR, 'button[mattooltip="Close dialog"]')
        click_element_with_retry(close_popup)
        #if address == 'YORK AVENUE @ EAST 60 STREET':
        stop_address = address
            
        
        
        

def go_to_next_page():
    
    try:
        next_page_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')
        driver.execute_script("arguments[0].click();", next_page_button)
        print("\n\n\n")
        print("Going to next page")
        
        print("\n\n\n")
    except Exception as e:
        print(f"Error clicking next page button: {e}")
        return False
    
    return True


try:

    while True:
        print(f"scraping page {page_num}")
      
        
        scrape_page()
        print(stop_address)
       
        page_num +=1
        
        # Try to go to the next page
        if not go_to_next_page():
            break

        # Wait for the next page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tbody[@role='rowgroup']//tr"))
            )
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break


        if page_num == 39:
            break

except Exception as e:
    error_message = f"Script failed with the following error: {e}"
    send_failure_email("Script Failure Alert", error_message, EMAIL)
    driver.quit()

# Print all the scraped addresses and API URLs
for address, api_url in address_api_dict.items():
    print(f"{address}: {api_url}")



# Open the file in write mode and use json.dump to write the dictionary to the file
with open('address_to_camera_id.json', 'w') as file:
    json.dump(address_api_dict, file, indent=4)  # indent=4 is optional, it prettifies the output

with open('missing_addresses.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(missing_addresses)
# Close the WebDriver
driver.quit()
