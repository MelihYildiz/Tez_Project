# lang_detect.py

import json
from langdetect import detect

# Yorumların dilini tespit etmek için fonksiyon
def is_english(comment):
    try:
        language = detect(comment)
        return language == 'en'
    except:
        # Hata durumunda (örneğin, boş yorum) False döndür
        return False

# JSON dosyasındaki İngilizce yorumları seçip yeni bir JSON dosyasına kaydedecek fonksiyon
def filter_english_comments(input_filename, output_filename):
    # JSON dosyasını oku
    with open(input_filename, 'r', encoding='utf-8') as infile:
        comments_data = json.load(infile)
    
    # Yalnızca İngilizce yorumları filtrele
    english_comments = []
    for comment in comments_data:
        if is_english(comment):
            english_comments.append(comment)
    
    # Filtrelenmiş İngilizce yorumları yeni bir JSON dosyasına kaydet
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(english_comments, outfile, ensure_ascii=False, indent=4)
