import os
import tempfile

import gradio as gr
import speech_recognition as sr
import soundfile as sf
from gtts import gTTS
from groq import Groq


SYSTEM_PROMPT = """
You are an Interview Practice Partner AI.

- Conduct mock interviews for the chosen role: {role}
- Adapt difficulty to experience level: {level}
- Ask ONE specific question at a time.
- Ask realistic follow-up questions.
- Do NOT give feedback unless the user ends the interview.
"""


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set. "
            "Set it before running the app."
        )
    return Groq(api_key=api_key)


client = get_client()


def call_llm(role, level, history, user_text):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.format(role=role, level=level),
        }
    ]

    # Build conversation history
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": user_text})

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=900,
    )

    return resp.choices[0].message.content


def transcribe_audio(audio):
    """Convert microphone input (numpy array) to text."""
    if audio is None:
        return ""

    try:
        sample_rate, data = audio

        # Convert stereo to mono if needed
        if len(data.shape) == 2:
            data = data.mean(axis=1)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, data, sample_rate)

            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp.name) as src:
                audio_data = recognizer.record(src)

        return recognizer.recognize_google(audio_data)

    except Exception as exc:
        return f"[Transcription error: {exc}]"


def text_to_speech(text: str):
    """Turn bot response into an mp3 file path."""
    tts = gTTS(text=text, lang="en")
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(tmp.name)
    return tmp.name


def interview_step(text_input, audio_input, history, role, level, voice_reply):
    history = history or []

    user_msg = (text_input or "").strip()

    # If no text, try to use audio instead
    if not user_msg and audio_input is not None:
        user_msg = transcribe_audio(audio_input)

    if not user_msg:
        # Nothing to process
        return "", None, history, None

    # --- Check for wrap-up / final feedback case ---
    wrap_up_phrases = [
        "yes",
        "okay",
        "ok",
        "sure",
        "let's wrap",
        "wrap up",
        "stop",
        "end",
        "finish",
        "i am done",
        "done",
    ]

    last_bot_message = history[-1][1].lower() if history else ""

    bot_asked_to_stop = any(
        phrase in last_bot_message
        for phrase in (
            "wrap up",
            "stop here",
            "end the interview",
            "want to stop",
        )
    )

    user_agreed_to_stop = any(
        phrase in user_msg.lower() for phrase in wrap_up_phrases
    )

    if bot_asked_to_stop and user_agreed_to_stop:
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
        # Clear inputs after processing
        return "", None, history, audio_out

    # --- Normal interview question/answer flow ---
    bot_msg = call_llm(role, level, history, user_msg)
    history.append([user_msg, bot_msg])

    audio_out = text_to_speech(bot_msg) if voice_reply else None
    return "", None, history, audio_out


def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## 🎤 Interview Practice Partner")

        with gr.Row():
            role = gr.Dropdown(
                [
                    "Software Engineer",
                    "Data Analyst",
                    "Sales Associate",
                    "Product Manager",
                ],
                value="Data Analyst",
                label="Interview Role",
            )

            level = gr.Dropdown(
                ["Intern", "Junior", "Mid-level", "Senior"],
                value="Junior",
                label="Experience Level",
            )

            voice_reply = gr.Checkbox(
                label="Speak AI responses", value=False
            )

        chatbot = gr.Chatbot(label="Interview Conversation")

        text_in = gr.Textbox(
            placeholder="Type your answer or use the mic below...",
            label="Your Answer (Text)",
        )

        with gr.Row():
            audio_in = gr.Audio(
                sources=["microphone"],
                type="numpy",
                label="🎙️ Speak Your Answer",
            )
            audio_out = gr.Audio(
                label="AI Voice Output",
                autoplay=True,
            )

        send_btn = gr.Button("Send Answer")

        send_btn.click(
            fn=interview_step,
            inputs=[text_in, audio_in, chatbot, role, level, voice_reply],
            outputs=[text_in, audio_in, chatbot, audio_out],
        )

    return demo


if __name__ == "__main__":
    app = build_interface()
    # Adjust host/port as needed for deployment
    app.launch()
