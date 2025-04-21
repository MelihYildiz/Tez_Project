import requests
import json
import re
import os
from cleaning import clean_comment
from remove_duplicates import remove_duplicates
from lang_detect import is_english
from sentiment_analysis import textblob_sentiment_analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from summarizer import summarize_comments_in_chunks

API_KEY = "AIzaSyBwwuw4D_3rRzDIpEPNWakn9JY6I4dh2_g"
video_ids = ["N6BJVM5tvnw"]
analyzer = SentimentIntensityAnalyzer()

def fetch_video_title(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {"part": "snippet", "id": video_id, "key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["snippet"]["title"]
    return None

def fetch_all_youtube_comments(video_id, api_key, max_results=100):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    comments, next_page_token = [], None
    while True:
        params = {
            "part": "snippet", "videoId": video_id, "key": api_key,
            "maxResults": max_results
        }
        if next_page_token:
            params["pageToken"] = next_page_token
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
        else:
            break
    return comments, len(comments)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', "_", filename)

def save_json_to_folder(data, filename, folder):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {filepath}")

def vader_analysis(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        sentiment = "positive"
    elif score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return score, sentiment

def process_video(video_id, api_key):
    try:
        title = fetch_video_title(video_id, api_key)
        if not title:
            print(f"[WARNING] Skipping video ID {video_id} due to missing title.")
            return

        comments, total_comments = fetch_all_youtube_comments(video_id, api_key)
        cleaned_comments, removed_comments = [], []

        for comment in comments:
            cleaned = clean_comment(comment)
            if cleaned:
                cleaned_comments.append(cleaned)
            else:
                removed_comments.append(comment.strip())

        save_json_to_folder(removed_comments, f"removed_comments_{sanitize_filename(title)}.json", "removed_comments")
        unique_comments = remove_duplicates(cleaned_comments, f"unique_comments_{sanitize_filename(title)}.json")
        save_json_to_folder(unique_comments, f"unique_comments_{sanitize_filename(title)}.json", "unique_comments")
        english_comments = [c for c in unique_comments if is_english(c)]

        sentiment_results, conflicts = [], []
        for comment in english_comments:
            tb_score, tb_sentiment = textblob_sentiment_analysis(comment)
            vader_score, vader_sentiment = vader_analysis(comment)
            sentiment_results.append({
                "comment": comment,
                "textblob_score": tb_score,
                "textblob_sentiment": tb_sentiment,
                "vader_score": vader_score,
                "vader_sentiment": vader_sentiment
            })
            if tb_sentiment != vader_sentiment:
                conflicts.append({
                    "comment": comment,
                    "textblob_sentiment": tb_sentiment,
                    "vader_sentiment": vader_sentiment
                })

        sentiment_output_file = f"sentiment_analysis_{sanitize_filename(title)}.json"
        conflict_output_file = f"conflicted_sentiments_{sanitize_filename(title)}.json"
        save_json_to_folder(sentiment_results, sentiment_output_file, "sentiment_analysis")
        save_json_to_folder(conflicts, conflict_output_file, "conflicted_sentiments")

        positive_count = sum(1 for r in sentiment_results if r["textblob_sentiment"] == "positive")
        negative_count = sum(1 for r in sentiment_results if r["textblob_sentiment"] == "negative")
        neutral_count = sum(1 for r in sentiment_results if r["textblob_sentiment"] == "neutral")

        # Comment Summary Generation
        summary = summarize_comments_in_chunks(english_comments)
        summary_data = {
            "video_title": title,
            "summary": summary
        }
        save_json_to_folder(summary_data, f"summary_{sanitize_filename(title)}.json", "summaries")

        print(f"\n[PROCESS COMPLETED] Video: {title}")
        print(f"  Total comments: {total_comments}")
        print(f"  Clean comments: {len(cleaned_comments)}")
        print(f"  Unique comments: {len(unique_comments)}")
        print(f"  English comments: {len(english_comments)}")
        print(f"  Positive: {positive_count} | Negative: {negative_count} | Neutral: {neutral_count}")
        print(f"  Sentiment results saved to 'sentiment_analysis/{sentiment_output_file}'")
        print(f"  Conflicted results saved to 'conflicted_sentiments/{conflict_output_file}'")
        print(f"  Summary saved to 'summaries/summary_{sanitize_filename(title)}.json'")
        print(f"  ▶ Summary:\n  {summary}")

    except Exception as e:
        print(f"[ERROR] Error processing video ID {video_id}: {e}")

for video_id in video_ids:
    process_video(video_id, API_KEY)

print("[ALL VIDEOS PROCESSED]")