# Tiny AI Q&A Bot (Offline Bash Project)


I first tried using OpenAI API for this bot, but it was not free and caused errors.  
So I switched to the Gemini API which provides a free tier.  
This whole project is meant to run offline from bash on my system.  

**Note:**  
For this project, I used **Gemini API** for building and coding the chatbot, and **ChatGPT** to help me write and refine the documentation.  
This whole project is meant to run offline from Bash on my system.

---

## Step-by-Step Plan: AI Q&A Bot  

### Part 1: Setup and Documentation  

Install Python and Create a Virtual Environment  
I have bash already installed before for posting projects on GitHub.  

1) I created a folder name Projects on E disk on my computer  
and open bash and used this command  
```bash
cd /e/Projects
```  
to make the directory in this project folder.  

2) Using this command I created a directory named "tiny-ai-qna-bot":  
```bash
mkdir tiny-ai-qna-bot
cd tiny-ai-qna-bot
```  

3) I need to create a virtual environment (A virtual environment will keep my project's dependencies separate from your main system, preventing conflicts.)  
```bash
python -m venv venv
```  
to create virtual environment and used activation command to activate it.  

4) First I installed OpenAI:  
```bash
pip install openai python-dotenv
```  
(Note: openai is a non-standard library, used to connect to OpenAI servers, send secret key, etc.)  

5) Created a new OpenAI secret key from:  
👉 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)  

Steps:  
- Log In → API Keys page  
- Create new secret key  
- Name it (e.g., TinyQnABot)  
- Copy full secret key (starts with sk-...)  

6) I created a `.env` file and pasted the secret key there.  
I also created `.gitignore` file and added:  
```
venv/
.env
__pycache__/*.pyc
```  

This ensures venv and secret keys are ignored from GitHub.  

---

### Part 2: Coding, Testing, and Final Commit  

7) Writing the Core Application (app.py) (OpenAI version first):  

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    client = OpenAI()
except Exception as e:
    print("Error: Could not initialize OpenAI client.")
    exit()

print("\n🤖 AI Q&A Bot Initialized! Ask me anything (type 'quit' to exit).")

def run_qna_bot():
    while True:
        user_question = input("\nYou: ")
        if user_question.lower() in ('quit', 'exit'):
            print("Goodbye!")
            break
        if not user_question.strip():
            continue
        print("Bot: Thinking...")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful, brief, and concise Q&A assistant."},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7 
            )
            answer = response.choices[0].message.content
            print(f"Bot: {answer}")
        except Exception as e:
            print(f"API error: {e}")

if __name__ == "__main__":
    run_qna_bot()
```

But this failed since OpenAI was not free.  
So I switched to **Gemini API**.  

---

## Project Documentation: Tiny AI Q&A Bot (Gemini API Version) 🤖  

### Part 1: Setup and Documentation (Revised)  

Steps 1-3: Already done (created folder, venv). ✅  

Step 4 (Revised): Install Gemini libraries  
```bash
pip uninstall openai -y
pip install google-generativeai python-dotenv
```  

Step 5 (Revised): Get Gemini API Key  
👉 [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)  

Update `.env` file:  
```
GOOGLE_API_KEY=AIzaSy...
```  

Confirm `.gitignore` still has `.env`.  

---

### Part 2: Coding with Gemini  

7) Writing the Core Application (Gemini version, app.py):  

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- 1. Setup and Initialization ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
    exit()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print("Error: Could not initialize Gemini client.")
    print(f"Details: {e}")
    exit()

print("\n🤖 AI Q&A Bot Initialized with Gemini! Ask me anything (type 'quit' to exit).")

# --- 2. Main Q&A Loop ---
def run_qna_bot():
    while True:
        user_question = input("\nYou: ")
        if user_question.lower() in ('quit', 'exit'):
            print("Goodbye!")
            break
        if not user_question.strip():
            continue
        print("Bot: Thinking...")
        try:
            response = model.generate_content(
                contents=[
                    "You are a helpful, brief, and concise Q&A assistant.",
                    user_question
                ],
                config=genai.types.GenerateContentConfig(
                    temperature=0.7
                )
            )
            answer = response.text
            print(f"Bot: {answer}")
        except Exception as e:
            print(f"API error: {e}")

if __name__ == "__main__":
    run_qna_bot()
```

---

### Step 8: Testing  

Make sure `(venv)` is active in terminal.  
Run:  
```bash
python app.py
```  

Test:  
```
You: hello
Bot: Hello!

You: how are you
Bot: I am an AI, ready to assist.
```  

✅ Working fine with Gemini API.
