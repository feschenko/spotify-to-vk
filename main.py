from spotipy.oauth2 import SpotifyOAuth
from typing import List

from config import Config
from colorama import Fore
import spotipy
import typing
import vk_api
import time

vk = vk_api.VkApi(token=Config.VK_TOKEN).get_api()

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=Config.SCOPE,
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        redirect_uri=Config.REDIRECT_URI,
        username=Config.USERNAME,
    )
)

current_playing = typing.List[typing.Union[str, str, str]]


def update_status_to_standard():
    if vk.users.get(fields="status")[0]["status"] != Config.STANDARD_STATUS:
        vk.status.set(text=Config.STANDARD_STATUS)
    print(Fore.RED + f"User status was changed to {Config.STANDARD_STATUS}")


def update_status(_current_playing: typing.List[typing.Union[str, str, str]]
                  ) -> typing.List[typing.Union[str, str, str]]:
    current = spotify.current_user_playing_track()
    track, album, artist = current["item"]["name"], \
                           current["item"]["album"]["name"], \
                           current["item"]["artists"][0]["name"]
    if _current_playing != [track, album, artist]:
        vk.status.set(text=Config.STATUS.format(track=track, album=album, artist=album))
        print(Fore.GREEN + f"Now playing: * {track} * {album} * {artist}")
    if _current_playing is None:
        raise
    return [track, album, artist]


while True:
    try:
        current_playing = update_status(current_playing)
        time.sleep(5)
    except (KeyboardInterrupt, SystemExit, Exception):
        update_status_to_standard()
        raise
