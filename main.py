import speech_recognition as sr
import webbrowser
import datetime
import musiclibrary
from gtts import gTTS
import pygame
from newsapi import NewsApiClient
import os
import tempfile
from dotenv import load_dotenv
import wikipedia
import requests

load_dotenv()
news_api_key = os.getenv("news_api_key")
gemini_api_key = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
 

r = sr.Recognizer()
newsapi = NewsApiClient(api_key=news_api_key)

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def speak(text):
    print(f"Spora: {text}")
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

def search_wikipedia(command):
    try:
        # Pull out the search term after common trigger words
        topic = command
        keywords = ["wikipedia","search"]
        for kw in keywords:
            if kw in command.lower():
                # split on the keyword (case-insensitive) and take what's after it
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
            # Multiple matches found; just use the first suggested option
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

def ask_gemini(command):
    if not gemini_api_key:
        speak("Gemini API key is not set up, so I can't answer that.")
        return True

    try:
        speak("Let me think about that")

        headers = {"Content-Type": "application/json"}
        params = {"key": gemini_api_key}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Answer briefly and conversationally, in 2-3 sentences, "
                                f"since this will be read aloud: {command}"}
                    ]
                }
            ]
        }

        response = requests.post(GEMINI_URL, headers=headers, params=params, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        answer = data["candidates"][0]["content"]["parts"][0]["text"].strip()
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
 

def perform_task(command):
    cmd = command.lower()

    # Exit
    if any(w in cmd for w in ["stop", "exit", "goodbye", "shut down", "shutdown", "bye bye"]):
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

    # Wikipedia
    if any(kw in cmd for kw in ["wikipedia","search"]):
        return search_wikipedia(cmd)

    # Explicit Gemini trigger
    if any(kw in cmd for kw in ["ask gemini", "gemini,"]):
        return ask_gemini(cmd)
 
    # Fallback: send anything unmatched to Gemini instead of just failing
    return ask_gemini(cmd)


if __name__ == "__main__":
    speak("Initializing Spora.")
    running = True

    while running:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print(f"Heard: {word}")

            if "spora" in word.lower():
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

    print("Spora offline.")