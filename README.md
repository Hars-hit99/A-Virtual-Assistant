# Spora — Voice-Controlled Desktop Assistant

A Python-based voice assistant that listens for a wake word, understands spoken commands, and responds out loud. Spora can open websites, play music, read the news, search Wikipedia, and answer open-ended questions using Google's Gemini API.

## Features

- **Wake-word activation** — listens passively and springs into action when it hears "Spora"
- **Voice input & output** — uses Google Speech Recognition for input and gTTS for natural-sounding spoken responses
- **Web shortcuts** — opens Google, YouTube, GitHub, LinkedIn, Instagram, and more on command
- **Music playback** — plays tracks from a configurable local music library
- **Live news briefings** — fetches top headlines or topic-specific news via the NewsAPI
- **Wikipedia lookups** — answers "who is" / "what is" / "tell me about" questions with concise summaries
- **AI-powered fallback** — routes any unrecognized question to Google Gemini (free tier) for a conversational answer
- **Time & date queries**

## Tech Stack

| Component        | Technology              |
|-------------------|--------------------------|
| Speech-to-text    | `speech_recognition` (Google Web Speech API) |
| Text-to-speech    | `gTTS` + `pygame`         |
| News              | `newsapi-python`          |
| Knowledge lookup  | `wikipedia`                |
| Conversational AI | Google Gemini API (`gemini-3.5-flash`) |
| Config            | `python-dotenv`            |

## Getting Started

### Prerequisites

- Python 3.9+
- A working microphone and speakers
- API keys:
  - [NewsAPI](https://newsapi.org/) key
  - [Google Gemini API](https://aistudio.google.com/apikey) key (free tier)

### Installation

```bash
git clone https://github.com/<your-username>/Spora-voice-assistant.git
cd Spora-voice-assistant
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
news_api_key=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### Run

```bash
python Spora.py
```

Say **"Spora"** to wake it up, then speak your command.

## Example Commands

| Say this                          | Spora does                          |
|------------------------------------|----------------------------------------|
| "Open YouTube"                     | Opens youtube.com                      |
| "Play [song name]"                 | Plays a track from your music library  |
| "What's the time"                  | Speaks the current time                |
| "Give me the news"                 | Reads today's top headlines            |
| "News about technology"            | Reads headlines on a specific topic    |
| "Who is Marie Curie"               | Reads a Wikipedia summary               |
| "What's the capital of Japan"      | Falls back to Gemini for an answer      |
| "Ask Gemini to explain quantum computing" | Sends the question directly to Gemini |
| "Stop" / "Goodbye"                 | Shuts Spora down                       |

## Project Structure

```
Spora-voice-assistant/
├── Spora.py           # Main assistant logic
├── musiclibrary.py     # Song name → URL mapping
├── .env                # API keys (not committed)
├── requirements.txt    # Python dependencies
└── README.md
```

## Roadmap / Future Aspirations

This project is an evolving playground for exploring voice-driven, agentic assistants. Planned improvements include:

- [ ] **Offline speech recognition** (e.g. Vosk/Whisper) to remove dependency on internet-based STT
- [ ] **Wake-word detection library** (e.g. Porcupine) instead of polling short audio clips, for lower latency and better accuracy
- [ ] **Conversation memory** — let Gemini maintain context across a multi-turn conversation rather than treating each command in isolation
- [ ] **Rate-limit resilience** — retry with exponential backoff and graceful fallback when the Gemini free tier is throttled
- [ ] **Smart home integration** — control lights, plugs, and thermostats via Home Assistant or similar APIs
- [ ] **Calendar & reminders** — read/write to Google Calendar for scheduling and reminders
- [ ] **Email assistant** — read unread emails aloud and draft replies via voice
- [ ] **Custom wake word** ("Hey Spora" personalization)
- [ ] **Cross-platform packaging** — ship as a standalone app (PyInstaller) for easy installation
- [ ] **Plugin architecture** — let commands be registered as modular plugins instead of hardcoded `if` branches
- [ ] **Multi-language support** for both recognition and speech output

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](../../issues) or open a pull request.


## Author

Built as a personal project to explore speech interfaces, API integration, and applied conversational AI.

**Feel free to connect or reach out with feedback and ideas!**
