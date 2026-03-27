---
description: "Ask Elia to speak in French using elia-speak"
---

**Speak about the :**


${message}

---

Résume en français ce que tu viens de faire dans cette session. Utilise la commande `elia-speak` pour prononcer le résumé directement. Sois concis et parle clairement.

**IMPORTANT**: When asked to speak, ALWAYS use:
```bash
python3 /Users/vakandi/EliaAI/setup/speak.py "Ton message" --autoplay
```

Available tones:
| Tone | Flag | When to use |
|------|------|-------------|
| Default | (none) | Normal conversation, general summaries |
| Sexy | `-x` | When user explicitly asks for vocal output (most common) |
| Serious | `-s` | Technical explanations, code reviews, professional updates |
| Joyful | `-j` | Celebrating successes, good news, completed tasks |
| Angry | `-a` | Simulating frustration, warning about issues |
| Sad | `-d` | Reporting failures, bad news, blockers |
| Tired | `-t` | End of long session, acknowledging fatigue |
| Sassy | `-y` | Playful teasing, humorous responses |
| Boss | `-b` | Authoritative statements, urgent priorities |
| Whisper | `-w` | Confidential info, secrets, dramatic effect |
| Emergency | `-e` | Urgent alerts, quick status updates |

Le script utilise la voix française Elia (ff_siwis) via Kokoro TTS. Ne pas utiliser `say -v Thomas`.

**Tip**: Use `-x` (sexy) tone as default when the user asks you to speak - it's the most natural and pleasant for voice output.
