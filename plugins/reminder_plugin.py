from plugins.base import Plugin
from services.tts import speak
import threading
import time
class ReminderPlugin(Plugin):
    name = "reminder"
    priority = 30
    triggers = ["remind", "timer"]
    time_keywords = ["for", "of", "in", "about"]

    def matches(self, command):
        cmd = command.lower()
        return any(t in cmd for t in self.triggers)

    def run(self, command):
        extract_time()

    def extract_time(self, command):
        cmd = command.lower()
        for kw in self.time_keywords:
            marker = f" {kw} "
            

