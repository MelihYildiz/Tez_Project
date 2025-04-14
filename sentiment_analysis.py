from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

vader_analyzer = SentimentIntensityAnalyzer()

# Metni hazırla
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# TextBlob + kelime listesi ile analiz
def textblob_sentiment_analysis(text):
    positive_words = set(["awesome", "great", "amazing", "fantastic", "good", "cool", "perfect", "thanks"])
    negative_words = set(["bad", "terrible", "awful", "boring", "cringe", "lame", "troll", "disappointing"])
    negation_words = ["not", "no", "never", "barely", "hardly"]

    processed_text = preprocess_text(text)
    words = processed_text.split()
    sentiment_score = TextBlob(text).sentiment.polarity

    i = 0
    while i < len(words):
        word = words[i]
        if word in negation_words and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in positive_words:
                sentiment_score -= 0.4
                i += 2
                continue
            elif next_word in negative_words:
                sentiment_score += 0.4
                i += 2
                continue
        if word in positive_words:
            sentiment_score += 0.3
        elif word in negative_words:
            sentiment_score -= 0.3
        i += 1

    if sentiment_score > 0.1:
        return sentiment_score, "positive"
    elif sentiment_score < 0:
        return sentiment_score, "negative"
    else:
        return sentiment_score, "neutral"

# VADER ile analiz
def vader_sentiment_analysis(text):
    vs = vader_analyzer.polarity_scores(text)
    compound = vs["compound"]
    if compound >= 0.05:
        return compound, "positive"
    elif compound <= -0.05:
        return compound, "negative"
    else:
        return compound, "neutral"

# Her iki yöntemi karşılaştır ve sonucu döndür
def compare_sentiments(text):
    tb_score, tb_sentiment = textblob_sentiment_analysis(text)
    vader_score, vader_sentiment = vader_sentiment_analysis(text)

    return {
        "comment": text,
        "textblob_score": round(tb_score, 3),
        "textblob_sentiment": tb_sentiment,
        "vader_score": round(vader_score, 3),
        "vader_sentiment": vader_sentiment,
        "disagreement": tb_sentiment != vader_sentiment
    }

# Test
if __name__ == "__main__":
    test_texts = [
        "This was an awesome video!",
        "I didn't like this at all, it was boring.",
        "Not bad, but could be better.",
        "Absolutely terrible, waste of time.",
        "Perfect balance of story and visuals!",
    ]

    for text in test_texts:
        result = compare_sentiments(text)
        print(f"\nComment: {text}")
        print(f"TextBlob → {result['textblob_sentiment']} ({result['textblob_score']})")
        print(f"VADER    → {result['vader_sentiment']} ({result['vader_score']})")
        if result["disagreement"]:
            print("⚠️ Sentiment mismatch!")
