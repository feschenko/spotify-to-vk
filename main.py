from spotipy.oauth2 import SpotifyOAuth as sOauth
import spotipy as sp
import vk_api
from config import Config
from colorama import Fore
import time
import random


spotify = sp.Spotify(auth_manager=sOauth(scope=Config.SCOPE,
                                         client_id=Config.CLIENT_ID,
                                         client_secret=Config.CLIENT_SECRET,
                                         redirect_uri=Config.REDIRECT_URI))
vk = vk_api.VkApi(token=Config.VK_TOKEN).get_api()
status_data = []


def update_status(last_status_data: list) -> list:

    current_playing = spotify.current_user_playing_track()
    emoji = ['☔', '⚡']

    if current_playing is None or current_playing["currently_playing_type"] == "ad" or\
            current_playing["is_playing"] is False:

        recently_played = spotify.current_user_recently_played(limit=50)
        rp_track = recently_played['items'][-1]
        status_data = [rp_track['track']['name'],
                       rp_track['track']['album']['name'],
                       ', '.join([el['name'] for el in rp_track["track"]["artists"]])]
        if status_data != last_status_data:
            text = f'{random.choice(emoji)}Spotify recently: {status_data[0]} {random.choice(emoji)} {status_data[1]} ' \
                   f'{random.choice(emoji)} {status_data[2]} {random.choice(emoji)}'
            vk.status.set(text=text)
            print(Fore.YELLOW + text)
    else:
        status_data = [current_playing["item"]["name"],
                       current_playing["item"]["album"]["name"],
                       ', '.join(el['name'] for el in current_playing["item"]["artists"])]

        if status_data != last_status_data:
            search_result = vk.audio.search(q=f"{status_data[2]} {status_data[0]}")
            if search_result["count"] == 0:
                text = f'{random.choice(emoji)}Spotify playing: {status_data[0]} {random.choice(emoji)} {status_data[1]} ' \
                       f'{random.choice(emoji)} {status_data[2]} {random.choice(emoji)}'
                vk.status.set(text=text)
                print(text)
            else:
                vk.audio.setBroadcast(
                    audio=f"{search_result['items'][0]['owner_id']}_{search_result['items'][0]['id']}")
            print(Fore.GREEN + f"Now playing: * {status_data[0]} * {status_data[1]} * {status_data[2]}")
    return status_data


while True:
    try:
        status_data = update_status(status_data)
        time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        raise
