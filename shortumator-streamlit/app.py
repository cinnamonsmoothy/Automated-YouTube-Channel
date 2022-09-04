#--modules:
import streamlit as st
from streamlit_lottie import st_lottie
import json
import random
import os, subprocess
from pathlib import Path
import time
from datetime import datetime
#-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from fake_headers import Headers

#--login details
email = 'petuniverse.business@gmail.com'
password = '999digits'


#--selector shortcuts:
rejectall_btn = '//tp-yt-paper-button[contains(@aria-label, "Reject")]'
signin_btn = '//tp-yt-paper-button[contains(@aria-label, "Sign in")]'
email_input = '//input[contains(@type, "email")]'
next_btn = '//div[contains(@id, "Next")]'
password_input = '//input[contains(@autocomplete, "password")]'
create_btn = '//button[contains(@aria-label, "Create")]'
upload_btn = '//a[contains(@href, "upload")]'
select_files_btn = '//input[@type="file"]'
title_input = '//div[contains(@aria-label, "title")]'
description_input = '//div[contains(@aria-label, "Tell viewers")]'
show_more_btn = '//ytcp-button[contains(@id, "toggle")]'
no_kids_radio = '//tp-yt-paper-radio-button[contains(@name, "NOT")]'
tags_input = '//ytcp-form-input-container[contains(@id, "tags")]'
next_btn_2 = '//ytcp-button[contains(@id, "next")]'
public_radio = '//tp-yt-paper-radio-button[contains(@name, "PUBLIC")]'
private_radio = '//tp-yt-paper-radio-button[contains(@name, "PRIVATE")]'
schedule_radio = '//tp-yt-paper-radio-button[contains(@name, "SCHEDULE")]'
publish_btn = '//ytcp-button[contains(@id, "done")]'
upload_time_input = '//input[contains(@aria-labelledby, "paper-input-label-1")]'
upload_date_dropdown = '//ytcp-text-dropdown-trigger[contains(@id, "datepicker-trigger")]'
upload_date_input = '/html/body/ytcp-date-picker/tp-yt-paper-dialog/div/form/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input'

#--css styling
st.markdown(
"""
<style>

/* Titles */ 
h1 {
  color: #c2185b;
}

/* Title Field */ 
.st-cg {
  line-height: 2;
}

h3 {
  color: #c2185b;
  text-align:center;
}

/* Reels */ 
video:nth-child(1) {
  width: 100%;
  height: 277px;
}

/* Description Box */ 
.st-cu {
  resize: none;
}

/* button .css-1lsl330 */
button {
  transition: all 0.15s ease-in-out;
 }

/* labels */ 
.css-16nzq6b {
  font-size: 17px;
}

/* submit button */
button:nth-child(1) {
  width: 100%;
}
footer {visibility: hidden;}



/* Hyperlink */

a:link {
  color: #c2185b;
  text-decoration:none;
  font-size:17px;
  text-align:center;
}

/* visited link */
a:visited {
  color: #c2185b;
}

/* mouse over link */
a:hover {
  color: #f73481;
}

/* selected link */
a:active {
  color: #c2185b;
}

</style>
"""
, unsafe_allow_html=True)


#--lottie file loader (local)
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

#--lottie animations
lottie_youtube = load_lottiefile('lottie/youtube.json')


#--youtube tags:
cat_tags = ['funny cats','cute cats','funny cat','funny baby cats','cute cat','cutest cats','funny cat videos','funny kittens','cutest cat','cute baby cats','cute cat videos',
            'funny pet videos','funny animals','cute baby cat','funny cat videos 2020','cute dogs and cats','cute babies','cute kittens','cute animals','funny dog videos',
            'cute dogs','funny','cute baby','baby cats','funny animal videos','cute funny dogs','cute videos','cute puppies','baby cat','too cute','cats','cute','cutest animals']


#--widget containers:
heading_c, logo_c = st.columns([5,1])
feed_title_c = st.container()
feed_c = st.container()


#--app heading:
heading_c.title('#InstaShorts')
with logo_c:
   st_lottie(lottie_youtube, speed=1, height=105)


#--feed heading:
with feed_title_c:
    st.markdown('## Feed')
    st.markdown('')
    st.markdown('')
    st.markdown('')

#--feed content path:
reels_dir = Path('C:/Users/hamza/Desktop/shortumator-streamlit/reels')

