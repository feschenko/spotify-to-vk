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


    if (track, album, artist) != last_track:
        r = vk.audio.search(
            q=f"\"{track}\" \"{artist}\""
        )
        if r['count'] == 0:
            set_standart_status()
            return
        music = r['items'][0]

        track_id = f"{music['owner_id']}_{music['id']}"

        vk.audio.setBroadcast(audio=track_id)
        #vk.status.set(
        #    text=Config.STATUS.format(track=track, album=album, artist=artist,)
        #)
        last_track = (track, album, artist)
        print(Fore.GREEN + f"// Now playing: * {track} * {album} * {artist}")


while True:
    try:
        current_playing = update_status(current_playing)
        time.sleep(5)
    except (KeyboardInterrupt, SystemExit, Exception):
        update_status_to_standard()
        raise
