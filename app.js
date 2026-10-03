document.addEventListener('DOMContentLoaded', function () {
    const playlistUrl = 'https://raw.githubusercontent.com/roanimevn/my-football-m3u8/main/highlight_football.m3u8';

    fetch(playlistUrl)
        .then(response => response.text())
        .then(data => {
            const lines = data.split('\n');
            const playlistContainer = document.getElementById('playlist');
            playlistContainer.innerHTML = '';

            let currentTitle = '';
            let channels = [];

            for (let i = 0; i < lines.length; i++) {
                let line = lines[i].trim();
                if (line.startsWith('#EXTINF:')) {
                    // Lấy tên kênh từ thẻ #EXTINF
                    let parts = line.split(',');
                    if (parts.length > 1) {
                        currentTitle = parts.slice(1).join(',').trim();
                    }
                } else if (line.startsWith('http')) {
                    if (currentTitle) {
                        channels.push({ title: currentTitle, url: line });
                        currentTitle = '';
                    }
                }
            }

            if (channels.length > 0) {
                // Phát video đầu tiên mặc định
                playVideo(channels[0].url);

                // Tạo danh sách nút bấm chọn kênh
                channels.forEach((item, index) => {
                    let btn = document.createElement('button');
                    btn.className = 'channel-btn' + (index === 0 ? ' active' : '');
                    btn.innerText = item.title;
                    btn.onclick = function () {
                        document.querySelectorAll('.channel-btn').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        playVideo(item.url);
                    };
                    playlistContainer.appendChild(btn);
                });
            } else {
                playlistContainer.innerHTML = 'Không tìm thấy kênh nào.';
            }
        })
        .catch(err => {
            console.error(err);
            document.getElementById('playlist').innerHTML = 'Lỗi tải playlist m3u8.';
        });
});

function playVideo(url) {
    const iframe = document.getElementById('main-player');
    iframe.src = url;
}
