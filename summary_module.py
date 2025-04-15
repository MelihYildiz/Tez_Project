import json
import os
from transformers import pipeline

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
        if input_length < 50:
            return combined_text
        
        # Modeli kullanarak özet al
        summary = self.summarizer(combined_text, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
        
        # Özet dönüşü sağla
        return summary

# Yorumları okuma ve genel fikri özetleme işlemi
def process_unique_comments():
    try:
        # 'unique_comments.json' dosyasını oku
        unique_comments_file = "unique_comments/unique_comments_example.json"  # Dosya yolunu buraya ekleyin
        with open(unique_comments_file, 'r', encoding='utf-8') as f:
            unique_comments = json.load(f)
        
        # Yorumları özetle
        summarizer = CommentSummarizer()  # CommentSummarizer sınıfını kullan
        general_summary = summarizer.summarize_comments(unique_comments)  # Tüm yorumları özetle
        
        # Özet çıktısını kaydet
        summary_output_file = "summaries/general_summary.json"
        save_json_to_folder({"summary": general_summary}, summary_output_file, "summaries")

        print(f"[PROCESS COMPLETED] General summary saved to '{summary_output_file}'")

    except Exception as e:
        print(f"[ERROR] Error processing unique comments: {e}")

# JSON dosyasını belirtilen klasöre kaydetme
def save_json_to_folder(data, filename, folder):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {filepath}")

# Ana fonksiyon
process_unique_comments()
