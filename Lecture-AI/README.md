# Lecture-AI
Lecture AI is a simple local application that converts lecture audio or PDF files into short summaries and useful questions.
It runs completely offline after the first setup.

---

## 🚀 Features
- 🎤 Convert audio (.mp3, .wav) to text
- 📄 Extract text from PDFs
- 🧠 Generate summaries
- ❓ Generate questions
- 🌐 Simple web interface
- 🔒 No paid APIs (fully local)

---

## 🏗️ Project Structure
Lecture-AI/
│
├── backend/
├── frontend/
├── uploads/

---

## ⚙️ Installation

Open terminal in the project folder and run:
- pip install flask transformers torch sentencepiece
- pip install openai-whisper
- pip install pymupdf

## ▶️ Run the Project
### 1. Start Backend
- cd backend
- python app.py

You should see:
Running on http://127.0.0.1:5000/

### 2. Open Frontend

- Go to frontend/ and open:
index.html

### 3. Use the App
- Upload .mp3, .wav, or .pdf
Wait a few seconds

View:
- Summary
- Questions

---


## ⚠️ First Run
- Models will download (~1–2GB)
- Takes some time
- After that → works offline

---


## 🧪 Troubleshooting

- Torch error
pip install torch

- Too slow
Change in speech_to_text.py:
whisper.load_model("tiny")

- Memory issues
Reduce chunk size in summarizer.py

---


## 🎯 Use Case

Helpful for:

- Studying lectures
- Quick revision
- Generating practice questions
