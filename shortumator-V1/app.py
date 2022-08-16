#--modules:
import re
import traceback
import requests
import json
from os import path, kill, getpid, getcwd, execv
import os
import sys
from signal import SIGTERM
from bs4 import BeautifulSoup as soup
import datetime
from colorama import Fore, Style
from time import sleep
import emoji
import pickle
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


#--instructions:
'''
1)
To download a reel, use function:
bot.Download_reel(reel_id, file_name, username, password)

do this below the reel downloader code.

2)
To upload a reel to youtube...
'''


# [<----------REEL DOWNLOADER CODE---------->]


#--instagram login details:
username = 'adjdj_jdjdjdjd'
password = '999digits123'


#--reel script:
def Kill_with_pid(*args,**kwargs): kill(getpid(),SIGTERM)

class Main:
    def __init__(self):
        pass

    def Download_reel(self, reel_id, file_name, username, password):
        bot = Bot(self)

        # Login
        if not bot.Login(username, password):
            self.Print_error('Failed to login to Instagram. Perhaps the details are wrong?')
            self.Quit()
        else:
            pass
            
        # Download
        if not bot.Download_reel(reel_id, file_name): self.Print_error('Bot failed to download reel')
        else:
            pass

    def Print_success_message(self, msg):
        print(Fore.GREEN + f'[->] {msg}')

    def Quit(self):
        print('')
        self.Print_success_message('GOOD BYE :)')
        Kill_with_pid(sleep(5))

    def Print_error(self, msg):
        msg = Fore.RED + '[!!] ' + msg + Style.RESET_ALL
        print(msg)

    def Get_inputs(self, inputs, ty, message):
        while True:
            inp = str()
            for i in inputs:
                if inputs.index(i) == 0: inp += Style.RESET_ALL + ' ( '
                inp += Fore.RED + i
                if inputs.index(i) != len(inputs) - 1:
                    inp += Style.RESET_ALL + ', '
                else:
                    inp += Style.RESET_ALL + ' )'
            msg = Fore.GREEN + '[->] ' + Style.RESET_ALL + message + Fore.YELLOW + inp + Style.RESET_ALL + ': ' + Fore.BLUE
            response = input(msg)
            try:
                response = ty(response)
                if not isinstance(response, float) and not isinstance(response, int):
                    if len(inputs) != 0 and response not in inputs:
                        self.Print_error('You provided wrong data, please choose among the provided values')
                        continue
                return response
            except:
                t = 'string'
                if ty == int:
                    t = 'number'
                elif ty == float:
                    t = 'float'
                self.Print_error(f'You provided wrong data, your data should be a {t}')


