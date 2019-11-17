import spotipy
import spotipy.util as util
import vk_api
import time
import random
from colorama import Fore, Back, Style
from dotenv import load_dotenv
import os
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
load_dotenv()


STANDART_STATUS = os.getenv("STANDART_STATUS")
VK_TOKEN = os.getenv("VK_TOKEN")
SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
VK_BOT_TOKEN = os.getenv("VK_BOT_TOKEN")
UID = os.getenv("USER_ID")

vk = vk_api.VkApi(token=VK_TOKEN)

scope = 'user-read-playback-state user-library-read'
token = util.prompt_for_user_token(f'{SPOTIFY_TOKEN}', scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='https://google.com/')
spotify = spotipy.Spotify(auth=token)







def set_standart_status():
    vk.method("status.set", {"text": STANDART_STATUS})
    print(Fore.RED + f"// STANDART STATUS USED // {STANDART_STATUS} //")

    
def set_status():
    current_track = spotify.current_user_playing_track()
    track = current_track['item']['name']
    album = current_track['item']['album']['name']
    artist = current_track['item']['artists'][0]['name']
    vk.method("status.set", {"text": f'🌟{track} 🌟 {artist} 🌟 {album} 🌟  '})
    print(Fore.GREEN + f"// NOW PLAY: // {track} // {album} // {artist} //")

    
def send_message(vk, id_type, id, message=None, attachment=None, keyboard=None):
    vk.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})
    time.sleep(20)





while True:
    try:
        set_status()
        time.sleep(5)
    except Exception as e:
        set_standart_status()
        current_track = spotify.current_user_playing_track()
#         if current_track == None:
#             send_message(vk, 'user_id', UID, message=f"Captcha!")
        continue



