import json

# remove_duplicates.py
def remove_duplicates(comments, output_file):
    seen_comments = set()
    unique_comments = []

    for comment in comments:
        if comment.lower() not in seen_comments:
            unique_comments.append(comment)
            seen_comments.add(comment.lower())

    return unique_comments  # Benzersiz yorumları döndür
