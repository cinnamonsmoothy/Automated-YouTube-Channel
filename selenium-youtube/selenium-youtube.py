#--modules:
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
#--
import time


#--login details
email = 'petuniverse.business@gmail.com'
password = '999digits'


#--setup:
s=Service('C:\Program Files (x86)\chromedriver.exe') # change this to the chromedriver directory


#--settings:

#-headless mode:
options = uc.ChromeOptions()
options.headless = False

#-browser:
driver = uc.Chrome(service=s, options=options, use_subprocess=True)

#-website url:
driver.get('https://www.youtube.com/')

#-wait time:
driver.implicitly_wait(1)

#--selector shortcuts:
rejectall_btn = '//tp-yt-paper-button[contains(@aria-label, "Reject")]'
signin_btn = '//tp-yt-paper-button[contains(@aria-label, "Sign in")]'
email_input = '//input[contains(@type, "email")]'
next_btn = '//div[contains(@id, "Next")]'
password_input = '//input[contains(@autocomplete, "password")]'
create_btn = '//button[contains(@aria-label, "Create")]'
upload_btn = '//a[contains(@href, "upload")]'

#--functions:

#-slow type:
def slow_type(element, text, delay=0.00001):
    for character in text:
        driver.find_element(By.XPATH, element).send_keys(character)
        time.sleep(delay)


# [<----------YOUTUBE UPLOAD AUTOMATED PROCESS---------->]

#--steps:

# 1) reject cookies
driver.find_element(By.XPATH, rejectall_btn).click()

# 2) click sign in
driver.find_element(By.XPATH, signin_btn).click()

# 3) type email
slow_type(email_input, email)

# 4) click next 
driver.find_element(By.XPATH, next_btn).click()

# 5) type password
slow_type(password_input, password)

# 6) click next 
driver.find_element(By.XPATH, next_btn).click()
    
# 7) click create 
driver.find_element(By.XPATH, create_btn).click()

# 8) click upload video 
driver.find_element(By.XPATH, upload_btn).click()



