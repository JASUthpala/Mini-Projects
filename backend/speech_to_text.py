import whisper

model = whisper.load_model("base")  # use "tiny" if slow

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]