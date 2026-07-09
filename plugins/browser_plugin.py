from plugins.base import Plugin
from services.tts import speak
from data import sitelibrary
import webbrowser

class BrowserPlugin(Plugin):
    name = "browser"
    priority = 10

    def matches(self, command):
        cmd = command.lower()
        return any(f"open {site}" in cmd for site in sitelibrary.sites)

    def run(self, command):
        cmd = command.lower()
        for site, url in sitelibrary.sites.items():
            if f"open {site}" in cmd:
                speak(f"Opening {site}")
                webbrowser.open(url)
                break
        return True