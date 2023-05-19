from selenium import webdriver
import streamlit as st
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import io
import time

def get_driver(options):
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
options.add_argument("no-sandbox")
options.add_argument("disable-dev-shm-usage")
options.add_argument("disable-gpu")
options.add_argument('--disable-web-security')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

driver = get_driver(options)
# Get the current Streamlit session
imagePlaceholder = st.empty()
errorMessage = st.empty()
# Define the Streamlit login page
def login_page():
    st.title("Gmail Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Perform Gmail login
        st.write("Logging in...")
        login(email, password)

# Define the Gmail login process using Selenium
def login(email, password):
    driver.get('https://accounts.google.com')
    time.sleep(1)
    # Find the email field and enter the provided email
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
    except Exception as e:
        errorMessage.error("An error occured: " + str(e))
        driver.quit()
        return
    try:
        # Find the password field and enter the provided password
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{password}\n')
    except Exception as e:
        errorMessage.error("An error occured: " + str(e))
        # driver.quit()
        return

    # Close the webdriver
    # driver.quit()

# Run the Streamlit app
login_page()
