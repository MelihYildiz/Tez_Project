import requests
import json
import re
import os
from cleaning import clean_comment  # Temizleme fonksiyonu
from remove_duplicates import remove_duplicates  # Tekrarları silme fonksiyonu
from lang_detect import is_english  # Dil tespiti fonksiyonu
from sentiment_analysis import youtube_sentiment_analysis  # Duygu analizi fonksiyonu

# API anahtarınızı ve video ID'sini burada belirtin
API_KEY = "AIzaSyBwwuw4D_3rRzDIpEPNWakn9JY6I4dh2_g"  # Google Cloud Console'dan alınan API anahtarı
video_ids = ["j3w8-d_fnqE"]  # Çekmek istediğiniz video ID'leri

# Video başlıklarını çeker
def fetch_video_title(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": video_id,
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            title = data["items"][0]["snippet"]["title"]
            return title
    return None

# Yorumları çeker
def fetch_all_youtube_comments(video_id, api_key, max_results=100):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    comments = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "key": api_key,
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

# Dosya adındaki geçersiz karakterleri güvenli karakterlerle değiştirir
def sanitize_filename(filename):
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, "_", filename)

# Klasörde dosya kaydetme fonksiyonu
def save_json_to_folder(data, filename, folder):
    # Klasör yoksa oluştur
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Dosya yolunu oluştur
    filepath = os.path.join(folder, filename)

    # JSON verisini kaydet
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved to {filepath}")

# Bir video için yorumları işler ve kaydeder
def process_video(video_id, api_key):
    try:
        title = fetch_video_title(video_id, api_key)
        if title:
            comments, total_comments = fetch_all_youtube_comments(video_id, api_key)

            cleaned_comments = []
            removed_comments = []

            for comment in comments:
                cleaned = clean_comment(comment)
                if cleaned:
                    cleaned_comments.append(cleaned)
                else:
                    removed_comments.append(comment.strip())

            # Elenen yorumları json olarak kaydet
            removed_output_file = f"removed_comments_{sanitize_filename(title)}.json"
            save_json_to_folder(removed_comments, removed_output_file, "removed_comments")

            unique_comments = remove_duplicates(cleaned_comments, f"unique_comments_{sanitize_filename(title)}.json")
            save_json_to_folder(unique_comments, f"unique_comments_{sanitize_filename(title)}.json", "unique_comments")

            english_comments = [comment for comment in unique_comments if is_english(comment)]

            sentiment_results = [{"comment": comment, "sentiment_score": youtube_sentiment_analysis(comment)[0], 
                                  "sentiment": youtube_sentiment_analysis(comment)[1]} for comment in english_comments]

            sentiment_output_file = f"sentiment_analysis_{sanitize_filename(title)}.json"
            save_json_to_folder(sentiment_results, sentiment_output_file, "sentiment_analysis")

            # Sayım işlemleri
            positive_count = sum(1 for result in sentiment_results if result["sentiment"] == "positive")
            negative_count = sum(1 for result in sentiment_results if result["sentiment"] == "negative")
            neutral_count = sum(1 for result in sentiment_results if result["sentiment"] == "neutral")

            print(f"\n[PROCESS COMPLETED] Video: {title}")
            print(f"  Total comments: {total_comments}")
            print(f"  Clean comments: {len(cleaned_comments)}")
            print(f"  Unique comments: {len(unique_comments)}")
            print(f"  English comments: {len(english_comments)}")
            print(f"  Sentiment analysis saved to 'sentiment_analysis/{sentiment_output_file}'")
            print(f"  Removed comments saved to 'removed_comments/{removed_output_file}'")
            print(f"  Positive comments: {positive_count}")
            print(f"  Negative comments: {negative_count}")
            print(f"  Neutral comments: {neutral_count}")
        else:
            print(f"[WARNING] Skipping video ID {video_id} due to missing title.")
    except Exception as e:
        print(f"[ERROR] Error processing video ID {video_id}: {e}")

# Videoları sırayla işle
for video_id in video_ids:
    process_video(video_id, API_KEY)

print("[ALL VIDEOS PROCESSED]")
