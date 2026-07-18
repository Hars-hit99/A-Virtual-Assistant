import datetime
from plugins.base import Plugin
from services.tts import speak


class TimePlugin(Plugin):
    name = "time"
    priority = 20

    def matches(self, command):
        return "time" in command.lower()

    def run(self, command):
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True