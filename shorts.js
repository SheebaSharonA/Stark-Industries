document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('detectButton').addEventListener('click', function() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            var tab = tabs[0];
            if (tab && tab.url.includes('youtube.com/watch')) {
                var videoUrl = extractYouTubeVideoUrl(tab.url);
                if (videoUrl) {
                    if (isYouTubeShorts(videoUrl)) {
                        detectDeepfake(videoUrl);
                    } else {
                        displayResult('This is not a YouTube Shorts video.');
                    }
                } else {
                    displayResult('Invalid YouTube video URL.');
                }
            } else {
                displayResult('Please navigate to a YouTube video page.');
            }
        });
    });
});

function extractYouTubeVideoUrl(url) {
    var urlParams = new URLSearchParams(new URL(url).search);
    return urlParams.get('v');
}

function isYouTubeShorts(videoUrl) {
    return videoUrl.includes('shorts');
}

function detectDeepfake(videoId) {
    var apiUrl = 'http://127.0.0.1:5000/detect_deepfake_youtube';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.is_deepfake) {
                    displayResult('Deepfake content detected!');
                } else {
                    displayResult('No deepfake content detected.');
                }
            } else {
                console.error('Error detecting deepfake:', xhr.statusText);
                displayResult('Error detecting deepfake. Please try again.');
            }
        }
    };
    xhr.onerror = function() {
        console.error('Error detecting deepfake: Network error');
        displayResult('Error detecting deepfake. Please try again.');
    };
    xhr.send(JSON.stringify({ video_url: `https://www.youtube.com/watch?v=${videoId}` }));
}

function displayResult(message) {
    document.getElementById('resultText').textContent = message;
}
