from transformers import pipeline

qg_pipeline = None


def get_question_generator():
    global qg_pipeline
    if qg_pipeline is None:
        qg_pipeline = pipeline("text2text-generation", model="t5-small")
    return qg_pipeline


def generate_questions(text):
    cleaned = (text or "").strip()
    if not cleaned:
        return "No content available to generate questions from."

    prompt = "Generate 5 study questions from this lecture: " + cleaned[:1000]
    result = get_question_generator()(prompt, max_length=200, num_beams=4, do_sample=False)
    output = result[0]["generated_text"]
    return output.strip() or "No questions could be generated from the supplied lecture."
