import speech_recognition as sr
import webbrowser
import datetime
import musiclibrary
from gtts import gTTS
import pygame
from newsapi import NewsApiClient
import os
import tempfile

news_api_key = "f9ed639e79d049e382e3fe21d4890633"

r = sr.Recognizer()
newsapi = NewsApiClient(api_key=news_api_key)

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def speak(text):
    print(f"Jarvis: {text}")
    try:
        # Generate speech mp3 in a temp file
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            temp_path = f.name
        
        tts.save(temp_path)
        
        # Play it
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(20)
        
        pygame.mixer.music.unload()
        os.remove(temp_path)  # Clean up temp file
        
    except Exception as e:
        print(f"Speech error: {e}")

def get_news(command):
    try:
        topic = None
        keywords = ["about", "on", "related to", "regarding"]
        for kw in keywords:
            topic = command.split(kw)[-1].strip()
            break

        if topic:
            response = newsapi.get_everything(
                q=topic,
                language="en",
                sort_by="publishedAt",
                page=5
            )
            speak(f"Here are the latest headlines about {topic}")
        else:
            response = newsapi.get_top_headlines(
                country='in',
                page_size=5
            )
            speak("Here are today's top headlines")
        
        articles = response.get('articles', [])

        if not articles:
            speak("Sorry, I couldn't find any news right now.")
            return True

        for i, article in enumerate(articles[:5], 1):
            title = article.get('title', '').split(' - ')[0]  # Remove source suffix
            print(f"{i}. {title}")
            speak(f"{i}; {title}")

    except Exception as e:
        print(f"News error: {e}")
        speak("Sorry, I couldn't fetch the news right now.")

    return True


def perform_task(command):
    cmd = command.lower()

    # Exit
    if any(w in cmd for w in ["stop", "exit", "goodbye", "shut down", "shutdown"]):
        speak("Goodbye! Shutting down.")
        return False

    # Browser shortcuts
    sites = {
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "youtube": "https://www.youtube.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com",
    }
    for site, url in sites.items():
        if f"open {site}" in cmd:
            speak(f"Opening {site}")
            webbrowser.open(url)
            return True

    # Music
    if cmd.startswith("play"):
        song = cmd[5:].strip()
        if song in musiclibrary.musics:
            speak(f"Playing {song}")
            webbrowser.open(musiclibrary.musics[song])
        else:
            speak(f"Sorry, I couldn't find {song} in your library")
        return True

    # Time
    if "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True

    # Date
    if "date" in cmd:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")
        return True

    # News
    if "news" in cmd:
        return get_news(cmd)

    speak("Sorry, I didn't understand that command")
    return True


if __name__ == "__main__":
    speak("Initializing Jarvis.")
    running = True

    while running:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print(f"Heard: {word}")

            if "jarvis" in word.lower():
                speak("Yes Spotty")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=3)

                command = r.recognize_google(audio)
                print(f"Command: {command}")
                running = perform_task(command)

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