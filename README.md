<h1 style="font-size: 48px;">🎤 AI Interview Practice Partner — Voice + Chat</h1>


An interactive, voice-enabled AI mock interview system built using Groq LLM, Gradio, Speech Recognition, and gTTS.
It conducts realistic interviews, adapts to your experience level, and generates a structured Final Interview Report with ratings, strengths, weaknesses, and improvement plans.

<h2 style="font-size: 48px;">🚀 Features</h2>

🎙 Microphone Input — Speak your interview answers.

💬 Chat Input — Type instead of speaking.

🧠 LLM-Driven Interviewer — Asks context-aware follow-up questions.

🎛 Role & Experience Selection.

🤖 Voice Output (optional) with gTTS.

📄 Final Evaluation Report including:

Ratings (1–10)

Strengths

Weaknesses

Recommended preparation plan

Hiring recommendation

⚡ Low-latency responses via Groq.

<h2 style="font-size: 48px;">Tech Stack</h2>


| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| **Python 3.10+**      | Core programming language       |
| **Gradio**            | Web UI framework                |
| **Groq LLM API**      | Interview questions & responses |
| **SpeechRecognition** | Microphone → Text               |
| **SoundFile**         | Handling raw audio              |
| **gTTS**              | Text → Speech                   |
| **Tempfile**          | Temporary audio storage         |


<h2 style="font-size: 48px;">📦 Installation & Setup</h2>

Follow these steps to run the AI Interview Partner locally.

<h3 style="font-size: 48px;">1️⃣ Clone the Repository</h3>
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

<h3 style="font-size: 48px;">2️⃣ Install Dependencies
</h3>

pip install -r requirements.txt


If you don’t have a requirements file, use:

pip install groq gradio speechrecognition gtts soundfile

<h3 style="font-size: 48px;">3️⃣ Set Your API Key
</h3>

Create a .env file or export the key in your terminal:

export GROQ_API_KEY="your_api_key_here"

<h3 style="font-size: 48px;">4️⃣ Run the App
</h3>
python app.py


A Gradio link will appear → open it in your browser.


<h2 style="font-size: 48px;">🏗 Architecture Overview</h2>


<img width="644" height="660" alt="image" src="https://github.com/user-attachments/assets/80246fd5-fd42-48bd-836f-9bb688dd2d87" />

    
<h2 style="font-size: 48px;">🧩 Key Design Decisions</h2>

1. Groq LLM instead of OpenAI

Very low latency → perfect for live interaction

Excellent speed/accuracy ratio

Cheaper & easy to scale

Reasoning:
I wanted the interviewer to feel “real-time”. Groq delivers sub-100ms responses.

2. Gradio UI instead of Streamlit

Built-in audio recording

Native chatbot component

Fast prototyping

Easy to embed CSS themes

Reasoning:
Gradio is designed for ML demos — perfect match for a conversational tool.

3. Simple Conversation Memory (List of Pairs)
history = [[user_message, assistant_message], ...]


Reasoning:
Interview conversations are linear; no need for complex vector stores or memory libs.

4. Template-Based Final Report

Instead of building a custom evaluation algorithm, I designed a strict structured prompt.

Reasoning:

Consistent format every time

Professional look

Easy to parse if needed later

5. Google SpeechRecognition Instead of Whisper

Whisper requires a GPU for fast inference

Google SR is lightweight & perfect for short interview answers

Reasoning:
Compatible with CPU-only machines (perfect for students & Colab users).



📝 Example Final Report
====================
🏁 FINAL INTERVIEW REPORT
====================

📌 Overall Summary:
You communicated clearly and demonstrated growing confidence. Your technical foundation is solid...

⭐ Ratings
- Communication Skills: 8/10
- Technical Ability: 7/10
- Problem-Solving: 6/10
- Confidence: 8/10
- Domain Knowledge: 7/10

💪 Strengths
• Clear communication  
• Good structured thinking  
• Strong fundamentals  

⚠️ Areas for Improvement
• SQL optimization skills  
• Provide more real-world examples  

📘 Preparation Plan
• Practice STAR method  
• Review SQL JOINS/CTEs  
• Take mock interviews weekly  

📝 Hiring Recommendation
• **Yes**

🚧 Future Improvements

Add downloadable PDF report

Add progress tracking dashboard

Add job-specific interview packs (Python, SQL, ML, HR)

Upgrade to Whisper for better transcription

Add login + saved history

📄 License

This project is released under the MIT License.
