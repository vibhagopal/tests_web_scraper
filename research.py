from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Method to data scrape a given url and web driver
def get_data(driver, url) -> list:
    # Navigating to the appropriate practice exam
    driver.get(url)
    
    # [] keeps track of data scraped
    # QUESTION_NUMBER: current question number
    questions = []
    question_number = 1

    while True:
        try:
            # INSTRUCTIONS:
            # 1. Code will naviate to 'Practice Test Questions', 'NCMHCE Practice Exams'
            # 2. Choose the 'Study Mode' option in the 'Test of or Study Mode' field
            # 3. Click the 'APPLY PREFERENCES AND START TEST' green button
            
            # NOTE: You will have 10 seconds to complete this task. The script will read the scenario
            # if user has sucessfully navigated to the first question of the practice exam or quit otherwise.
            # From here on, the script will continue until the last practice exam questsion 
            
            # SCENARIO: Initial Intake, Presenting Problem, Mental Status Exam, Family History
            scenario = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'scenario'))
            )
            scenario_text = scenario.text
            
            # PROBLEM: The question being asked of the exam taker given scenario
            problem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'itemnum'))
            )
            problem_text = problem.text
            
            
            # OPTIONS CLEANED: a._, b._, c._, d._
            options_elements = driver.find_elements(By.CLASS_NAME, 'qanswer')
            options_cleaned = [option.text.strip() for option in options_elements]
           
            # CORRECT VALUE: a._, b._, c._, d._ (whichever option is correct)
            correct_input = driver.find_element(By.CSS_SELECTOR, 'input[name="Correct"]')
            correct_value = correct_input.get_attribute('value')
            
            # CORRECT IDX: 0, 1, 2, 3 (whichever option is correct reflected as an idx value)
            correct_idx = driver.find_element(By.CSS_SELECTOR, 'input[name="CorrectIdx"]')
            correct_idx_value = correct_idx.get_attribute('value')
            correct_idx_value = int(correct_idx_value) - 1

            # ANSWER BUTTONS: identifying all possible answer radio buttons and .click() on the proper
            # answer_buttion[correct_idx_value]
            # NOTE: It is crucial that the webdriver click on the correct answer so the explanations
            # are available.
            answer_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'qanswer'))
            )
            answer_buttons[correct_idx_value].click()
            
            # Two seconds given for the wesite to display explanation after clicking the correct answer
            time.sleep(2)
            
            # EXPLANATION ELEMENT CONTENT: correct answer explanation in paragraph form
            explanation_element = driver.find_element (By.CLASS_NAME, 'msg_answer')
            explanation_element_content = explanation_element.text
            
            # Packaging the data scraped within question_data and appending to a global questions[]
            # Format is following https://github.gatech.edu/mtaher3/Counseling-QA/blob/main/data/ncmhce_practice1_exam_questions.csv
            question_data = {
                "Source": "tests.com",
                "Exam Name": "NCMHCE Practice Exam",
                "Question #": question_number,
                
                # TODO: FILL THIS OUT
                "Case Study #": None,
                "Patient": None,
                "Patient Demographic": None,
                "Presenting Problem": None,
                "Mental Status Exam": None,
                "Content": None,
                "Question": None,
                "Choice A": None,
                "Choice B": None,
                "Choice C": None, 
                "Choice D": None,
                "Correct Answer": None,
                "Explanation for correct answer": None,
                # END OF TODO
                
                "Scenario": scenario_text,
                "Question" : problem_text,
                "Options": options_cleaned,
                "Correct Answer": correct_value,
                "Explanation Answer": explanation_element_content
            }
            questions.append(question_data)
            
            question_number += 1    
            
            # Navigating to the next page
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'recansnext'))
            )
            next_button.click()

            # Ensuring there is a scenario availble on the next page.
            # This safegaurds against infinite while loops and unncessary data
            WebDriverWait(driver, 10).until(
                EC.staleness_of(scenario)
            )

        # Error handling
        except Exception as e:
            print("No more questions or error occurred:", e)
            break

    # Quit the driver and return global questions[]
    driver.quit()
    return questions

# Login user using webdriver
def login(driver):
    driver.get('https://www.tests.com/login')

    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.ID, 'Email'))
    )

    driver.find_element(By.ID, 'Email').send_keys('cuongvnguyen1104@gmail.com')
    driver.find_element(By.ID, 'pw').send_keys('hozki4-mizhyb-muzDid')

    time.sleep(30)

    driver.find_element(By.ID, 'Login').click()

# Instantiate driver object, Login user, get data from practice exam at given link
# Package data to a CSV saved locally
def main():
    driver = webdriver.Chrome()
    login(driver)
    
    data = get_data(driver, "https://www.tests.com/mypreferences/NCMHCE-Counselor-Practice-Exam&id=202370")
    
    df = pd.DataFrame(data)
    file_path = '/Users/vibhagopalakrishnan/Desktop/exam1.csv'
    df.to_csv(file_path, index=False)
    print("Data has been saved to CSV.")

if __name__ == '__main__':
    main()