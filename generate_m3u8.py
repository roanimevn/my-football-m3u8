import os
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL

# Lấy API Key từ GitHub Secrets (Environment Variable)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Danh sách các giải đấu và ID kênh YouTube chính thức
LEAGUES = {
    "Premier League": {"channel_id": "UCNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"channel_id": "UC14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"channel_id": "UC6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"channel_id": "UCBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"channel_id": "UCfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"channel_id": "UC2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_latest_highlights(youtube, channel_id, max_results=3):
    """Lấy danh sách video highlight từ YouTube."""
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            q="highlight",
            order="date",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({"title": title, "url": url})
        return videos
    except Exception as e:
        print(f"[-] Lỗi khi gọi YouTube API: {e}")
        return []

def extract_stream_url(youtube_url):
    """Dùng yt-dlp lấy link luồng phát trực tiếp."""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info.get('url')
    except Exception as e:
        print(f"[-] Không thể giải mã link {youtube_url}: {e}")
        return None

def generate_m3u8():
    if not YOUTUBE_API_KEY:
        print("[!] Không tìm thấy YOUTUBE_API_KEY. Vui lòng kiểm tra lại GitHub Secrets!")
        return

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    
    for league_name, info in LEAGUES.items():
        print(f"[+] Đang lấy highlight cho giải: {league_name}...")
        videos = get_latest_highlights(youtube, info["channel_id"], max_results=2)
        
        for video in videos:
            print(f"    - Xử lý: {video['title']}")
            stream_url = extract_stream_url(video["url"])
            if stream_url:
                m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}", {video["title"]}\n'
                m3u8_content += f'{stream_url}\n\n'
    
    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)
    print(f"\n[✓] Hoàn tất! Đã lưu file {output_file}")

if __name__ == "__main__":
    generate_m3u8()
