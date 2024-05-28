from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
time.sleep(30)

# Click the submit button
driver.find_element(By.ID, 'Login').click()

try:
    # Wait for the specific heading with ID 'my_test_results_heading' to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'My Test Results'))
    )
    
    # Find the specific heading element
    heading_element = driver.find_element(By.ID, 'My Test Results')
    
    # Find all links following the heading
    links = heading_element.find_element(By.LINK_TEXT, 'NCMHCE Practice Exams')
    
    # Click on the first four links
    for link in links[:4]:
        link.click()
        
    print("Clicked on the first four links following the heading with ID 'my_test_results_heading'")
    
except Exception as e:
    print(f"Failed to click on links: {e}")

# Close the browser
driver.quit()