from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def scrape_attendance(username, password):
    # Initialize Chrome WebDriver
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Edge(options=options)

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
    time.sleep(1)

    # Navigate to the attendance page
    driver.get("https://learner.pceterp.in/attendance")

    # Wait for the attendance page to load
    time.sleep(1)

    # Find the parent div containing all attendance divs
    parent_div = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/main/div/div/div/div/div[2]/div[2]/div")

    # Find all child divs containing attendance data
    attendance_divs = parent_div.find_elements(By.XPATH, "./div")

    # Create a list to store attendance data
    attendance_list = []

    # Iterate over each div and extract the data
    for div in attendance_divs:
        # Extract text content of the div
        attendance_data = div.text

        # Add attendance data to the list
        attendance_list.append(attendance_data)

    # Close the browser window
    driver.quit()

    return attendance_list

def clean_attendance_data(attendance_data):
    # Remove any unwanted characters from the attendance data
    cleaned_data = [data.strip() for data in attendance_data]
    cleaned_data = [data.split('\n')[2] for data in cleaned_data]
    attended = [data.split('/')[0] for data in cleaned_data]
    total = [data.split('/')[1] for data in cleaned_data]

    a = 0
    t = 0
    for i in range(len(attended)):
        a += int(attended[i])
        t += int(total[i])


    return a/t

@app.route('/attendance', methods=['POST'])
def get_attendance():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Please provide both username and password'}), 400

    attendance_data = scrape_attendance(username, password)
    attendance_data = clean_attendance_data(attendance_data)

    return jsonify({'attendance': attendance_data}), 200

if __name__ == '__main__':
    app.run(debug=True)