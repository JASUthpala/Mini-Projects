from transformers import pipeline

qg_pipeline = pipeline("text2text-generation", model="t5-small")

def generate_questions(text):
    text = text[:1000]  # limit input

    prompt = "Generate 5 questions from this lecture: " + text

    result = qg_pipeline(prompt, max_length=150)

    return result[0]['generated_text']