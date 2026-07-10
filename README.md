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

Contributions, issues, an# Spora

A voice assistant I'm building from scratch in Python. Say the wake word, give it a command, it does the thing or speaks back. No bloated frameworks, minimal internet dependency except where it actually matters (Gemini for the smart stuff).

Started out as a single `if/elif` chain that got out of hand fast. Now it's a proper plugin system — every capability is its own file, and adding a new one doesn't mean touching everything else.

## How it's built

```
Spora/
├── main.py                  # wake word loop + command loop
├── config.py                 # API keys, constants, wake word
├── core/
│   ├── plugin_manager.py     # auto-discovers plugins, sorts by priority
│   └── intent_router.py      # picks the right plugin for a command
├── plugins/
│   ├── base.py                # Plugin ABC
│   ├── exit_plugin.py
│   ├── browser_plugin.py
│   ├── music_plugin.py
│   ├── time_plugin.py
│   ├── date_plugin.py
│   ├── news_plugin.py
│   ├── wikipedia_plugin.py
│   ├── weather_plugin.py
│   └── gemini_plugin.py       # catch-all, priority 999
├── services/
│   ├── tts.py                 # gTTS + pygame playback
│   └── gemini_service.py      # raw Gemini REST calls
└── data/
    ├── musiclibrary.py
    └── sitelibrary.py
```

Each plugin just implements `matches(command)` and `run(command)`. `PluginManager` finds them all via `pkgutil`, sorts by priority (low number = checked first, exit is 0, Gemini is 999 so it only fires when nothing else claims the command). Adding a new skill means dropping a new file in `plugins/` — nothing else needs to change.

## What it can do right now

- Wake word activation (`"jarvis"` for now, will rename to `"spora"`)
- Open sites — YouTube, GitHub, whatever's in the site library
- Play music from a local library
- Tell you the time and date
- Read news headlines, general or topic-specific (NewsAPI)
- Wikipedia summaries for "who is" / "what is" type questions
- Current weather via Open-Meteo (free, no API key needed)
- Falls back to Gemini for anything it doesn't recognize, so it can basically answer whatever you throw at it

## Tech it's running on

- `speech_recognition` (Google Web Speech backend for now — see roadmap, this is the first thing getting replaced)
- `gTTS` + `pygame` for speech output, Indian English accent, tuned for fast/snappy playback instead of the default sluggish pace
- Gemini API (`gemini-3.5-flash`) hit directly over REST, no SDK
- Open-Meteo for weather, keyless
- `pycaw` for real system volume control on Windows
- `python-dotenv` for keeping keys out of the repo

## Setup

```bash
git clone <repo-url>
cd spora
pip install -r requirements.txt
```

Drop a `.env` in the root:

```env
NEWS_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Run it:

```bash
python main.py
```

## Plugins in progress / next up

- **Volume control plugin** — wire up the `pycaw` work into an actual plugin instead of a standalone script
- **Reminders / alarms plugin** — set and get spoken reminders
- **Retry wrapper for Gemini** — shared backoff logic so 503s and read timeouts don't just die, and so the fallback pattern doesn't accidentally hammer the free-tier rate limit
- **Smart home plugin** — lights/plugs through Home Assistant, way down the line
- **App launcher plugin** — "open spotify", "open vscode" for local apps, not just websites

## Bigger goals

- **Ditch Google's speech backend.** `recognize_google()` needs internet for every single phrase, which defeats half the point of a "low-dependency" assistant. Currently weighing:
  - **Porcupine** for wake word + a separate offline STT for commands
  - **Vosk** — does wake word and full transcription in one, but eats more CPU and is less accurate than Porcupine for the wake word part specifically
  - **openWakeWord** as another wake-word-only option to compare against Porcupine
- **Offline TTS.** gTTS works but it's a cloud call every time something needs to be said. Looking hard at **Piper TTS** — runs locally, no API round trip. Porcupine + Piper is looking like the strongest fully-offline combo right now.
- **Conversation memory for Gemini.** Right now every question to Gemini is stateless. Want basic short-term context so follow-up questions actually make sense.
- **Config-driven plugin priorities** instead of hardcoding them per file, so reordering doesn't mean editing source.
- Eventually: package this as something installable instead of "clone and run `main.py`."

## Notes to self / lessons learned the hard way

- Indentation bugs inside plugin `run()`/`matches()` loops are sneaky — a misplaced `return True` inside a `for` loop will silently only check the first entry. Bit me twice already (browser plugin, then almost again in music plugin).
- Rotate API keys immediately if one ever ends up somewhere it shouldn't (chat logs, commits, wherever).
- The plugin refactor was 100% worth the pain. The old `if/elif` chain was unmaintainable past like 6 commands.d feature requests are welcome. Feel free to check the [issues page](../../issues) or open a pull request.


## Author

Built as a personal project to explore speech interfaces, API integration, and applied conversational AI.

**Feel free to connect or reach out with feedback and ideas!**
