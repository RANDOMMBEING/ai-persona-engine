# AI Persona Engine 🤖

Welcome to the **AI Persona Engine**! This is a simple, beginner-friendly Streamlit application that lets you chat with different AI personas. You can even create your own custom persona on the fly!

This project uses Python, Streamlit (for the UI), and LangChain (to connect to OpenAI and remember the conversation).

## ✨ Features
- **Multiple Built-in Personas**: Talk to Advocate Ananya Sharma, Tech Mentor Rahul Verma, and more.
- **Custom Persona Builder (Wizard & Advanced)**: Want to talk to a supportive friend or a fictional character? Create them in the sidebar using our foolproof Step-by-Step Wizard, or paste your own raw prompt in Advanced Mode!
- **Cost-Efficient Conversation Memory**: The AI uses a dynamic Buffer Memory system. It stores your chat raw at zero cost, and only when the conversation gets incredibly long does it securely summarize old messages in the background to save your API tokens.
- **Real-Time Typing (Streaming)**: Watch the AI type out its response letter by letter, just like ChatGPT.
- **Premium Dark UI**: The app features a custom glassmorphic description box and a sleek dark purple theme.
- **Turn Limits**: To prevent run-on conversations, the system implements a strict 21-turn limit per session.

---

## 🛠️ Setup Instructions

### 1. Install Dependencies
You need to install a few Python libraries to make this work. Open your terminal and run:
```bash
pip install -r requirements.txt
```

### 2. Add your OpenAI API Key
This app uses OpenAI to generate text, so you need an API key. 
1. Create a new file named `.env` in the same folder as this README.
2. Open the `.env` file and add your key like this:
```text
OPENAI_API_KEY="sk-your-super-secret-api-key-here"
```
*(Never share your `.env` file or upload it to GitHub!)*

### 3. Run the App
To start the application, type this in your terminal:
```bash
streamlit run app.py
```
A browser window will pop up automatically, and you can start chatting!

---

## 📁 File Structure

- **`app.py`**: The main file. It builds the Streamlit user interface and handles all the buttons and text boxes.
- **`conversation.py`**: The "brain" of the app. It talks to OpenAI using LangChain, handles the memory, and streams the text back to the screen.
- **`personas.py`**: A simple dictionary that stores the default personas and their secret instructions (system prompts).

---

## 💡 How the Code Works (For Beginners)

If you look inside the code, you'll see it's written to be very easy to read:
- We avoid confusing "enterprise" Python tricks.
- We use simple `for` loops to create dropdown menus.
- We use a basic `try/except` block to safely check if the API key exists.
- We use `import warnings` to hide scary-looking library deprecation notices from the console.
- We added simple, conversational comments explaining exactly what each section does!

---

## 🐛 Troubleshooting

If you run into issues, don't panic! Here are a few common fixes:
- **"No module named..." error:** Make sure you've activated your virtual environment and ran `pip install -r requirements.txt`.
- **App crashes on startup:** Double-check your `.env` file! If the `OPENAI_API_KEY` isn't set properly, the app won't know how to connect to the AI.
- **Dropdown takes two clicks:** This is a common Streamlit glitch. We fixed this in the code by using `st.rerun()` right after the persona is selected to instantly refresh the screen!
- **Chat input disappears:** This means you hit the 21-turn hard limit! Just click "Clear Chat" in the sidebar to reset your turns to zero.
