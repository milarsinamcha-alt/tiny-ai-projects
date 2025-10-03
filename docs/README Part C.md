# Project Documentation: Gemini Q&A Chatbot Deployment

**Note:** I am uploading this document separately because my earlier projects were built to run offline on Bash, while this one is deployed online using Hugging Face Spaces.

## Part C of the Assignment  
### Project Name: `my-gemini-qna`  
**Platform:** Hugging Face Space (Streamlit)  
**Goal:** Deploy a functional, persistent chat application using Google's Gemini API.

---

## Initial Setup
At first, I created a Hugging Face account, logged in, and then created a new Space with **CPU Basic** (free version). I used **Apache 2.0** license (Default/Best Practice), which is an excellent choice for open-source apps where maximum community adoption and commercial use is permitted.

All modifications and file creations were performed directly within the Hugging Face Space's **web file editor**; no local files were uploaded.

---

## I. File Structure
The project required three critical files to run correctly:

1. `chatbot_app.py` → The main Python application code containing the Streamlit UI and Gemini logic.  
2. `requirements.txt` → Lists all necessary Python dependencies for the build process.  
3. `Dockerfile` → Defines the container environment and contains crucial, early-executed environment variables to fix permission issues.

---

## Phase 1: Resolving the PermissionError
The application initially failed with the error:  
`PermissionError: [Errno 13] Permission denied: '/.streamlit'`  

This happened because Streamlit tries to write temporary files (like usage statistics) to the root directory, which is restricted in cloud containers.

| Status      | File/Action | Rationale |
|-------------|-------------|-----------|
| Attempt 1 (Partial Fail) | Created `.streamlit/config.toml` file in main branch with `gatherUsageStats = false`. | Standard fix, but failed because container executed code too early, before parsing the file. |
| Attempt 2 (Partial Fail) | Added `os.environ["HOME"] = "/tmp"` in `chatbot_app.py`. | Fix was executed too late; error still occurred before script started. |
| Final Solution (Success) | Modified `Dockerfile` to include `ENV HOME="/tmp"` and `ENV STREAMLIT_GATHER_USAGE_STATS="false"`. | Setting these environment variables at container build level forced Streamlit to use the writable `/tmp` directory immediately. |

---

## Phase 2: Resolving Dependency and Application Errors

| Error | Cause | Fix Applied |
|-------|-------|-------------|
| `SyntaxError: invalid syntax` | Accidentally pasted placeholder text instead of Python code into `chatbot_app.py`. | Replaced with full, correct Python code. |
| `ImportError: cannot import name 'genai' from 'google'` | Missing SDK not specified in dependencies list. | Updated `requirements.txt` to include correct package: `google-genai`. |

---

## Phase 3: Resolving the API Key Access

| Error | Cause | Solution Implemented |
|-------|-------|-----------------------|
| `streamlit.errors.StreamlitSecretNotFoundError` | Application could not find `GEMINI_API_KEY` in `st.secrets`. | 1. Key securely saved in Hugging Face Secrets panel.<br>2. Modified code in `chatbot_app.py` to read only from system environment variable: `os.environ.get("GEMINI_API_KEY")`. |

This final change eliminated the error and allowed the application to successfully initialize the Gemini client.

---

## Final Configuration Summary

The application is currently running with a friendly and helpful AI persona.

| File | Key Contents/Fixes |
|------|---------------------|
| **Dockerfile** | `ENV HOME="/tmp"` (Permission Fix) and `ENV STREAMLIT_GATHER_USAGE_STATS="false"` (Usage Stats Fix). |
| **requirements.txt** | `streamlit` and `google-genai`. |
| **chatbot_app.py** | `os.environ["HOME"] = "/tmp"` (Programmatic fix) and `system_instruction` defines the AI's persona. |
| **Secrets Manager** | Contains the `GEMINI_API_KEY` environment variable. |

---

✅ **Status:** Successfully deployed and functional on Hugging Face Space.  
direct link to the bot "https://huggingface.co/spaces/milarsinam/my-gemini-qna"
