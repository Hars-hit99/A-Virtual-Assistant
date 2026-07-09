import requests
from plugins.base import Plugin
from services.tts import speak
from services.gemini_service import ask_gemini_raw
from config import GEMINI_API_KEY


class GeminiPlugin(Plugin):
    """Handles explicit 'ask gemini' commands AND acts as the catch-all
    fallback for anything no other plugin recognizes (highest priority
    number = checked last)."""

    name = "gemini"
    priority = 999  # always last -> catch-all

    def matches(self, command: str) -> bool:
        # Catch-all: this plugin matches everything that reaches it,
        # since PluginManager only gets here if nothing else matched.
        return True

    def run(self, command: str) -> bool:
        if not GEMINI_API_KEY:
            speak("Gemini API key is not set up, so I can't answer that.")
            return True

        try:
            speak("Let me think about that")
            answer = ask_gemini_raw(command)
            print(f"Gemini: {answer}")
            speak(answer)

        except requests.exceptions.RequestException as e:
            print(f"Gemini request error: {e}")
            speak("Sorry, I couldn't reach Gemini right now.")
        except (KeyError, IndexError) as e:
            print(f"Gemini response parsing error: {e}")
            speak("Sorry, I got an unexpected response from Gemini.")
        except Exception as e:
            print(f"Gemini error: {e}")
            speak("Sorry, something went wrong asking Gemini.")

        return True