from textblob import TextBlob
import re

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Noktalama temizle
    return text

def youtube_sentiment_analysis(text):
    positive_words = list(set([
        "good", "great", "excellent", "amazing", "awesome", "fantastic", "wonderful", "impressive",
        "superb", "outstanding", "perfect", "incredible", "terrific", "brilliant", "marvelous", "delightful", 
        "lovely", "adorable", "lit", "fire", "dope", "sick", "epic", "bangin", "on point", "slaps", "vibes", 
        "fresh", "crushing it", "killing it", "next level", "hype", "legendary", "baller", "clutch", "chill",
        "boss", "wavy", "groovy", "banger", "smash hit", "game changer", "iconic", "unreal", "all-time favorite", 
        "mind-blowing", "heartfelt", "soulful", "tight","thx", "thanks" ,"thank", "congrats", "flawless", "showstopper", "climactic", "intense", 
        "masterpiece", "classic", "unstoppable", "phenomenal", "top-notch", "unbelievable", "top-tier",
        "sublime", "exceptional", "breathtaking", "jaw-dropping", "heartwarming", "masterful", "unparalleled", 
        "high-quality", "genius", "showstopping", "innovative", "dynamic", "stellar", "vibrant", 
        "fascinating", "addictive", "cool", "unmatched", "immaculate", "solid", "cutting-edge"
    ]))
    
    negative_words = list(set([
        "bad", "terrible", "awful", "boring", "disappointing", "horrible", "lackluster", "unimpressive",
        "underwhelming", "mediocre", "poor", "uninspiring", "trash", "waste of time", "unacceptable", "dull", 
        "weak", "unpleasant", "frustrating", "pointless", "rubbish", "disastrous", "lousy", "subpar", "ugly",
        "unoriginal", "cringe", "overrated", "cringe-worthy", "forgettable", "shoddy", "regrettable", "incompetent", 
        "unfocused", "flawed", "chaotic", "unpolished", "unrefined", "bland", "unsuccessful", "low-effort", 
        "unworthy", "unfit", "shabby", "broken", "disjointed", "crappy", "awkward", "messy", "annoying", 
        "unreliable", "jarring", "unremarkable", "disliked", "painful", "underachieving", "lame", 
        "terrifying", "cry", "ruins", "not cheap", "expensive", "unwatchable", "troll", "trolling"
    ]))

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
                sentiment_score -= 0.4  # Olumlu kelimeyi negatife çevir
                i += 2
                continue
            elif next_word in negative_words:
                sentiment_score += 0.4  # Negatif kelimeyi pozitife çevir (örn. "not bad")
                i += 2
                continue
        # Normal pozitif/negatif kelime kontrolü
        if word in positive_words:
            sentiment_score += 0.3
        elif word in negative_words:
            sentiment_score -= 0.3
        
        i += 1

    # Sınıflandırma
    if sentiment_score > 0.1:
        sentiment_class = "positive"
    elif sentiment_score < 0:
        sentiment_class = "negative"
    else:
        sentiment_class = "neutral"

    return sentiment_score, sentiment_class



    score, sentiment = youtube_sentiment_analysis(review)
    print(f"Comment: {review}\n→ Score: {score:.2f} | Sentiment: {sentiment}\n")
