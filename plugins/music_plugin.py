from plugins.base import Plugin
from services.tts import speak
from data import musiclibrary
import webbrowser

class MusicPlugin(Plugin):
    name = "music"
    priority = 10

    def matches(self, command):
        cmd = command.lower()
        return any(f"play {music}" in cmd for music in musiclibrary.musics)

    def run(self, command):
        cmd = command.lower()
        for music, url in musiclibrary.musics.items():
            if f"play {music}" in cmd:
                speak(f"Playing {music}")
                webbrowser.open(url)
                break
        return True
