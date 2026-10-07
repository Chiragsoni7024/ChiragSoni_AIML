# ⚡ Nexus: MailMate AI
**Transform simple points into perfect professional emails using Voice & AI.**

Built for the **FLUX Technical Club Task** by **Chirag Soni**.

## 🚀 Killer Features
- **🎙️ Voice-to-Text Input:** Speak your key points directly using Web Speech API (No typing required).
- **🧠 Smart AI Generation:** Powered by the latest Gemini 3.8 Flash model for precise, tone-aware emails.
- **🔄 Reply Mode:** Paste an existing email to instantly generate a professional reply.
- **💾 Local History:** Automatically saves your recent generations using an SQLite database.
- **🌐 One-Click Gmail Integration:** Instantly opens the generated email in Gmail, ready to send.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python, SQLite
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **AI Integration:** Google Generative AI (Gemini)

## 💻 Local Setup Instructions
1. Clone the repository.
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your API key: `GEMINI_API_KEY=your_api_key_here`
4. Run the server: `uvicorn main:app --reload`