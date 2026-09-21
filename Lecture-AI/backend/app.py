import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from pdf_extractor import extract_text_from_pdf
from question_generator import generate_questions
from speech_to_text import transcribe_audio
from summarizer import summarize

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "uploads"))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def ensure_upload_folder(folder_path=None):
    target = folder_path or app.config["UPLOAD_FOLDER"]
    os.makedirs(target, exist_ok=True)
    return True


def detect_media_type(filename):
    if filename is None:
        return None

    lowered = filename.lower()
    if lowered.endswith((".mp3", ".wav")):
        return "audio"
    if lowered.endswith(".pdf"):
        return "pdf"
    return None


@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    ensure_upload_folder()
    file_type = detect_media_type(uploaded_file.filename)
    if file_type is None:
        return jsonify({"error": "Unsupported file type. Please upload a PDF, MP3, or WAV file."}), 400

    safe_name = secure_filename(uploaded_file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
    uploaded_file.save(file_path)

    try:
        if file_type == "audio":
            text = transcribe_audio(file_path)
        else:
            text = extract_text_from_pdf(file_path)

        if not text or not text.strip():
            return jsonify({"error": "No text could be extracted from the uploaded file."}), 400

        summary = summarize(text)
        questions = generate_questions(text)

        return jsonify({
            "summary": summary,
            "questions": questions,
        })
    except Exception as exc:
        return jsonify({"error": f"Processing failed: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)