class Bot:
    def __init__(self, main):
        self.main = main
        self.session = requests.session()

    def Load_session_file(self, username):
        try:
            file_name = username + '_session.session'
            if path.exists(file_name):
                with open(file_name, 'rb') as file:
                    self.session.cookies.update(json.loads(file.read()))
                    return True
        except:
            pass
        return False


    def Check_login(self):
        try:
            content = self.session.get('https://instagram.com',timeout=60).text
            matches = re.findall('"viewerId":".*?"}',content)
            if matches: return json.loads('{'+matches[0])["viewerId"].isnumeric()
        except:
            pass
        return False

    def Get_csrf_value(self, response):
        
        try:
            for cookie in response.cookies:
                if cookie.name == 'csrftoken': return cookie.value
        except:
            pass
        return False


    def Login(self,username,password):
        try:
            self.Load_session_file(username)
            if self.Check_login(): return True
            self.session.cookies.clear()
            self.session.params.clear()
            self.session.headers.clear()
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)",
                'accept': '*/*',
                'x-requested-with': 'XMLHttpRequest',
                'origin': 'https://www.instagram.com',
                'referer': 'https://www.instagram.com/',
                'accept-language': 'en-US,en;q=0.9',
            }
            self.session.headers.update(headers)
            response = self.session.get('https://instagram.com',timeout=60)
            time = int(datetime.now().timestamp())
            csrf = self.Get_csrf_value(response)
            if not csrf:
                self.main.Print_error('Bot failed to get csrf token')
                return False
            payload = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }
            login_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": csrf
            }
            self.session.headers.update(login_header)
            login_response = self.session.post('https://www.instagram.com/accounts/login/ajax/', data=payload).json()
            if login_response['status'] == 'ok' and login_response["authenticated"]:
                headers = {
                    'authority': 'www.instagram.com',
                    'user-agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                    "Referer": "https://www.instagram.com/",
                    'accept-language': 'en-US,en;q=0.9',
                }
                self.session.headers.update(headers)
                self.Save_session(username,dict(self.session.cookies))
                return True
            elif 'two_factor_required' in login_response and login_response['two_factor_required']:
                code = self.main.Get_inputs([], int, 'Enter the code you received')
                self.Verify_fa(username, login_response['two_factor_info']['two_factor_identifier'], code)
                return self.Check_login()
            else:
                return self.Check_login()
        except:
            pass
        return False


    def Verify_fa(self, username, identifier, code):
        try:
            data = {
                'identifier': identifier,
                'trust_signal': 'false',
                'username': username,
                'verificationCode': code,
                'verification_method': '1',
                'queryParams': '{"next":"/"}'
            }
            response = self.session.post('https://www.instagram.com/accounts/login/ajax/two_factor/',data=data).json()
            if response['status'] == 'ok': return True
            return self.Check_login()
        except:
            return False

    def Save_session(self,username,cookies):
        file = username+'_session.session'
        try:
            with open(file,'wb+') as doc:
                doc.write(json.dumps(cookies).encode())
        except:
            pass


    def Get_media_id(self, content):
        match = re.findall('"media_id":".*?"', content.text)
        return json.loads('{%s}'%match[0])['media_id']


    def Get_media_info(self, media_id):
        try:
            headers = self.session.headers.copy()
            headers['user-agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
            session = requests.session()
            session.cookies.update({'sessionid': self.session.cookies['sessionid']})
            session.headers.update(headers)
            response = session.get('https://i.instagram.com/api/v1/media/{}/info/'.format(media_id))
            if response.ok: return response.json()
            else: raise Exception(response.text)
        except:
            pass


    def Download(self, video_url, file_name):
        response = self.session.get(video_url)
        with open(file_name+'.mp4', 'wb+') as file:
            file.write(response.content)
            return True


    def Download_reel(self, id, file_name):
        try:
            url = 'https://www.instagram.com/reel/{}/?utm_source=ig_web_copy_link'.format(id)
            content = self.session.get(url)
            media_id = self.Get_media_id(content)
            if not media_id:
                self.main.Print_error('Bot failed to get the media id')
                return
            media_info = self.Get_media_info(media_id)
            if not media_info:
                self.main.Print_error('Bot failed to get media info')
                return
            if media_info['items'][0]['media_type'] != 2:
                self.main.Print_error('Media is not a video')
                return
            video_url = media_info['items'][0]['video_versions'][0]['url']
            return self.Download(video_url, file_name)
        except Exception as e:
            self.main.Print_error(str(e))


if __name__ == '__main__':
    bot = Main()

#--download reel:
reel_id = input('reel id: ')
file_name = 'reel_'+ str(reel_id) 
bot.Download_reel(reel_id, file_name, username, password)

    
# [<----------YOUTUBE UPLOADER CODE---------->]


#--tags:
cat_tags = ['funny cats','cute cats','funny cat','funny baby cats','cute cat','cutest cats','funny cat videos','funny kittens','cutest cat','cute baby cats','cute cat videos',
            'funny pet videos','funny animals','cute baby cat','funny cat videos 2020','cute dogs and cats','cute babies','cute kittens','cute animals','funny dog videos',
            'cute dogs','funny','cute baby','baby cats','funny animal videos','cute funny dogs','cute videos','cute puppies','baby cat','too cute','cats','cute','cutest animals']


#--upload times: 
now = datetime.datetime.today()
tonight = (now.replace(hour=17, minute=0, second=0, microsecond=0)).isoformat() + '.000Z'
tomorrow = (now.replace(hour=17, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)).isoformat() + '.000Z'


#--video info:
title = input('title: ')
desc = input('description: ')


#--api function:
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


#--api settings:
client_secret_file = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


#--create service:
service = Create_Service(client_secret_file, API_NAME, API_VERSION, SCOPES)


#--setting video metadata:
request_body = {
    'snippet': {
        'title': title,
        'description': desc,
        'tags': cat_tags
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': tomorrow,
        'selfDeclaredMadeForKids': False, 
    },
    'notifySubscribers': False
}


#--upload video to youtube:
upload_video = MediaFileUpload(file_name+str('.mp4'))
response_upload = service.videos().insert(part='snippet,status', body=request_body, media_body=upload_video).execute()
print('upload complete')
