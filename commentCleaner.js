export class CommentCleaner {
    static isEnglish(text) {
        const englishRegex = /^[\x00-\x7F]*$/;
        return englishRegex.test(text);
    }

    static clean(comments) {
        return comments
            .map(c => c.trim().toLowerCase())
            .filter(c => CommentCleaner.isEnglish(c));
    }
    static removeSpecialChars(text) {
        // Remove #, *, /, <, > and script tags
        return text
            .replace(/[#*/<>]/g, '')             // bu sembolleri sil
            .replace(/<script.*?>.*?<\/script>/gi, '')  // script tag'lerini tamamen kaldır
            .replace(/\s{2,}/g, ' ');             // gereksiz fazla boşlukları da sil
    }
}
