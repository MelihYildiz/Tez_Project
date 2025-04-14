export class SentimentAnalyzer {
    constructor(wordScores) {
        this.wordScores = wordScores || {
            // Positive words with weights
            "amazing": 3,
            "awesome": 2,
            "beautiful": 2,
            "brilliant": 2,
            "cheerful": 2,
            "delightful": 2,
            "ecstatic": 3,
            "excited": 2,"enough":2,"good luck":2,
            "fantastic": 3,
            "flawless": 3,
            "genius": 2,
            "grateful": 2,
            "happy": 2,
            "hopeful": 2,
            "impressive": 2,
            "incredible": 3,
            "joyful": 2,
            "legendary": 3,
            "lovely": 2,
            "love": 3,
            "magical": 2,
            "masterpiece": 3,
            "neat": 1,
            "perfect": 3,
            "pog": 2,
            "remarkable": 2,
            "respectful": 1,
            "satisfying": 2,
            "slay": 2,
            "smooth": 1,
            "solid": 1,
            "superb": 2,
            "sweet": 2,
            "thankful": 2,"i think so":3,"i agree":3,
            "thrilling": 2,
            "valuable": 2,
            "wonderful": 3,
            "wholesome": 2,
            "yas": 2,"yeah":2,"yes":2,
            "w": 1,
            "this made my day": 3,
            "absolutely loved it": 3,
            "gave me goosebumps": 2,
            "this is everything i needed": 3,
            "you nailed it": 2,
            "chef’s kiss": 2,
            "hands down the best video": 3,
            "i'm blown away": 3,
            "my favorite video": 2,
            "i didn’t expect to cry today. wow.": 3,
            "this hit me right in the feels": 3,
            "why am i crying in the club right now?": 2,
            "not all heroes wear capes": 2,
            "i was not ready for this level of greatness": 3,
            "i came here to laugh, and i stayed for the feels": 2,
            "who’s chopping onions here?": 2,
            "okay, now i’m emotionally invested": 2,
            "it started as a joke, and now it’s my favorite": 2,
            "didn't know i needed this until now": 2,

            // Negative words with weights
            "awful": -3,"but":-1,
            "bad": -2,
            "boring": -2,
            "cringe": -2,
            "disappointed": -2,
            "disgusting": -3,
            "dreadful": -3,
            "fail": -2,
            "fake": -2,
            "horrible": -3,
            "hate": -3,
            "lame": -2,
            "mess": -2,
            "painfull":-2,
            "poor": -2,
            "rude": -2,
            "sad": -2,
            "terrible": -3,
            "trash": -2,
            "ugly": -2,
            "worst": -3,
            "wtf": -2,
            "yikes": -2,
            "this was a disaster": -3,
            "i regret watching this": -3,
            "total waste of time": -3,
            "i hated every second of this": -3,
            "just awful": -2,
            "this made no sense": -2,
            "what a mess": -2,
            "this video is misleading": -3,
            "this is so cringe": -2,
            "painfully bad": -2,
            "not worth watching": -3,
            "i’m disappointed": -2,
            "worst thing i’ve seen today": -3,
            "nothing good about this": -2,
            "this ruined my mood": -3,
            "i expected more": -2,
            "really poor quality": -3,
            "completely unnecessary": -2,
            "this was hard to watch": -2,
            "this gave me secondhand embarrassment": -2,
            "loved how they wasted 10 minutes of my life": -3,
            "great job making me regret watching this": -3,
            "if cringe had a face, this would be it": -2,
            "this belongs in the hall of shame": -3,
            "they tried... i guess": -2,
            "i laughed. but not in a good way": -2,
            "quality content... if you're into torture": -3,
            "chef’s kiss... for disaster": -2,
            "at least it ended": -2
        };
    }

    analyze(comment) {
        const words = comment.split(/\s+/);
        let score = 0;
        words.forEach(word => {
            if (this.wordScores[word]) {
                score += this.wordScores[word];
            }
        });
        return score;
    }

    analyzeAll(comments) {
        return comments.map(comment => ({
            comment,
            score: this.analyze(comment)
        }));
    }
}
