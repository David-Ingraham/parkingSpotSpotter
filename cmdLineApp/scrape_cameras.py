from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def scrape_camera_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get('https://webcams.nyctmc.org/cameras-list')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))

    # Extract the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    camera_data = {}

    # Find all rows in the table
    rows = soup.find_all('tr', class_='mat-row')
    for index, row in enumerate(rows):
        try:
            print(f"Processing row {index}")

            # Extract the address
            address = row.find('td', class_='cdk-column-name').text.strip()
            print(f"Address: {address}")

            # Click the row to view the selected camera
            row_elements = driver.find_elements(By.CLASS_NAME, 'mat-row')
            print(f"Total rows found: {len(row_elements)}")
            row_element = row_elements[index]
            print(f"Clicking on row {index}")
            driver.execute_script("arguments[0].click();", row_element)

            # Ensure the "View Selected" button is clickable and click it
            print("Waiting for 'View Selected' button to be clickable...")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "mat-raised-button") and contains(span/text(), "View Selected")]'))
            )
            print("'View Selected' button is clickable")
            view_button = driver.find_element(By.XPATH, '//button[contains(@class, "mat-raised-button") and contains(span/text(), "View Selected")]')
            print("Found 'View Selected' button:", view_button)
            view_button.click()
            print(f"Clicked 'View Selected' for row {index}")

            # Wait for the video element to appear and get the camera ID from the video URL
            print("Waiting for video element to appear...")
            video_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img.image'))
            )
            print("Video element appeared")
            video_url = video_element.get_attribute('src')
            camera_id = video_url.split('/')[-2]
            print(f"Video URL: {video_url}")
            print(f"Camera ID for {address}: {camera_id}")

            camera_data[address] = camera_id
            print()
            print('*' * 40)
            print()
            driver.back()
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            #print(driver.page_source)  # Log the current page source for debugging
            driver.get('https://webcams.nyctmc.org/cameras-list')
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            rows = soup.find_all('tr', class_='mat-row')

    driver.quit()
    return camera_data

camera_data = scrape_camera_data()

# Save the camera data to a file for future use
with open('camera_data.json', 'w') as f:
    json.dump(camera_data, f)

print("Camera data has been saved to camera_data.json.")
