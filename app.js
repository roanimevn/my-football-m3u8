document.addEventListener('DOMContentLoaded', function () {
    // Đọc file playlist m3u8 để lấy link video YouTube mới nhất
    var playlistUrl = 'https://raw.githubusercontent.com/roanimevn/my-football-m3u8/main/highlight_football.m3u8';

    fetch(playlistUrl)
        .then(response => response.text())
        .then(data => {
            // Tìm link YouTube đầu tiên trong file m3u8
            var lines = data.split('\n');
            var youtubeUrl = '';
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i].trim();
                if (line.includes('youtube.com/watch?v=')) {
                    youtubeUrl = line;
                    break;
                }
            }

            if (youtubeUrl) {
                // Trích xuất Video ID từ link YouTube
                var videoId = youtubeUrl.split('v=')[1];
                if (videoId.includes('&')) {
                    videoId = videoId.split('&')[0];
                }
                
                // Nhúng iframe YouTube vào trình phát
                var iframe = document.getElementById('youtube-iframe');
                iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&enablejsapi=1`;
            } else {
                console.error('Không tìm thấy link video trong file m3u8');
            }
        })
        .catch(error => {
            console.error('Lỗi khi tải file m3u8:', error);
        });
});
