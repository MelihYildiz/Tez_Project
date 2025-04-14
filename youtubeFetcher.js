export async function fetchYouTubeComments(videoId, apiKey) {
    const apiUrl = `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&key=${apiKey}&maxResults=100`;

    const response = await fetch(apiUrl);
    const data = await response.json();

    return data.items.map(item => item.snippet.topLevelComment.snippet.textDisplay);
}