from newsapi import NewsApiClient
from plugins.base import Plugin
from services.tts import speak
from config import NEWS_API_KEY


class NewsPlugin(Plugin):
    name = "news"
    priority = 30

    def __init__(self):
        self.client = NewsApiClient(api_key=NEWS_API_KEY)

    def matches(self, command):
        return "news" in command.lower()

    def run(self, command):
        try:
            topic = None
            keywords = ["about", "on", "related to", "regarding"]
            for kw in keywords:
                topic = command.split(kw)[-1].strip()
                break

            if topic:
                response = self.client.get_everything(
                    q=topic,
                    language="en",
                    sort_by="publishedAt",
                    page=5
                )
                speak(f"Here are the latest headlines about {topic}")
            else:
                response = self.client.get_top_headlines(
                    country='in',
                    page_size=5
                )
                speak("Here are today's top headlines")

            articles = response.get('articles', [])

            if not articles:
                speak("Sorry, I couldn't find any news right now.")
                return True

            for i, article in enumerate(articles[:5], 1):
                title = article.get('title', '').split(' - ')[0]
                print(f"{i}. {title}")
                speak(f"{i}; {title}")

        except Exception as e:
            print(f"News error: {e}")
            speak("Sorry, I couldn't fetch the news right now.")

        return True