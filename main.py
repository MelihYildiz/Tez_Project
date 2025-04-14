import json
from cleaning import clean_comment  # cleaning.py içindeki temizleme fonksiyonu
from sentiment_analysis import analyze_sentiment  # sentiment_analysis.py içindeki duygu analizi fonksiyonu

def process_json(input_file, output_file):
    """
    - JSON dosyasını okur.
    - Yorumları temizler ve analiz eder.
    - Temizlenmiş ve analiz edilmiş yorumları tekrar JSON formatında kaydeder.
    """
    try:
        # Giriş dosyasını oku
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        if not isinstance(data, list):
            raise ValueError("JSON dosyası bir liste olmalıdır.")

        # Benzersiz ve işlenmiş yorumlar
        unique_comments = set()
        processed_data = []

        for comment in data:
            cleaned_comment = clean_comment(comment)
            if cleaned_comment and cleaned_comment not in unique_comments:
                unique_comments.add(cleaned_comment)
                sentiment = analyze_sentiment(cleaned_comment)
                processed_data.append({
                    "comment": cleaned_comment,
                    "sentiment": sentiment
                })

        # Yeni JSON dosyasını oluştur
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(processed_data, file, indent=4, ensure_ascii=False)

        print(f"İşlenmiş yorumlar '{output_file}' dosyasına kaydedildi.")

    except FileNotFoundError:
        print(f"'{input_file}' dosyası bulunamadı.")
    except json.JSONDecodeError:
        print(f"'{input_file}' geçerli bir JSON dosyası değil.")
    except Exception as e:
        print(f"Hata: {e}")

# Giriş ve çıkış dosya yollarını belirtin
input_file = "english_comments_The Man Who Took LSD and Changed The World.json"  # Temizlenecek yorumların JSON dosyası
output_file = "processed_comments_The Man Who Took LSD and Changed The World.json"  # İşlenmiş yorumların kaydedileceği JSON dosyası

# JSON işlemini başlat
process_json(input_file, output_file)
