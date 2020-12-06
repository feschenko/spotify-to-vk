import time

import spotipy
import vk_api
from colorama import Back, Fore, Style
from spotipy.oauth2 import SpotifyOAuth

from config import Config

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

last_track = (None, None, None)


def set_standart_status():
    user = vk.users.get(fields="status")[0]
    if user["status"] == Config.STANDART_STATUS:
        return
    vk.status.set(text=Config.STANDART_STATUS)
    print(
        Fore.RED
        + f"// Используется стандартный статус юзера: // {Config.STANDART_STATUS} //"
    )

def set_status():
    global last_track
    current_track = spotify.current_user_playing_track()

    if current_track is None:
        set_standart_status()
        return

    track = current_track["item"]["name"]
    album = current_track["item"]["album"]["name"]
    artist = current_track["item"]["artists"][0]["name"]

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
        print(Fore.GREEN + f"// Сейчас играет: // {track} // {album} // {artist} //")


while True:
    try:
        set_status()
    except Exception as e:
        print(f"An error has occurred: {e}")
        set_standart_status()
        break
    finally:
        time.sleep(5)
