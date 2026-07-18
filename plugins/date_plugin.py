import datetime
from plugins.base import Plugin
from services.tts import speak


class DatePlugin(Plugin):
    name = "date"
    priority = 20

    def matches(self, command):
        return "date" in command.lower()

    def run(self, command):
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")
        return True