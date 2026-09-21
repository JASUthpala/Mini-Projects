from transformers import pipeline

summarizer_pipeline = None


def get_summarizer():
    global summarizer_pipeline
    if summarizer_pipeline is None:
        summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer_pipeline


def split_text(text, chunk_size=1000):
    cleaned = text.strip()
    if not cleaned:
        return []
    return [cleaned[i:i + chunk_size] for i in range(0, len(cleaned), chunk_size)]


def summarize(text):
    cleaned = (text or "").strip()
    if not cleaned:
        return "No lecture content available to summarize."

    chunks = split_text(cleaned)
    if len(chunks) == 1:
        result = get_summarizer()(chunks[0], max_length=150, min_length=30, do_sample=False, truncation=True)
        return result[0]["summary_text"]

    summaries = []
    for chunk in chunks:
        result = get_summarizer()(chunk, max_length=150, min_length=30, do_sample=False, truncation=True)
        summaries.append(result[0]["summary_text"])

    return " ".join(summaries).strip() or cleaned[:500]