#--generate feed function:
def generate_feed():

    for file in os.listdir(reels_dir):
        
        os.chdir(reels_dir) 

        if file.endswith('.mp4'):
            
            with feed_c:

                with st.form(key=str(file)):
                    
                    #-title:
                    title = st.text_input(label = 'Title', placeholder = 'Add a title that describes your video', max_chars=55)
                    
                    media, metadata = st.columns([1, 1])
     
                    with media:

                        #--link to instagram post:
                        if 'reel_C' in file:
                            st.caption('https://www.instagram.com/p/' + (file[5:16]))
                        else:
                            st.caption('No Link Available :(')

                        #--video:
                        st.video(data = file)

                    with metadata:
                        
                        #-desciption:
                        description = st.text_area(label = 'Description', placeholder = 'Add a description of the video for your viewers', height=70)

                        #-upload date + time:
                        upload_date = st.date_input('Publish Date')
                        upload_date_formatted = upload_date.strftime('%b %d, %Y')
                        upload_time = st.time_input('Publish Time')

                         
                    #--steps:
                    def upload():

                        #--progress bar:
                        loading_bar = st.progress(0)
                        progress_completed = 0
                        
                        #--settings:

                        #-chromedriver directory
                        s=Service('C:\Program Files (x86)\chromedriver.exe')
                        
                        #-headless mode:
                        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
                        options = uc.ChromeOptions()
                        options.headless = False
                        options.add_argument('--window-size=1920,1080')
                        options.add_argument(f'user-agent={user_agent}')

                        #-browser:
                        driver = uc.Chrome(service=s, options=options, use_subprocess=True)
                        
                        #-wait time:
                        driver.implicitly_wait(10)
                        
                        #-website url:
                        driver.get('https://www.youtube.com/')

                        time.sleep(1)
                        #--steps:
                        
                        # 1) reject cookies
                        driver.find_element(By.XPATH, rejectall_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 2) click sign in
                        driver.find_element(By.XPATH, signin_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 3) type email
                        driver.find_element(By.XPATH, email_input).send_keys(email)
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 4) click next
                        time.sleep(2)
                        driver.save_screenshot('./save_screenshot_methodd.png') #Capture the screen

                        driver.find_element(By.XPATH, next_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 5) type password
                        time.sleep(3)
                        driver.save_screenshot('./save_screenshot_method.png') #Capture the screen
                        driver.find_element(By.XPATH, password_input).send_keys(password)
                        time.sleep(0.5)
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 6) click next 
                        driver.find_element(By.XPATH, next_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)
                            
                        # 7) click create 
                        driver.find_element(By.XPATH, create_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 8) click upload video 
                        driver.find_element(By.XPATH, upload_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 9) upload video
                        driver.find_element(By.XPATH, select_files_btn).send_keys('C:/Users/hamza/Desktop/shortumator-streamlit/reels/' + str(file))
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 10) set title
                        driver.find_element(By.XPATH, title_input).clear()
                        driver.find_element(By.XPATH, title_input).send_keys(title)
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 11) set description 
                        driver.find_element(By.XPATH, description_input).send_keys(description)
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 12) click show more
                        driver.find_element(By.XPATH, show_more_btn).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 13) set tags 
                        # driver.find_element(By.XPATH, tags_input).send_keys(cat_tags)

                        # 14) click 'not made for kids'
                        driver.find_element(By.XPATH, no_kids_radio).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 15) click next
                        driver.find_element(By.XPATH, next_btn_2).click()
                        driver.find_element(By.XPATH, next_btn_2).click()
                        driver.find_element(By.XPATH, next_btn_2).click()
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 16) set visibility
                        driver.find_element(By.XPATH, schedule_radio).click()
                        driver.find_element(By.XPATH, upload_time_input).clear()
                        driver.find_element(By.XPATH, upload_time_input).send_keys(str(upload_time))
                        time.sleep(1)

                        driver.find_element(By.XPATH, upload_date_dropdown).click()
                        driver.find_element(By.XPATH, upload_date_input).clear()
                        driver.find_element(By.XPATH, upload_date_input).send_keys(str(upload_date_formatted))
                        driver.find_element(By.XPATH, upload_date_input).send_keys(Keys.RETURN)
                        
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)

                        # 17) publish
                        time.sleep(5)
                        #driver.find_element(By.XPATH, publish_btn).click()
                        time.sleep(3.5)
                        progress_completed = progress_completed + 4
                        loading_bar.progress(progress_completed)
                        
                        # 18) close
                        driver.quit()
                        time.sleep(8)
                        progress_completed = progress_completed + 6
                        loading_bar.progress(progress_completed)
                        time.sleep(0.3)
                        loading_bar.empty()
                        
                    publish_submitted = st.form_submit_button(label='Publish Video', help=None, args=None, kwargs=None)
                    os.chdir('C:/Users/hamza/Desktop/shortumator-streamlit')

                    if publish_submitted:
                        upload()
                        
                #-gap between posts
                for i in range(5):
                    st.write('')
              
#--generate feed:                 
generate_feed()
st.markdown('### Thats All!')


if __name__ == "__main__":
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )


