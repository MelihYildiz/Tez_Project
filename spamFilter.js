export class SpamFilter {
    static spamPhrases = [

        "free", "click here", "subscribe", "giveaway", "buy now","what song?","song name?","comment",


        "greetings from", "listening in", "still listening", "still here",
        "from 2024", "from 2023", "from 2022", "from the future", "from the past",


        "visit my profile", "check my channel", "win a prize", "telegram", "whatsapp group","add me"
    ];

    static isSpam(comment) {
        const lower = comment.toLowerCase();
        return this.spamPhrases.some(phrase => lower.includes(phrase));
    }

    static filter(comments) {
        return comments.filter(c => !this.isSpam(c));
    }
}