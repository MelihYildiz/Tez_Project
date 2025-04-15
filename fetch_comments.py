import requests
import json
import re
import os
from transformers import pipeline
from cleaning import clean_comment  # Yorumları temizlemek için
from remove_duplicates import remove_duplicates  # Tekrarlanan yorumları kaldırmak için

API_KEY = "AIzaSyBwwuw4D_3rRzDIpEPNWakn9JY6I4dh2_g"
video_ids = ["HXFHVRS1ZW8"]

# Özetleme işlemi
class CommentSummarizer:
    def __init__(self):
        # BART modelini özetleme için yükle
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def summarize_comments(self, comments):
        # Yorumları birleştir
        combined_text = " ".join(comments)

        # Yorum uzunluğunu kontrol et ve max_length ayarla
        input_length = len(combined_text.split())

        # Eğer yorum çok kısa ise özetleme yapma, direkt olarak döndür
        if input_length < 20:
            return combined_text

        # Eğer yorum uzunluğu çok fazla ise, daha küçük parçalara ayır
        max_tokens = 1024  # Modelin işleyebileceği token sayısı
        if input_length > max_tokens:
            chunk_size = max_tokens // 2  # Modelin işleyebileceği boyutta parçalara ayır
            chunks = [combined_text[i:i+chunk_size] for i in range(0, len(combined_text), chunk_size)]
            summaries = []
            for chunk in chunks:
                chunk_summary = self.summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                summaries.append(chunk_summary[0]['summary_text'])
            return " ".join(summaries)

        # Modeli kullanarak özet al
        summary = self.summarizer(combined_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        
        # Özet dönüşü sağla
        return summary

# Yorumları çekme ve işleme
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

def save_json_to_folder(data, filename, folder):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {filepath}")

# Yorumları işleme ve özetleme işlemi
def process_video(video_id, api_key):
    try:
        title = fetch_video_title(video_id, api_key)
        if not title:
            print(f"[WARNING] Skipping video ID {video_id} due to missing title.")
            return

        comments, total_comments = fetch_all_youtube_comments(video_id, api_key)
        cleaned_comments, removed_comments = [], []

        for comment in comments:
            cleaned = clean_comment(comment)  # Temizleme işlemi
            if cleaned:
                cleaned_comments.append(cleaned)
            else:
                removed_comments.append(comment.strip())

        # Temizlenmiş yorumları kaydetme
        save_json_to_folder(removed_comments, f"removed_comments_{sanitize_filename(title)}.json", "removed_comments")
        unique_comments = remove_duplicates(cleaned_comments, f"unique_comments_{sanitize_filename(title)}.json")
        save_json_to_folder(unique_comments, f"unique_comments_{sanitize_filename(title)}.json", "unique_comments")

        # Yorumları özetle
        summarizer = CommentSummarizer()  # CommentSummarizer sınıfını kullan
        final_summary = summarizer.summarize_comments(unique_comments)  # Yorumları özetle

        summary_output_file = f"summaries_{sanitize_filename(title)}.json"
        save_json_to_folder({"summary": final_summary}, summary_output_file, "summaries")

        print(f"[PROCESS COMPLETED] Video: {title}")
        print(f"  Total comments: {total_comments}")
        print(f"  Clean comments: {len(cleaned_comments)}")
        print(f"  Unique comments: {len(unique_comments)}")
        print(f"  Comment summary saved to 'summaries/{summary_output_file}'")

    except Exception as e:
        print(f"[ERROR] Error processing video ID {video_id}: {e}")

# Ana fonksiyon
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', "_", filename)

# Örnek video işleme
process_video("HXFHVRS1ZW8", API_KEY)
