from urllib import response
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import gradio as gr
from google import genai
from google.genai import types

import os

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


reader = PdfReader("1.foundations/me/Profile.pdf")
linkedIn = ""

print("Reading PDF file...")
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedIn += text


with open("1.foundations/me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()


name = "Joseph Adedeji Adewunmi"


system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so.

## Summary:
{summary}

## LinkedIn Profile:
{linkedIn}

With this context, please chat with the user, always staying in character as {name}."""


def chat(message, history):
    # Build conversation context for Gemini
    conversation_text = f"System instructions: {system_prompt}\n\n"

    # Add conversation history
    if history:
        for msg in history:
            if isinstance(msg, dict):
                # Handle dict format with role/content
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    conversation_text += f"User: {content}\n"
                elif role == "assistant":
                    conversation_text += f"Assistant: {content}\n"
            elif isinstance(msg, (list, tuple)) and len(msg) == 2:
                # Handle tuple/list format [user_msg, assistant_msg]
                user_msg, assistant_msg = msg
                conversation_text += f"User: {user_msg}\n"
                if assistant_msg:  # Only add if assistant responded
                    conversation_text += f"Assistant: {assistant_msg}\n"

    # Add current user message
    conversation_text += f"User: {message}\n"
    conversation_text += "Assistant: "

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=conversation_text
        )
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I apologise, but I encountered an error while processing your request. Please try again."


gr.ChatInterface(chat, type="messages").launch()
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Explain how AI works in a few words",
# )
# print(response.text)
