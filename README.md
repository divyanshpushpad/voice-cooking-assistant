# 🔊 Voice-Controlled Cooking Assistant

This is a voice-controlled cooking assistant built with Python. It guides users through step-by-step recipes using voice commands like "next step", "repeat", or "stop". It also includes the ability to recognize simple spoken inputs and manage recipe flow interactively. It aims to do all tasks of the user while he/she is busy in cooking.

---

## 🚀 Features

- Voice command recognition using SpeechRecognition
- Text-to-speech guidance with pyttsx3
- Predefined recipe steps with voice responses
- Command-based flow control (e.g., "next step", "repeat")
- Easy to customize and extend with more recipes
- Voice command to play videos on YT
- Set timmers

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/divyanshpushpad/voice-cooking-assistant.git
cd voice-cooking-assistant
```
### 2. Create and activate a virtual environment (recommended)
 
For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```
For Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install all required Python packages

```bash
pip install -r requirements.txt
```
If pyaudio fails to install, use a prebuilt wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio (for Windows users).

### 4. Run the Voice-Controlled Assistant

```bash
python assistant.py
```
### Once it's running, speak clearly into your mic. Use voice commands like:

start maggi recipe

next step

repeat step

ingredients

nutritional information

set a timer for 2 minutes

play relaxing music

stop or exit to end



