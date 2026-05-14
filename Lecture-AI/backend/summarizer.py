from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def split_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize(text):
    chunks = split_text(text)
    summaries = []

    for chunk in chunks:
        result = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
        summaries.append(result[0]['summary_text'])

    return " ".join(summaries)