
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'startDeepfakeDetection') {

        var videoId = request.videoId;

        var videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
        fetch('http://127.0.0.1:5000/detect_deepfake_youtube', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ video_url: videoUrl })
        })
        .then(response => response.json())
        .then(data => {
            
            if (data.is_deepfake) {
                console.log('Deepfake content detected!');
                chrome.tabs.sendMessage(sender.tab.id, { action: 'showDeepfakeDetectionResult', isDeepfake: true });
            } else {
                console.log('No deepfake content detected.');
                chrome.tabs.sendMessage(sender.tab.id, { action: 'showDeepfakeDetectionResult', isDeepfake: false });
            }
        })
        .catch(error => {
            console.error('Error detecting deepfake:', error);

        });
    }
});
