from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import google.generativeai as genai
import sqlite3
import os
from dotenv import load_dotenv

# API Key load karna
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
# Latest active model
model = genai.GenerativeModel('gemini-3.8-flash')

app = FastAPI(title="AI Professional Email Generator Pro")
templates = Jinja2Templates(directory="templates")

# Database setup karna (History save karne ke liye)
def init_db():
    conn = sqlite3.connect('email_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, recipient TEXT, topic TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

# History database se nikalne ka function
def get_history():
    conn = sqlite3.connect('email_history.db')
    c = conn.cursor()
    c.execute("SELECT recipient, topic, content FROM history ORDER BY id DESC LIMIT 4")
    history = c.fetchall()
    conn.close()
    return history

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    history = get_history()
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={
            "email_content": None,
            "history": history
        }
    )

@app.post("/generate", response_class=HTMLResponse)
async def generate_email(
    request: Request,
    recipient: str = Form(default=""),
    topic: str = Form(default=""),
    tone: str = Form(...),
    length: str = Form(...),
    language: str = Form(...),
    mode: str = Form(...),
    key_points: str = Form(...)
):
    try:
        if mode == "reply":
            task_instruction = "Write a professional reply to the email described in the key points."
            # Reply mode mein agar topic/recipient khali ho toh default set kar do
            if not topic: topic = "Email Reply"
            if not recipient: recipient = "Sender"
        else:
            task_instruction = "Write a brand new professional email based on the key points."

        prompt = f"""
        You are an expert professional email writer. {task_instruction}
        - Recipient: {recipient}
        - Topic: {topic}
        - Tone: {tone}
        - Length: {length}
        - Language: {language}
        - Details / Key Points: {key_points}
        
        CRITICAL INSTRUCTION: Output MUST be strictly formatted in {language} language. Do not add conversational filler.
        Subject: [Write subject here]
        
        Dear [Recipient Name/Title],
        
        [Write email body here]
        
        [Sign-off],
        [Your Name]
        """
        
        # AI se generate karwana
        response = model.generate_content(prompt)
        generated_text = response.text
        
        # Database mein save karna taaki history me dikhe
        conn = sqlite3.connect('email_history.db')
        c = conn.cursor()
        c.execute("INSERT INTO history (recipient, topic, content) VALUES (?, ?, ?)", (recipient, topic, generated_text))
        conn.commit()
        conn.close()
        
    except Exception as e:
        generated_text = f"Error aayi hai: {str(e)}"

    history = get_history()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={
            "email_content": generated_text,
            "recipient": recipient,
            "topic": topic,
            "generated_subject": topic, 
            "history": history
        }
    )