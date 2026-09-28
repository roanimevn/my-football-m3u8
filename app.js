document.addEventListener('DOMContentLoaded', function () {
    var video = document.getElementById('video');
    // Đã thay đúng username 'roanimevn' và repo 'my-football-m3u8'
    var videoSrc = 'https://raw.githubusercontent.com/roanimevn/my-football-m3u8/main/highlight_football.m3u8';

    if (Hls.isSupported()) {
        var hls = new Hls();
        hls.loadSource(videoSrc);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
            video.play();
        });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // Hỗ trợ trình duyệt Safari trên iOS / Mac
        video.src = videoSrc;
        video.addEventListener('loadedmetadata', function () {
            video.play();
        });
    }
});
