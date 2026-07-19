import wikipedia
from plugins.base import Plugin
from services.tts import speak


class WikipediaPlugin(Plugin):
    name = "wikipedia"
    priority = 40
    triggers = ["wikipedia", "search", "who is", "what is"]

    def matches(self, command):
        cmd = command.lower()
        return any(kw in cmd for kw in self.triggers)

    def run(self, command):
        try:
            topic = command
            for kw in self.triggers:
                if kw in command.lower():
                    idx = command.lower().find(kw)
                    topic = command[idx + len(kw):].strip()
                    break

            if not topic:
                speak("What would you like me to look up on Wikipedia?")
                return True

            speak(f"Searching Wikipedia for {topic}")

            try:
                summary = wikipedia.summary(topic, sentences=2)
                print(f"Wikipedia: {summary}")
                speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                options = e.options[:5]
                first_option = options[0]
                speak(f"That was ambiguous. Showing results for {first_option}")
                summary = wikipedia.summary(first_option, sentences=2)
                print(f"Wikipedia: {summary}")
                speak(summary)
            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I couldn't find a Wikipedia page for {topic}")

        except Exception as e:
            print(f"Wikipedia error: {e}")
            speak("Sorry, something went wrong while searching Wikipedia")

        return True
