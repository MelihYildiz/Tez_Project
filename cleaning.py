import re
import os

# Küfürlü veya istenmeyen kelimeler
banned_words = [
    "fuck", "fuk", "shit", "anyone here", "asshole", "bitch", "damn",
    "crap", "stupid", "idiot", "bastard", "douchebag", "bullshit"
]

# Anlamlı tek kelimelik yorumlara izin ver
allowed_single_words = {
    "good", "nice", "great", "awesome", "amazing", "wow", "excellent", "perfect",
    "cool", "love", "beautiful", "super", "funny", "thanks", "thankyou", "thankyou!", 
    "thankyou.", "thankyou!", "lovely", "okay", "yes", "no", "okay!", "amazing!","thanks", "thanks!", "thanks.", "thanks,", 
    "interesting", "love!", "best", "wow!", "true", "facts", "correct", "exactly", 
    "right", "wrong", "cool!", "damn"
}

def clean_comment(comment):
    comment = comment.strip()

    # 1. Sadece sembol/rakam olanlar
    if re.sub(r'[^\w]', '', comment) == '':
        return None

    # 2. Küfürlü içerik
    for word in banned_words:
        if word in comment.lower():
            return None

    # 3. Link içeriyorsa
    if re.search(r'http[s]?://', comment):
        return None

    # 4. Çok kısa ama anlamlı olmayan tek kelimelik yorumlar
    if len(comment.split()) < 2:
        if comment.lower() not in allowed_single_words:
            return None

    # 5. Sadece yıl
    if re.fullmatch(r'(19|20)\d{2}', comment.strip()):
        return None

    return comment

# Ana işlem fonksiyonu
def process_comments(comment_list, output_folder="output_comments"):
    cleaned = []
    removed = []

    for comment in comment_list:
        cleaned_comment = clean_comment(comment)
        if cleaned_comment:
            cleaned.append(cleaned_comment)
        else:
            removed.append(comment.strip())

    # Klasör oluştur
    os.makedirs(output_folder, exist_ok=True)

    # Temiz yorumları kaydet
    with open(os.path.join(output_folder, "cleaned_comments.txt"), "w", encoding="utf-8") as f:
        for c in cleaned:
            f.write(c + "\n")

    # Elenen yorumları kaydet
    with open(os.path.join(output_folder, "removed_comments.txt"), "w", encoding="utf-8") as f:
        for c in removed:
            f.write(c + "\n")

    print(f"Toplam: {len(comment_list)} yorum")
    print(f"✅ Temiz kalan: {len(cleaned)}")
    print(f"❌ Elenen: {len(removed)} (output_comments klasörüne kaydedildi)")

    return cleaned
