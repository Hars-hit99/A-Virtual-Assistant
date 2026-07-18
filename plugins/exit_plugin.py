from plugins.base import Plugin
from services.tts import speak


class ExitPlugin(Plugin):
    name = "exit"
    priority = 0
    triggers = ["stop", "exit", "goodbye", "shut down", "shutdown", "bye bye"]

    def matches(self, command):
        cmd = command.lower()
        return any(t in cmd for t in self.triggers)

    def run(self, command):
        speak("Goodbye! Shutting down.")
        return False