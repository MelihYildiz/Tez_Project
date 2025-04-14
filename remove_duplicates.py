import json

# remove_duplicates.py
def remove_duplicates(comments, output_file):
    seen_comments = set()
    unique_comments = []

    for comment in comments:
        if comment.lower() not in seen_comments:
            unique_comments.append(comment)
            seen_comments.add(comment.lower())

    # Benzersiz yorumları dosyaya kaydet
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_comments, f, ensure_ascii=False, indent=4)
    return unique_comments  # Benzersiz yorumları döndür
