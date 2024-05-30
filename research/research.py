from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

driver = webdriver.Chrome()

# Open the website
driver.get('https://www.tests.com/login')

# Wait until the email input field is present
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'Email'))
)

# Fill out the form
driver.find_element(By.ID, 'Email').send_keys('cuongvnguyen1104@gmail.com')
driver.find_element(By.ID, 'pw').send_keys('hozki4-mizhyb-muzDid')

# Wait for the user to solve the reCAPTCHA
time.sleep(60)

# Click the submit button
driver.find_element(By.ID, 'Login').click()

# Wait for the user to navigate to study mode and appropriate settings
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.pt-title'))
)

case_study_element = driver.find_element(By.CSS_SELECTOR, 'span.pt-title')
case_study_text = case_study_element.text


####
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.scenario#sceneall'))
)
scenario_element = driver.find_element(By.CSS_SELECTOR, 'div.scenario#sceneall')

# Extract text from the scenario element
scenario_text = scenario_element.text

# Split the text into lines
lines = scenario_text.split('\n')

# Initialize variables to store information
info = {}
current_key = None

# Iterate through lines and extract key-value pairs
for line in lines:
    if line.startswith('<strong>'):
        current_key = line.replace('<strong>', '').replace('</strong>', '').strip()
    elif line.startswith('<or>'):
        continue
    elif line.strip():
        if current_key:
            info[current_key] = line.strip()

# Print or process the extracted information as needed
print(info)



# Close the browser
#driver.quit()