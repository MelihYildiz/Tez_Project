import html
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_comments_in_chunks(comments: list[str], chunk_size=100):
    if not comments:
        return "No comments to summarize."

    summaries = []
    for i in range(0, len(comments), chunk_size):
        chunk = " ".join(comments[i:i+chunk_size])
        chunk = chunk[:3000]  # Max token sınırı
        try:
            partial = summarizer(chunk, max_length=60, min_length=20, do_sample=False)
            summary_text = html.unescape(partial[0]["summary_text"])
            summaries.append(summary_text)
        except Exception as e:
            print(f"[WARNING] Skipped chunk due to error: {e}")

    # Küçük özetlerden büyük özet çıkar
    combined_summary = " ".join(summaries)
    try:
        final_summary = summarizer(combined_summary, max_length=120, min_length=50, do_sample=False)
        return html.unescape(final_summary[0]["summary_text"])
    except Exception as e:
        print(f"[ERROR] Final summary failed: {e}")
        return "Summary failed."
