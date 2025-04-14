import { fetchYouTubeComments } from './YouTubeFetcher.js';
import { CommentStore } from './CommentStore.js';
import { CommentCleaner } from './CommentCleaner.js';
import { SpamFilter } from './SpamFilter.js';
import { SentimentAnalyzer } from './SentimentAnalyzer.js';

const apiKey = "AIzaSyAjcoG-ZMbUYPu3MUYy0G8JH6xgUt3sZQg"; // Set this manually

const btn = document.getElementById("analyzeBtn");
const result = document.getElementById("result");

btn.addEventListener("click", async () => {
    result.textContent = "Fetching tab info...";

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const url = new URL(tab.url);
        const videoId = url.searchParams.get("v");

        if (!videoId) {
            result.textContent = "This is not a valid YouTube video page.";
            return;
        }

        result.textContent = "Fetching comments...";

        const rawComments = await fetchYouTubeComments(videoId, apiKey);

        const store = new CommentStore();
        store.setComments(rawComments);

        const cleaned = CommentCleaner.clean(store.getComments());
        const filtered = SpamFilter.filter(cleaned);

        const sentiment = new SentimentAnalyzer();
        const analyzed = sentiment.analyzeAll(filtered);

        const data = analyzed.map((item) => ({
            comment: item.comment,
            score: item.score
        }));

        const jsonOutput = JSON.stringify(data, null, 2);
        result.textContent = jsonOutput;

        const percentages = calculateSentimentPercentages(analyzed);
        drawSentimentChart(percentages);

    } catch (err) {
        console.error("Popup error:", err);
        result.textContent = `Error: ${err.message}`;
    }
});

function calculateSentimentPercentages(results) {
    const totals = {
        positive: 0,
        neutral: 0,
        negative: 0
    };

    results.forEach(({ score }) => {
        if (score > 0) totals.positive++;
        else if (score < 0) totals.negative++;
        else totals.neutral++;
    });

    const totalCount = results.length;
    const percentages = {
        positive: ((totals.positive / totalCount) * 100).toFixed(1),
        neutral: ((totals.neutral / totalCount) * 100).toFixed(1),
        negative: ((totals.negative / totalCount) * 100).toFixed(1)
    };

    return percentages;
}

function drawSentimentChart(percentages) {
    const ctx = document.getElementById("sentimentChart").getContext("2d");

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [{
                data: [percentages.positive, percentages.neutral, percentages.negative],
                backgroundColor: ["#66bb6a", "#f0f0f0", "#ef5350"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                },
                title: {
                    display: true,
                    text: "Sentiment Distribution (%)"
                }
            }
        }
    });
}
