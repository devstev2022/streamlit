from selenium import webdriver
import streamlit as st
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import time

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
#chrome_options.add_argument("window-size=1600,900")
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

driver = webdriver.Chrome(options=options)
# Set up the Selenium webdriver
# Navigate to the Gmail login page
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
def get_screenshot(driver, title=''):
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    # if "image_element" not in st.session_state:
    #     st.image(image, caption=title, use_column_width=True, key="image_element")
    # else:
    #     st.image(image, caption=title, use_column_width=True, key="image_element")
    imagePlaceholder.image(image, caption=title, use_column_width=True)
    time.sleep(1)
# Define the Gmail login process using Selenium
def login(email, password):
    driver.get('https://accounts.google.com')
    time.sleep(1)
    # Find the email field and enter the provided email
    try:
        login_section = WebDriverWait(driver, 3).until( #using explicit wait for 10 seconds
            EC.presence_of_element_located((By.ID, 'initialView'))
        )
        email_field = login_section.find_element(By.ID, "identifierId")           
        get_screenshot(driver, "Second Image")
        email_field.send_keys(email)
        get_screenshot(driver, "Before Input Email")
        email_field.send_keys(Keys.ENTER)
        time.sleep(1)
        get_screenshot(driver, "After Input Email")
    except Exception as e:
        errorMessage.error("An error occured: " + str(e))
        driver.quit()
        return
    try:
        # Find the password field and enter the provided password
        login_section = WebDriverWait(driver, 3).until( #using explicit wait for 10 seconds
            EC.presence_of_element_located((By.ID, 'initialView'))
        )
        password_field = login_section.find_element(By.NAME, "Passwd")
        get_screenshot(driver, "Password Page")
        password_field.send_keys(password)
        get_screenshot(driver, "Before Password Page")
        password_field.send_keys(Keys.ENTER)
        get_screenshot(driver, "Input Password Page")
    except Exception as e:
        errorMessage.error("An error occured: " + str(e))
        driver.quit()
        return

    # Close the webdriver
    # driver.quit()

# Run the Streamlit app
login_page()
