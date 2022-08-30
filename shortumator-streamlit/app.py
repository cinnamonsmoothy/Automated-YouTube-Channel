#--modules:
import streamlit as st
from streamlit_lottie import st_lottie
import json
import random
import os, subprocess
from pathlib import Path


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
  height: 280px;
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

                with st.form(str(file)):
                    
                        #-title:
                        st.text_input(label = 'Title', placeholder = 'Add a title that describes your video', max_chars=55)
                        
                        media, metadata = st.columns([1, 1])
                        
                        with media:
                            if 'reel_C' in file:
                                st.caption('https://www.instagram.com/p/' + (file[5:16]))
                            else:
                                st.caption('No Link Available :(')

                            st.video(data = file)
                            
                        with metadata:
                            
                            #-desciption:
                            st.text_area(label = 'Description', placeholder = 'Add a description of the video for your viewers', height=70)

                            #-upload date + time:
                            upload_date = st.date_input('Publish Date')
                            upload_time = st.time_input('Publish Time')

                        st.form_submit_button(label='Publish Video', help=None, on_click=None, args=None, kwargs=None)
                        os.chdir('C:/Users/hamza/Desktop/shortumator-streamlit')
                        
                #-gap between posts
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                
#--generate feed:                 
generate_feed()
st.markdown('### Thats All!')

