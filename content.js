
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'detectDeepfake') {
        
        var videoUrl = window.location.href;
        var videoId = extractYouTubeVideoId(videoUrl);

        if (videoId) {
       
            chrome.runtime.sendMessage({ action: 'startDeepfakeDetection', videoId: videoId });
        } else {
            console.error('Invalid YouTube video URL:', videoUrl);
        }
    }
});

function extractYouTubeVideoId(url) {
    var urlParams = new URLSearchParams(new URL(url).search);
    return urlParams.get('v');
}
