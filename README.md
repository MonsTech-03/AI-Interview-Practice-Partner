# AI-Interview-Practice-Partner
🎤 AI Interview Practice Partner — Voice + Chat (Groq + Gradio)  

An interactive **AI-powered mock interview assistant** built using **Groq LLaMA 3**, **Gradio**, **speech recognition**, and **gTTS**.  
This project lets users practice interviews using **voice + chat**, receive **smart follow-up questions**, and get a **fully structured final evaluation report** at the end.



[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Gradio](https://img.shields.io/badge/Gradio-UI-green.svg)]()
[![Groq](https://img.shields.io/badge/Powered%20by-Groq%20LLaMA3-orange.svg)]()
[![Open Source](https://img.shields.io/badge/Status-Open%20Source-brightgreen.svg)]()

---

## 🚀 Features

### 🤖 **AI Mock Interviewer**
- Asks realistic interview questions  
- Generates contextual follow-up questions  
- Supports multiple job roles:
  - Software Engineer  
  - Data Analyst  
  - Product Manager  
  - Sales Associate  
- Adjusts difficulty based on experience level (Intern → Senior)

### 🎙️ **Voice Interaction**
- Record your answers via microphone  
- Speech-to-text using `SpeechRecognition`  
- AI voice responses (optional) using gTTS  
- Smooth chat + audio blended workflow

### 🧠 **Smart Conversation Memory**
- AI remembers previous questions  
- Responds naturally like a real interviewer  

### 🏁 **Automatic Final Report**
Triggered when the user chooses to end the interview.

Includes:
- ⭐ Overall Summary  
- ⭐ Communication Rating  
- ⭐ Technical Rating  
- ⭐ Problem-Solving Rating  
- ⭐ Domain Knowledge Rating  
- ⭐ Strengths  
- ⭐ Weaknesses  
- ⭐ Improvement Plan  
- ⭐ Hiring Recommendation  

### 🎨 **Customizable UI**
- Default clean Gradio interface  
- Optional **Spotify-inspired dark UI theme**

---

## 🛠️ Tech Stack

- **Python 3.10+**  
- **Gradio** (User Interface)  
- **Groq API** (LLaMA 3.1 model)  
- **SpeechRecognition + PyAudio**  
- **SoundFile**  
- **gTTS (Google Text-to-Speech)**  

---

## 📦 Installation

### 1️⃣ Install Dependencies
```bash
pip install groq gradio speechrecognition gtts soundfile

