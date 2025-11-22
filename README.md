📄 AI Interview Practice Partner — Voice + Chat

An interactive, voice-enabled mock interview system powered by Groq LLMs, Gradio, and Speech Recognition.
This project simulates realistic interview conversations, adapts to user experience levels, and generates a detailed final performance report with ratings and insights.

This repository is designed as a complete demonstration of building an AI-driven tool that conducts interviews, listens via microphone input, transcribes speech, and provides professional feedback at the end.

🚀 Features

🎙 Voice Input — Speak your answers using your microphone.

🧠 LLM-driven Interviewer — Asks realistic interview questions one at a time.

🔄 Adaptive Difficulty based on experience level (Intern → Senior).

🤖 Final Interview Report — Ratings, strengths, weaknesses, improvement plan.

🗣 Optional AI Voice Output using gTTS.

💬 Chat-based and Voice Mixed Input.

🖥 Clean Gradio Interface.

⚙️ Modular structure for easy extension.

🛠️ Tech Stack
Component	Purpose
Python 3.10+	Main programming language
Gradio	Web UI (chat, audio input, buttons, layout)
Groq API	LLM model for generating interview responses
SpeechRecognition	Converts microphone audio → text
SoundFile	Saves raw audio input temporarily
gTTS	Converts AI output → speech
Tempfile	Handles temporary audio storage
📦 Installation & Setup Instructions

Follow these steps to run the project locally.

1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Set Your Groq API Key

You need to create a .env file or export it in your terminal:

export GROQ_API_KEY="your_api_key_here"


(You can get a key from https://console.groq.com
)

4️⃣ Run the Application
python app.py


You will see a Gradio link in your terminal — open it in your browser.

🏗️ Architecture Overview

This project is structured around five main components:

app.py
│
├── SYSTEM_PROMPT        # Defines interviewer behavior
├── call_llm()           # Sends conversation context to Groq LLM
├── transcribe_audio()   # Converts audio → text
├── text_to_speech()     # Converts text → AI voice
├── interview_step()     # Core stateful logic of the interview
└── Gradio UI            # Layout and interaction layer

🔎 How It Works (Flow)

User speaks or types an answer.

If audio is used → transcribe using SpeechRecognition.

The system appends the answer to chat history.

Sends the full conversation to Groq LLM.

LLM responds with next interview question or a final report.

Optionally converts response to voice.

Updates the UI in real time.

🧩 Key Design Decisions (Human Explanation)
1️⃣ Using Groq LLM instead of OpenAI

I chose Groq because:

It provides extremely low latency, which is essential for real-time conversation.

Groq's llama-3.1-8b-instant model is fast and lightweight but still high quality.

Lower cost and easier scaling for a personal/academic project.

2️⃣ Gradio for UI instead of Streamlit

Reasons:

Gradio provides native audio components (mic recording, playback).

Chatbot and audio widgets integrate seamlessly.

Much simpler to embed custom CSS themes.

3️⃣ Manual Conversation Memory Design

Instead of using a vector database or memory manager, I store chat as simple pairs:

history = [[user_msg, bot_reply], ...]


Why?

The interview format is linear.

It reduces overhead.

Easy to modify and debug.

4️⃣ Generating the Final Interview Report via Prompting

Instead of building a long evaluation system manually, I used:

✔ A structured system prompt
✔ A strict final report template

This ensures:

Consistency

Professional formatting

Easy parsing if needed later

5️⃣ Using Google SpeechRecognition Instead of Whisper

Reasoning:

Whisper requires GPU and is slow on free environments.

Google SR is lightweight and works fast for short interview answers.

No large model downloads needed.

🧠 Reasoning Behind the Overall Design

This project is designed with simplicity, performance, and real-world interview simulation in mind.

Low Latency is Crucial
An interviewer waiting 4–8 seconds feels unnatural.
Groq + small Llama model solves this.

Voice Interaction Increases Realism
Most real interviews involve speaking, not typing.
Adding microphone input adds authenticity.

Final Report Helps Learning
Users need more than Q&A — they need feedback.
So I made a multi-part report with:

Ratings

Strengths

Weaknesses

Preparation plan

Hiring recommendation

Lightweight Architecture
No backend database, no auth, no deployment server required.
Easy for anyone to clone and run.

🎯 Usage Guide

Select Role (Software Engineer, Data Analyst, etc.).

Select Experience Level (Intern → Senior).

Start responding using:

microphone

OR text box

Continue until the interviewer asks:

“Do you want to wrap up?”

Say or type:

"yes",

"okay",

"let’s wrap up", etc.

The AI generates a final evaluation report.

📌 Example Outputs
Sample Strengths Section
• Demonstrated good foundational SQL knowledge
• Communicated step-by-step reasoning clearly
• Asked clarifying questions when needed

Sample Ratings
Communication Skills: 8/10
Technical Ability: 7/10
Problem-Solving: 6/10
Confidence: 8/10
Domain Knowledge: 7/10

🛠 Future Enhancements

Add topic-specific interview modes (e.g., Python-only, SQL-only).

Replace Google SR with Whisper if GPU available.

Add dashboard for tracking scores over time.

Add database to store interview history.

Improve UI with a more modern framework if deployed permanently.

📄 License

This project is open-source under the MIT License.
Feel free to use, modify, and share.
