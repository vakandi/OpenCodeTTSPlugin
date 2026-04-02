# OpenCode Voice Plugin

Voice input plugin for OpenCode with PyQt5 stop button and ntfy.sh notifications.

## Features

- 🎙 **Voice Recording** - Record audio with a floating PyQt5 stop button
- 📍 **Smart Positioning** - Button appears at bottom-right of Terminal window
- 🔔 **ntfy.sh Notifications** - Get notified when to speak, when transcribing, and the result
- 🇫🇷 **French Whisper** - Uses `medium` model for accurate French transcription
- ✅ **Visual Feedback** - Button changes color: 🔴 → ⏳ → ✅/❌

## Commands

| Command | Description |
|---------|-------------|
| `/talk` | Record voice, transcribe, and auto-send as message |
| `/speak` | Ask AI to speak in French with `elia-speak` |

## Installation

### 1. Prerequisites

**macOS requires:**
- `sox` (for audio recording)
- Python 3.10+ with pip
- OpenCode CLI

```bash
brew install sox
```

**Python packages:**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install openai-whisper PyQt5
```

### 2. Install Commands

```bash
mkdir -p ~/.config/opencode/commands
```

Copy these files to `~/.config/opencode/commands/`:
- `talk.md` - Voice recording command
- `speak.md` - French summary command
- `voice_record.py` - Main Python script

```bash
cp talk.md speak.md voice_record.py ~/.config/opencode/commands/
chmod +x ~/.config/opencode/commands/voice_record.py
```

### 3. ntfy.sh Setup

The plugin uses `ntfy.sh/OpenCode` topic for notifications.

**Option A: Use default (public)**
No setup needed. Install ntfy app and subscribe to `OpenCode` topic.

**Option B: Use private topic**
Edit `voice_record.py` and change:
```python
def notify(msg):
    subprocess.run(
        ["curl", "-s", "-X", "POST", "https://ntfy.sh/YOUR_TOPIC", "-d", msg],
        capture_output=True,
    )
```

### 4. Download Whisper Model

The first run will download the `medium` model (~1.5GB). To pre-download:
```bash
python3 -c "import whisper; whisper.load_model('medium')"
```

## Usage

### `/talk` - Voice Message

1. Type `/talk` in OpenCode
2. A 🔴 red stop button appears at bottom-right of Terminal
3. Speak your message
4. Click ⏹ Stop (or wait 60s timeout)
5. Button turns ⏳ blue during transcription
6. Button turns ✅ green with notification containing transcript
7. Transcript is auto-inserted and sent as chat message

### `/speak` - French Summary

Type `/speak` to ask the AI to speak in French using `elia-speak` with Kokoro TTS. The AI will prefix the message with "**Speak about the :**" followed by the content to be spoken.

## How It Works

```
┌─────────────────────────────────────────────────────┐
│  User types /talk                                   │
│         ↓                                           │
│  voice_record.py launches                           │
│         ↓                                           │
│  🔴 Red button appears (bottom-right of Terminal)   │
│         ↓                                           │
│  ntfy notification: "🎙 Parle maintenant..."         │
│         ↓                                           │
│  User clicks ⏹ Stop                                 │
│         ↓                                           │
│  ⏳ Blue button (transcribing...)                    │
│         ↓                                           │
│  ntfy notification: "⏳ Transcription..."            │
│         ↓                                           │
│  Whisper (medium model) transcribes in French        │
│         ↓                                           │
│  ✅ Green button                                    │
│         ↓                                           │
│  ntfy notification: "✅ [transcript]"              │
│         ↓                                           │
│  Transcript printed → OpenCode sends as message     │
└─────────────────────────────────────────────────────┘
```

## File Structure

```
~/.config/opencode/commands/
├── talk.md           # Command: record voice
├── speak.md          # Command: French summary
└── voice_record.py   # Main Python script

~/.config/opencode/plugins/
└── voice.ts          # (Optional) Plugin alternative
```

## Troubleshooting

### "rec command not found"
```bash
brew install sox
```

### "No module named 'whisper'"
```bash
pip install openai-whisper
```

### "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Button not appearing at Terminal
The script uses AppleScript to detect Terminal/iTerm2 window position. Grant Accessibility permissions if needed:
- System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal/iTerm

### Notifications not working
Check your ntfy.sh topic. Default is `OpenCode`. Install the ntfy app and subscribe to your topic.

### Whisper slow on first run
First run downloads the model (~1.5GB). Subsequent runs use cached model.

## Configuration

Edit `voice_record.py` to customize:

```python
TMP_FILE = "/tmp/opencode_voice.wav"  # Temp audio file
WHISPER_MODEL = "medium"              # Model: tiny/base/small/medium/large
WHISPER_LANG = "fr"                   # Language code
NTFY_TOPIC = "OpenCode"               # ntfy.sh topic
```

## Requirements

- macOS (uses AppleScript for window detection)
- sox (`brew install sox`)
- Python 3.10+
- openai-whisper
- PyQt5
