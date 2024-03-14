from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_attendance(username, password):
    # Initialize Chrome WebDriver
    driver = webdriver.Edge()

    # Open ERP login page
    driver.get("https://learner.pceterp.in/")

    # Find username and password fields and input the credentials
    username_field = driver.find_element(By.ID, "input-0")
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "input-2")
    password_field.send_keys(password)

    # Submit the login form by simulating a click on the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for the attendance page to load
    time.sleep(5)

    # Navigate to the attendance page
    driver.get("https://learner.pceterp.in/attendance")

    # Wait for the attendance page to load
    time.sleep(5)

    # Find the parent div containing all attendance divs
    parent_div = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/main/div/div/div/div/div[2]/div[2]/div")

    # Find all child divs containing attendance data
    attendance_divs = parent_div.find_elements(By.XPATH, "./div")

    # Iterate over each div and extract the data
    for div in attendance_divs:
        # Extract text content of the div
        attendance_data = div.text

        # Print attendance data
        print("Attendance Data:", attendance_data)

        # Add a sleep of 1 second
        time.sleep(1)

    # Close the browser window
    driver.quit()

# Example usage:
username = "122B1B200"
password = "d35789512357b"
scrape_attendance(username, password)
