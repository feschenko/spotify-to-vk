from spotipy.oauth2 import SpotifyOAuth as sOauth
import spotipy as sp
from config import Config
from colorama import Fore
import vk_api
import time


spotify = sp.Spotify(auth_manager=sOauth(scope=Config.SCOPE, client_id=Config.CLIENT_ID,
                                         client_secret=Config.CLIENT_SECRET, redirect_uri=Config.REDIRECT_URI,
                                         username=Config.USERNAME))


vk = vk_api.VkApi(token=Config.VK_TOKEN).get_api()
user = vk.account.getProfileInfo()
current_playing = []


def update_status_to_standard():
    if vk.status.get(user_id=user["id"])["text"] != Config.STANDARD_STATUS:
        vk.status.set(text=Config.STANDARD_STATUS)
        print(Fore.RED + "Your status was changed to a standard because of error.")


def update_status(last_playing: list) -> list:
    current_playing = spotify.current_user_playing_track()

    if current_playing is None:
        update_status_to_standard()
        return current_playing

    if current_playing["currently_playing_type"] != "ad":
        if current_playing["is_playing"] is False:
            update_status_to_standard()
            return current_playing

        current_playing = [current_playing["item"]["name"], current_playing["item"]["album"]["name"],
                           current_playing["item"]["artists"][0]["name"]]

        if current_playing != last_playing:
            search_result = vk.audio.search(q=f'{current_playing[0]} {current_playing[2]}')
            if search_result["count"] == 0:
                vk.status.set(text=Config.STATUS.format(track=current_playing[0], album=current_playing[1],
                                                        artist=current_playing[2]))
            else:
                vk.audio.setBroadcast(audio=f"{search_result['items'][0]['owner_id']}_{search_result['items'][0]['id']}")
            print(Fore.GREEN + f"Now playing: * {current_playing[0]} * {current_playing[1]} * {current_playing[2]}")
    else:
        update_status_to_standard()
    return current_playing



while True:
    try:
        current_playing = update_status(current_playing)
    except (KeyboardInterrupt, SystemExit):
        update_status_to_standard()
        raise
