import { CommentStore } from './commentStore.js';
import { CommentCleaner } from './commentCleaner.js';
import { SpamFilter } from './spamFilter.js';
import { SentimentAnalyzer } from './sentimentAnalyzer.js';
import { fetchYouTubeComments } from './youTubeFetcher.js';

const store = new CommentStore();
const sentiment = new SentimentAnalyzer();

const API_KEY = 'AIzaSyAjcoG-ZMbUYPu3MUYy0G8JH6xgUt3sZQg';
const VIDEO_ID = 'f5NJQiY9AuY';

async function run() {
    const rawComments = await fetchYouTubeComments(VIDEO_ID, API_KEY);
    store.setComments(rawComments);

    const cleaned = CommentCleaner.clean(store.getComments());
    const filtered = SpamFilter.filter(cleaned);
    const results = sentiment.analyzeAll(filtered);

    console.log("Final Results:", results);

    // Chrome extension control
    if (typeof chrome !== 'undefined' && chrome.runtime) {
        chrome.storage.local.set({ sentimentResults: results });
    }
}

run();