import whisper

model = None


def get_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model


def transcribe_audio(file_path):
    result = get_model().transcribe(file_path)
    return result["text"]