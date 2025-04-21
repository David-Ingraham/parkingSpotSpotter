from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
from PIL import Image
import numpy as np

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode to not open a browser window
driver = webdriver.Chrome(options=options)

# Open the traffic camera webpage
driver.get('https://webcams.nyctmc.org/cameras-list')

# Wait for the page to load and display the cameras list
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cameras-list')))

# Select a camera location (example: use the first camera in the list)
camera_list = driver.find_elements(By.CSS_SELECTOR, '.camera-link')
if camera_list:
    camera_list[0].click()
else:
    print("Error: No cameras found.")
    driver.quit()
    exit()

# Wait for the "View Selected" button to appear and click it
view_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "View Selected")]'))
)
view_button.click()

# Wait for the video element to load
video_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'video')))

# Get the video URL from the video element
video_url = video_element.get_attribute('src')
print(f"Video URL: {video_url}")

# Open the video stream using OpenCV
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    driver.quit()
    exit()

# Capture a single frame
ret, frame = cap.read()

if ret:
    # Convert the frame to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image
    img = Image.fromarray(frame_rgb)

    # Save the image
    img.save('traffic_screenshot.png')
    print("Screenshot saved as traffic_screenshot.png")
else:
    print("Error: Could not read frame from video stream.")

# Release the video stream and close the browser
cap.release()
driver.quit()
