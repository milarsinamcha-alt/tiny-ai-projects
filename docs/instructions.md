# Instructions for Tiny AI Bots

## Offline Bot (Part A & B)

**Purpose:** Run locally on your computer using Bash.  

### Setup

1. Make sure Python and Bash are installed.  
2. Navigate to the offline bot folder:
```bash
cd offline-bot
```
3. Activate virtual environment:
```bash
source venv/Scripts/activate   # Windows
# OR
source venv/bin/activate       # Linux/Mac
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Create a `.env` file with your Gemini API key:
```
GOOGLE_API_KEY=your_key_here
```
You must create your own Gemini API key from: [Google Cloud API](https://console.cloud.google.com/apis/library)

### Running

```bash
python app.py
```

---

## Online Bot (Part C)

**Purpose:** Run only on **Hugging Face Spaces**.  

### Setup

1. Go to [Hugging Face](https://huggingface.co/) and create an account.  
2. Create a new Space using **Streamlit CPU (free)**.  
3. Upload the `online-bot` folder content to the Space.  
4. Add your **Gemini API Key** via **Secrets** in the Hugging Face Space:  

   - Key name: `GEMINI_API_KEY`  
   - Value: your key from [Google Cloud API](https://console.cloud.google.com/apis/library)  

### Running

- Press **"Run"** in Hugging Face.  
- The chat interface will appear in the browser.  
- Type your questions and the bot will respond using Gemini.

