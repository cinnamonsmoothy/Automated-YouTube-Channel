#--modules
from instagrapi import Client


#--define cl
cl = Client()


#--settings
cl.login('adjdj_jdjdjdjd', '999digits123')
postid = cl.media_pk_from_url('https://www.instagram.com/p/Cgz5iQssb4i/')


#--download clip
cl.clip_download(postid, 'C:/Users/hamza/Desktop/instascrape')
print('download succesful.')
