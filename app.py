!pip install groq gradio speechrecognition gtts soundfile

import os
import gradio as gr
import speech_recognition as sr
import soundfile as sf
import tempfile
from gtts import gTTS
from groq import Groq

os.environ["GROQ_API_KEY"] = "Your-Groq-API-key"
client = Groq()

SYSTEM_PROMPT = """
You are an Interview Practice Partner AI.

- Conduct mock interviews for the chosen role: {role}
- Adapt difficulty to experience level: {level}
- Ask ONE specific question at a time.
- Ask realistic follow-up questions.
- Do NOT give feedback unless the user ends the interview.
"""

def call_llm(role, level, history, user_text):
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(role=role, level=level)}]

    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})

    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=900,
    )

    return response.choices[0].message.content


def transcribe_audio(audio):
    if audio is None:
        return ""

    try:
        sample_rate, data = audio

        if len(data.shape) == 2:
            data = data.mean(axis=1) 

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp.name, data, sample_rate)

        rec = sr.Recognizer()
        with sr.AudioFile(tmp.name) as src:
            audio_data = rec.record(src)

        return rec.recognize_google(audio_data)

    except Exception as e:
        return f"[Transcription error: {e}]"

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(tmp.name)
    return tmp.name

def interview_step(text_input, audio_input, history, role, level, voice_reply):
    history = history or []

    user_msg = (text_input or "").strip()

    if user_msg == "" and audio_input is not None:
        user_msg = transcribe_audio(audio_input)

    if user_msg == "":
        return "", None, history, None

    wrap_up_phrases = ["yes", "okay", "ok", "sure", "let's wrap", "wrap up",
                       "stop", "end", "finish", "i am done", "done"]

    last_bot_message = history[-1][1].lower() if history else ""

    bot_asked_to_stop = (
        "wrap up" in last_bot_message or
        "stop here" in last_bot_message or
        "end the interview" in last_bot_message or
        "want to stop" in last_bot_message
    )

    user_agreed_to_stop = any(word in user_msg.lower() for word in wrap_up_phrases)

    if bot_asked_to_stop or user_agreed_to_stop:

        final_feedback_prompt = """
The interview is now over. Provide a structured final evaluation.

FORMAT EXACTLY LIKE THIS:

====================
🏁 FINAL INTERVIEW REPORT
====================

📌 **Overall Summary (3–4 sentences)**
- Provide a brief overview of the candidate’s performance.

--------------------
⭐ **Ratings (1–10 scale)**
- Communication Skills: X/10
- Technical Ability: X/10
- Problem-Solving: X/10
- Confidence: X/10
- Domain Knowledge: X/10

--------------------
💪 **Strengths**
• Bullet point strengths
• Based on their answers

--------------------
⚠️ **Weaknesses / Areas For Improvement**
• Bullet points
• Actionable improvements

--------------------
📘 **Recommended Preparation Plan**
• 3–5 items the candidate should do to improve
• Include tools, courses, or habits

--------------------
📝 **Hiring Recommendation**
Choose exactly one:
• Strong Yes
• Yes
• Maybe
• No
"""

        bot_msg = call_llm(role, level, history, final_feedback_prompt)
        history.append([user_msg, bot_msg])

        audio_out = text_to_speech(bot_msg) if voice_reply else None
        return "", None, history, audio_out



    bot_msg = call_llm(role, level, history, user_msg)
    history.append([user_msg, bot_msg])

    audio_out = text_to_speech(bot_msg) if voice_reply else None
    return "", None, history, audio_out


with gr.Blocks() as demo:
    gr.Markdown("## 🎤 AI Interview Practice Partner — Voice + Chat")

    with gr.Row():
        role = gr.Dropdown(
            ["Software Engineer", "Data Analyst", "Sales Associate", "Product Manager"],
            value="Data Analyst",
            label="Interview Role",
        )
        level = gr.Dropdown(
            ["Intern", "Junior", "Mid-level", "Senior"],
            value="Junior",
            label="Experience Level",
        )
        voice_reply = gr.Checkbox(label="AI Should Speak Responses", value=False)

    chatbot = gr.Chatbot(label="Interview Conversation")

    text_in = gr.Textbox(
        placeholder="Type your answer or record below…",
        label="Your Answer (Text)"
    )

    with gr.Row():
        audio_in = gr.Audio(
            sources=["microphone"],
            type="numpy",
            label="🎙️ Speak Your Answer"
        )
        audio_out = gr.Audio(
            label="AI Voice Output",
            autoplay=True
        )

    send = gr.Button("Send Answer")

    send.click(
        interview_step,
        inputs=[text_in, audio_in, chatbot, role, level, voice_reply],
        outputs=[text_in, audio_in, chatbot, audio_out],
    )

demo.launch(share=True)

