from flask import Flask, request, jsonify
import os

from speech_to_text import transcribe_audio
from pdf_extractor import extract_text_from_pdf
from summarizer import summarize
from question_generator import generate_questions

app = Flask(__name__)

UPLOAD_FOLDER = "../uploads"

@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Detect file type
    if file.filename.endswith(".mp3") or file.filename.endswith(".wav"):
        text = transcribe_audio(file_path)
    elif file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        return jsonify({"error": "Unsupported file type"})

    summary = summarize(text)
    questions = generate_questions(text)

    return jsonify({
        "summary": summary,
        "questions": questions
    })

if __name__ == "__main__":
    app.run(debug=True)