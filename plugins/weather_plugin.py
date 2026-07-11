from plugins.base import Plugin
from services.tts import speak

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "clear sky",
    1: "mostly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy with rime",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "light snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "light rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorms",
    96: "thunderstorms with hail",
}

class WeatherPlugin(Plugin):
    name = "weather"
    priority = 20
    location_keyword = ["in", "at", "for"]
    default_city = "Gaya"

    def matches(self, command):
        cmd = command.lower
        return "weather" in cmd

    def run(self, command):
        city = self.extract_city(command) or self.default_city

        try:
            lat, lon, resolved_name = self._geocode(city)
            if lat is None:
                speak(f"Sorry, I couldn't find a place called {city}")
                return True
 
            temp, code, feels_like = self._get_forecast(lat, lon)
            condition = WEATHER_CODES.get(code, "unusual conditions")
 
            speak(
                f"It's currently {round(temp)} degrees Celsius in {resolved_name}, "
                f"feels like {round(feels_like)}, with {condition}."
            )
 
        except requests.exceptions.RequestException as e:
            print(f"Weather request error: {e}")
            speak("Sorry, I couldn't reach the weather service right now.")
        except Exception as e:
            print(f"Weather error: {e}")
            speak("Sorry, something went wrong getting the weather.")
 
        return True

    def extract_city(self, command):
        cmd = command.lower()
        for kw in self.location_keyword:
            marker = f" {kw} "
            if marker in cmd:
                return cmd.split(marker)[-1].strip()

        return ""

    def _geocode(self, city: str):
        resp = requests.get(GEOCODE_URL, params={"name": city, "count": 1}, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results")
        if not results:
            return None, None, None
        top = results[0]
        return top["latitude"], top["longitude"], top["name"]


    def _get_forecast(self, lat: float, lon: float):
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,apparent_temperature,weather_code",
        }
        resp = requests.get(FORECAST_URL, params=params, timeout=10)
        resp.raise_for_status()
        current = resp.json()["current"]
        return current["temperature_2m"], current["weather_code"], current["apparent_temperature"]
 

        

