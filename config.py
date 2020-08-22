import os


class Config:
    STANDART_STATUS = os.getenv("STANDART_STATUS") or "Your Status"
    STATUS = (
        os.getenv("STATUS") or "⏯ ʟɪsᴛᴇɴɪɴɢ ᴏɴ sᴘᴏᴛɪꜰʏ: {track} - {artist} - {album}"
    )
    VK_TOKEN = os.getenv("VK_TOKEN") or ""
    CLIENT_ID = os.getenv("CLIENT_ID") or ""
    CLIENT_SECRET = os.getenv("CLIENT_SECRET") or ""
    REDIRECT_URI = os.getenv("REDIRECT_URI") or ""
    USERNAME = os.getenv("USERNAME") or "Username"
    SCOPE = os.getenv("SCOPE") or "user-read-playback-state user-library-read"
