class Config:
    STANDARD_STATUS = "_"
    STATUS = "{track} - {artist} - {album}"
    VK_TOKEN = ""  # Access token for VKontakte account.
    CLIENT_ID = ""  # Client ID for spotify application.
    CLIENT_SECRET = ""  # Client secret for spotify application.
    REDIRECT_URI = "http://localhost:8888"  # Redirect uri for spotify application.
    USERNAME = ""  # Your name in spotify.
    SCOPE = "user-read-playback-state user-library-read"  # Spotify scopes.
