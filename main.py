import speech_recognition as sr

from services.tts import speak
from core.plugin_manager import PluginManager
from core.intent_router import IntentRouter
from config import WAKE_WORD

r = sr.Recognizer()


def main():
    speak("Initializing Jarvis.")

    plugin_manager = PluginManager()
    router = IntentRouter(plugin_manager)
    print(f"Loaded plugins: {[p.name for p in plugin_manager.plugins]}")

    running = True
    while running:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print(f"Heard: {word}")

            if WAKE_WORD in word.lower():
                speak("Yes Spotty")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=3)

                command = r.recognize_google(audio)
                print(f"Command: {command}")

                plugin = router.route(command)
                running = plugin.run(command)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

    print("Jarvis offline.")


if __name__ == "__main__":
    main()