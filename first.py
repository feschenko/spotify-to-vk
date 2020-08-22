import webbrowser
import time

first_url = "https://developer.spotify.com/dashboard/"
second_url = "https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1"
third_url = 'https://www.youtube.com/watch?v=RuxZaDHeZpA'


def open():
    webbrowser.open(url=first_url)
    webbrowser.open(url=second_url)
    webbrowser.open(url=third_url)

open()
